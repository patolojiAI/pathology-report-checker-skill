#!/usr/bin/env python3
"""
Multi-Pass Pathology Report Checker

Mimics Claude skill behavior by breaking analysis into 6 focused passes,
each with only the relevant reference material. This dramatically improves
accuracy with smaller local LLMs compared to the single-prompt approach.

Pipeline:
  Pass 1 — Element Extraction    (report → structured JSON)
  Pass 2 — Compliance Check      (extracted JSON + diagnosis checklist → gaps)
  Pass 3 — Macroscopy Evaluation  (macroscopy text + AAPA guidelines → assessment)
  Pass 4 — Staging Verification   (extracted pT/pN/M + staging tables → verification)
  Pass 5 — Cross-validation       (all previous JSONs → consistency checks + score)
  Pass 6 — Summary Report         (all JSONs → human-readable QA report)

Usage:
    # Single report with Ollama
    python check_report_multipass.py --provider ollama --file report.txt

    # Single report with LM Studio
    python check_report_multipass.py --provider lmstudio --file report.txt

    # Single report with Claude
    python check_report_multipass.py --provider anthropic --file report.txt

    # Batch mode from Excel
    python check_report_multipass.py --provider ollama --batch data.xlsx --output-dir results/

    # Specify model and tumor type
    python check_report_multipass.py -p ollama -m mistral:latest -t colorectal -f report.txt

    # Save intermediate JSON (debug/audit)
    python check_report_multipass.py -p ollama --save-intermediates -f report.txt
"""

import os
import sys
import json
import time
import argparse
import re
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
DEFAULT_OLLAMA_MODEL = "mistral:latest"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_LMSTUDIO_URL = "http://localhost:1234/v1"

OLLAMA_NUM_CTX = 16384      # Smaller context is fine per-pass (was 32K for single)
OLLAMA_NUM_PREDICT = 4096   # Max output tokens per pass


# ============================================================================
# REFERENCE FILE LOADING
# ============================================================================

def get_skill_dir() -> Path:
    """Get the skill directory. Checks multiple locations."""
    candidates = [
        Path(__file__).parent.parent,                    # scripts/ inside skill
        Path(__file__).parent / "pathology-report-checker-skill",
        Path.home() / "Documents/GitHub/pathology-report-checker-skill",
    ]
    # Also check env var
    env_dir = os.environ.get("SKILL_DIR")
    if env_dir:
        candidates.insert(0, Path(env_dir))

    for d in candidates:
        if (d / "SKILL.md").exists():
            return d
    return candidates[0]


def load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def load_references(skill_dir: Path, tumor_type: str = "colorectal") -> Dict[str, str]:
    """Load reference files organized by pass needs."""
    reference_map = {
        "pancreas": "diagnosis/exocrine_pancreas.md",
        "breast": "diagnosis/breast_invasive_carcinoma.md",
        "colorectal": "diagnosis/colorectal_resection.md",
        "gastric": "diagnosis/gastric_carcinoma.md",
    }

    refs = {
        "skill": load_file(skill_dir / "SKILL.md"),
        "diagnosis": load_file(skill_dir / "references" / reference_map.get(tumor_type, "")),
        "staging": load_file(skill_dir / "references" / "staging" / "tnm_stage_calculator.md"),
        "macroscopy": load_file(skill_dir / "references" / "macroscopy" / f"{tumor_type}_macroscopy.md"),
    }

    # Fallback: try generic macroscopy
    if not refs["macroscopy"]:
        macro_dir = skill_dir / "references" / "macroscopy"
        if macro_dir.exists():
            for f in macro_dir.glob("*.md"):
                if tumor_type in f.stem.lower():
                    refs["macroscopy"] = load_file(f)
                    break

    return refs


# ============================================================================
# LLM CALLING (Ollama Native, OpenAI-compat, Anthropic)
# ============================================================================

def call_ollama_native(prompt: str, model: str, base_url: str,
                       system: str = "", num_ctx: int = OLLAMA_NUM_CTX) -> str:
    """Call Ollama native /api/chat with configurable context."""
    import requests

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = requests.post(
        f"{base_url}/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "num_ctx": num_ctx,
                "num_predict": OLLAMA_NUM_PREDICT,
            },
        },
        timeout=600,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


def call_openai_compat(prompt: str, model: str, base_url: str,
                       system: str = "") -> str:
    """Call OpenAI-compatible API (LM Studio)."""
    from openai import OpenAI
    client = OpenAI(base_url=base_url, api_key="not-needed")

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        max_tokens=OLLAMA_NUM_PREDICT,
        messages=messages,
    )
    return response.choices[0].message.content


def call_anthropic(prompt: str, model: str, system: str = "") -> str:
    """Call Anthropic API."""
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    kwargs = {
        "model": model,
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system

    response = client.messages.create(**kwargs)
    return response.content[0].text


def call_llm(prompt: str, provider: str, model: str,
             base_url: str = "", system: str = "") -> str:
    """Unified LLM caller."""
    if provider == "ollama":
        return call_ollama_native(prompt, model, base_url or DEFAULT_OLLAMA_URL, system)
    elif provider == "lmstudio":
        return call_openai_compat(prompt, model, base_url or DEFAULT_LMSTUDIO_URL, system)
    elif provider == "anthropic":
        return call_anthropic(prompt, model or DEFAULT_ANTHROPIC_MODEL, system)
    else:
        raise ValueError(f"Unknown provider: {provider}")


# ============================================================================
# JSON PARSING HELPERS
# ============================================================================

def extract_json(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown fences and preamble."""
    # Try direct parse first
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # Try extracting from markdown code fences
    patterns = [
        r'```json\s*\n(.*?)\n\s*```',
        r'```\s*\n(.*?)\n\s*```',
        r'\{[\s\S]*\}',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                candidate = match.group(1) if match.lastindex else match.group(0)
                return json.loads(candidate)
            except (json.JSONDecodeError, IndexError):
                continue

    # Last resort: find first { to last }
    start = text.find('{')
    end = text.rfind('}')
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    # Return as error wrapper
    return {"_raw_response": text, "_parse_error": "Could not extract JSON"}


def safe_json_str(data: dict) -> str:
    """Convert dict to formatted JSON string."""
    return json.dumps(data, indent=2, ensure_ascii=False)


# ============================================================================
# PASS 1: ELEMENT EXTRACTION
# ============================================================================

PASS1_SYSTEM = """You are a pathology data extraction system. Your ONLY job is to extract structured data from pathology reports. Output ONLY valid JSON, no explanation."""

PASS1_PROMPT = """Extract all reportable elements from this pathology report into structured JSON.

<checklist>
Extract these elements if present (use null if not found):

SPECIMEN:
- specimen_type: (e.g., "right hemicolectomy", "sigmoid colectomy")
- laterality: (right/left/transverse/sigmoid/rectum)

TUMOR:
- tumor_site: anatomical location
- tumor_size_cm: largest dimension as number
- histologic_type: (e.g., "adenocarcinoma", "mucinous adenocarcinoma")
- histologic_grade: (well/moderately/poorly differentiated, or G1/G2/G3)
- depth_of_invasion: (mucosa/submucosa/muscularis propria/pericolorectal tissue/serosa/adjacent organs)

STAGING:
- pT: pathological T stage (pTis/pT1/pT2/pT3/pT4a/pT4b)
- pN: pathological N stage (pN0/pN1a/pN1b/pN1c/pN2a/pN2b)
- pM: (pM1a/pM1b/pM1c or null)
- reported_stage_group: if explicitly stated (e.g., "Stage IIIB")

LYMPH NODES:
- total_nodes_examined: number
- positive_nodes: number
- tumor_deposits: number or null

MARGINS:
- proximal_margin: (negative/positive/distance in cm)
- distal_margin: (negative/positive/distance in cm)
- radial_margin: (negative/positive/distance in cm, or "not applicable")
- margin_status_overall: (R0/R1/R2 or null)

ADDITIONAL:
- lymphovascular_invasion: (present/absent/not identified)
- perineural_invasion: (present/absent/not identified)
- tumor_budding: (low/intermediate/high or null)
- mismatch_repair: (intact/deficient/not tested) and individual markers if available
- kras_braf_status: if available
- microsatellite_instability: (MSS/MSI-H/MSI-L or null)
- treatment_effect: if neoadjuvant therapy given
- additional_findings: list of other notable findings (polyps, colitis, etc.)
</checklist>

<pathology_report>
{report_text}
</pathology_report>

Return ONLY a JSON object with the fields above. Use null for missing elements. Do not add commentary."""


# ============================================================================
# PASS 2: COMPLIANCE CHECK
# ============================================================================

PASS2_SYSTEM = """You are a pathology compliance auditor. Compare extracted report elements against required guidelines and identify gaps. Output ONLY valid JSON."""

PASS2_PROMPT = """Compare these extracted pathology report elements against CAP/ICCR required elements for colorectal carcinoma.

<extracted_elements>
{extracted_json}
</extracted_elements>

<required_elements_reference>
{diagnosis_reference}
</required_elements_reference>

For each required element, classify as:
- "present": element found and adequate
- "missing": element not found at all
- "incomplete": element found but inadequate (explain why)

Assign severity to each gap:
- "critical": Essential for staging/treatment decisions (e.g., pT, pN, margins, histologic type)
- "major": Required by CAP but not stage-defining (e.g., LVI, PNI, tumor budding)
- "minor": Recommended but not strictly required (e.g., tumor size in exact mm)

Return JSON:
{{
  "elements_checked": [
    {{
      "element": "element name",
      "status": "present|missing|incomplete",
      "severity": "critical|major|minor",
      "detail": "explanation if missing or incomplete"
    }}
  ],
  "critical_missing": ["list of critical missing elements"],
  "major_missing": ["list of major missing elements"],
  "minor_missing": ["list of minor missing elements"],
  "total_required": <number>,
  "total_present": <number>,
  "compliance_percentage": <number 0-100>
}}"""


# ============================================================================
# PASS 3: MACROSCOPY EVALUATION
# ============================================================================

PASS3_SYSTEM = """You are a pathology macroscopy evaluator. Assess gross description completeness against AAPA guidelines. Output ONLY valid JSON."""

PASS3_PROMPT = """Evaluate this macroscopic (gross) description of a colorectal specimen against standard macroscopy guidelines.

<macroscopy_text>
{macroscopy_text}
</macroscopy_text>

<macroscopy_guidelines>
{macroscopy_reference}
</macroscopy_guidelines>

Check for these required macroscopy elements:
1. Specimen identification and type
2. Specimen dimensions (length, circumference)
3. Tumor location and distance from margins
4. Tumor size (3 dimensions)
5. Tumor appearance (polypoid, ulcerated, annular, etc.)
6. Depth of penetration (gross assessment)
7. Serosal involvement (if applicable)
8. Margin descriptions (proximal, distal, radial/mesenteric)
9. Lymph node search description and count
10. Other lesions (polyps, diverticula, etc.)
11. Background mucosa description
12. Ink application description

Return JSON:
{{
  "macroscopy_elements": [
    {{
      "element": "element name",
      "status": "present|missing|incomplete",
      "detail": "what was found or what's missing"
    }}
  ],
  "macroscopy_score": <number 0-100>,
  "strengths": ["list of well-documented elements"],
  "gaps": ["list of missing or incomplete elements"],
  "recommendations": ["specific improvements"]
}}"""


# ============================================================================
# PASS 4: STAGING VERIFICATION
# ============================================================================

PASS4_SYSTEM = """You are a pathology staging calculator. Verify TNM staging using AJCC 8th edition criteria. Output ONLY valid JSON."""

PASS4_PROMPT = """Verify the TNM staging for this colorectal carcinoma case.

<extracted_staging>
- pT: {pT}
- pN: {pN}
- pM: {pM}
- Reported stage group: {reported_stage}
- Total nodes examined: {total_nodes}
- Positive nodes: {positive_nodes}
- Tumor deposits: {tumor_deposits}
- Depth of invasion: {depth_of_invasion}
- Histologic grade: {grade}
</extracted_staging>

<staging_reference>
{staging_reference}
</staging_reference>

Perform these checks:
1. Is pT consistent with described depth of invasion?
2. Is pN consistent with node count? (pN1a=1 node, pN1b=2-3, pN2a=4-6, pN2b=7+)
3. If tumor deposits present with no positive nodes, should be pN1c
4. Calculate expected stage group from pT + pN + pM using AJCC 8th edition
5. Compare calculated stage with reported stage
6. Check if ≥12 nodes examined (quality indicator)

Return JSON:
{{
  "reported": {{
    "pT": "{pT}",
    "pN": "{pN}",
    "pM": "{pM}",
    "stage_group": "{reported_stage}"
  }},
  "calculated_stage_group": "calculated stage",
  "staging_match": true/false,
  "staging_discrepancy": "explanation if mismatch, null if match",
  "pT_consistent": true/false,
  "pT_note": "explanation",
  "pN_consistent": true/false,
  "pN_note": "explanation",
  "node_quality": {{
    "total_examined": {total_nodes},
    "meets_minimum_12": true/false,
    "node_ratio": "positive/total"
  }},
  "staging_issues": ["list of any staging problems found"]
}}"""


# ============================================================================
# PASS 5: CROSS-VALIDATION & SCORING
# ============================================================================

PASS5_SYSTEM = """You are a pathology quality assessor. Cross-validate findings and compute a final compliance score. Output ONLY valid JSON."""

PASS5_PROMPT = """Cross-validate all findings from previous analysis passes and compute a final quality score.

<pass1_extraction>
{pass1_json}
</pass1_extraction>

<pass2_compliance>
{pass2_json}
</pass2_compliance>

<pass3_macroscopy>
{pass3_json}
</pass3_macroscopy>

<pass4_staging>
{pass4_json}
</pass4_staging>

Perform cross-validation checks:
1. pT vs described depth of invasion — consistent?
2. pN vs node counts — mathematically correct?
3. Margins vs R classification — if margins positive, should be R1/R2
4. Tumor size vs pT — does size support the T stage?
5. Grade vs differentiation description — consistent terminology?
6. LVI/PNI status vs staging implications
7. Macroscopy vs microscopy — do gross and micro findings agree?

Compute final scores:
- diagnosis_completeness (0-100): from pass 2 compliance
- macroscopy_completeness (0-100): from pass 3
- staging_accuracy (0-100): from pass 4
- internal_consistency (0-100): from cross-validation checks above
- overall_score (0-100): weighted average (diagnosis 40%, macroscopy 15%, staging 25%, consistency 20%)

Return JSON:
{{
  "cross_validation_checks": [
    {{
      "check": "check name",
      "result": "pass|fail|warning|not_applicable",
      "detail": "explanation"
    }}
  ],
  "scores": {{
    "diagnosis_completeness": <number>,
    "macroscopy_completeness": <number>,
    "staging_accuracy": <number>,
    "internal_consistency": <number>,
    "overall_score": <number>
  }},
  "overall_status": "Excellent|Good|Needs Improvement|Significant Gaps|Incomplete",
  "critical_issues": ["issues requiring immediate attention"],
  "recommendations": ["prioritized list of improvements"]
}}"""


# ============================================================================
# PASS 6: HUMAN-READABLE SUMMARY
# ============================================================================

PASS6_SYSTEM = """You are a pathology quality assurance reporter. Write a clear, actionable QA report from structured analysis data. Respond in the same language as the original report."""

PASS6_PROMPT = """Write a human-readable QA report from this structured analysis of a pathology report.

<case_info>
Case: {case_no}
Tumor Type: {tumor_type}
Analysis Date: {analysis_date}
Model: {model}
</case_info>

<extraction>
{pass1_json}
</extraction>

<compliance>
{pass2_json}
</compliance>

<macroscopy_evaluation>
{pass3_json}
</macroscopy_evaluation>

<staging_verification>
{pass4_json}
</staging_verification>

<cross_validation_and_scores>
{pass5_json}
</cross_validation_and_scores>

Write a structured QA report with these sections:

1. OVERALL ASSESSMENT — Score, status, one-line summary
2. KEY FINDINGS — What was correctly reported
3. MISSING ELEMENTS — Organized by severity (critical → major → minor)
4. STAGING REVIEW — Reported vs calculated, any discrepancies
5. MACROSCOPY REVIEW — Completeness assessment
6. CROSS-VALIDATION — Any internal inconsistencies found
7. RECOMMENDATIONS — Prioritized, actionable items

Keep it concise and actionable. Use the same language as the original pathology report.
Do NOT output JSON — write a clear text report."""


# ============================================================================
# MULTI-PASS PIPELINE
# ============================================================================

class MultiPassAnalyzer:
    """Orchestrates the 6-pass analysis pipeline."""

    def __init__(self, provider: str, model: str, base_url: str = "",
                 skill_dir: Path = None, tumor_type: str = "colorectal",
                 quiet: bool = False, save_intermediates: bool = False):
        self.provider = provider
        self.model = model
        self.base_url = base_url
        self.skill_dir = skill_dir or get_skill_dir()
        self.tumor_type = tumor_type
        self.quiet = quiet
        self.save_intermediates = save_intermediates
        self.refs = load_references(self.skill_dir, tumor_type)

    def log(self, msg: str):
        if not self.quiet:
            print(msg, file=sys.stderr, flush=True)

    def _call(self, prompt: str, system: str = "") -> str:
        return call_llm(prompt, self.provider, self.model, self.base_url, system)

    def _call_json(self, prompt: str, system: str = "") -> dict:
        """Call LLM and parse JSON response, with one retry on parse failure."""
        raw = self._call(prompt, system)
        result = extract_json(raw)

        if "_parse_error" in result:
            self.log("  ↳ JSON parse failed, retrying with stricter prompt...")
            retry_prompt = (
                prompt
                + "\n\nIMPORTANT: Your previous response was not valid JSON. "
                "Return ONLY a valid JSON object. No text before or after the JSON."
            )
            raw = self._call(retry_prompt, system)
            result = extract_json(raw)

        return result

    # ------------------------------------------------------------------
    # INDIVIDUAL PASSES
    # ------------------------------------------------------------------

    def pass1_extract(self, report_text: str) -> dict:
        """Pass 1: Extract structured elements from report."""
        self.log("  Pass 1/6 — Element Extraction...")
        prompt = PASS1_PROMPT.format(report_text=report_text)
        return self._call_json(prompt, PASS1_SYSTEM)

    def pass2_compliance(self, extracted: dict) -> dict:
        """Pass 2: Check compliance against guidelines."""
        self.log("  Pass 2/6 — Compliance Check...")
        prompt = PASS2_PROMPT.format(
            extracted_json=safe_json_str(extracted),
            diagnosis_reference=self.refs["diagnosis"],
        )
        return self._call_json(prompt, PASS2_SYSTEM)

    def pass3_macroscopy(self, macroscopy_text: str) -> dict:
        """Pass 3: Evaluate macroscopy description."""
        self.log("  Pass 3/6 — Macroscopy Evaluation...")

        if not macroscopy_text or macroscopy_text.strip() in ("", "(not provided)"):
            return {
                "macroscopy_score": 0,
                "macroscopy_elements": [],
                "gaps": ["Macroscopy section not provided"],
                "strengths": [],
                "recommendations": ["Include complete gross description"],
            }

        prompt = PASS3_PROMPT.format(
            macroscopy_text=macroscopy_text,
            macroscopy_reference=self.refs.get("macroscopy", "Use standard AAPA guidelines."),
        )
        return self._call_json(prompt, PASS3_SYSTEM)

    def pass4_staging(self, extracted: dict) -> dict:
        """Pass 4: Verify TNM staging."""
        self.log("  Pass 4/6 — Staging Verification...")
        prompt = PASS4_PROMPT.format(
            pT=extracted.get("pT") or "not reported",
            pN=extracted.get("pN") or "not reported",
            pM=extracted.get("pM") or "not reported",
            reported_stage=extracted.get("reported_stage_group") or "not reported",
            total_nodes=extracted.get("total_nodes_examined") or "not reported",
            positive_nodes=extracted.get("positive_nodes") or "not reported",
            tumor_deposits=extracted.get("tumor_deposits") or "not reported",
            depth_of_invasion=extracted.get("depth_of_invasion") or "not reported",
            grade=extracted.get("histologic_grade") or "not reported",
            staging_reference=self.refs["staging"],
        )
        return self._call_json(prompt, PASS4_SYSTEM)

    def pass5_crossvalidate(self, p1: dict, p2: dict, p3: dict, p4: dict) -> dict:
        """Pass 5: Cross-validate and score."""
        self.log("  Pass 5/6 — Cross-validation & Scoring...")
        prompt = PASS5_PROMPT.format(
            pass1_json=safe_json_str(p1),
            pass2_json=safe_json_str(p2),
            pass3_json=safe_json_str(p3),
            pass4_json=safe_json_str(p4),
        )
        return self._call_json(prompt, PASS5_SYSTEM)

    def pass6_summary(self, case_no: str, p1: dict, p2: dict,
                      p3: dict, p4: dict, p5: dict) -> str:
        """Pass 6: Generate human-readable summary."""
        self.log("  Pass 6/6 — Summary Report...")
        prompt = PASS6_PROMPT.format(
            case_no=case_no,
            tumor_type=self.tumor_type,
            analysis_date=datetime.now().isoformat(),
            model=self.model,
            pass1_json=safe_json_str(p1),
            pass2_json=safe_json_str(p2),
            pass3_json=safe_json_str(p3),
            pass4_json=safe_json_str(p4),
            pass5_json=safe_json_str(p5),
        )
        return self._call(prompt, PASS6_SYSTEM)

    # ------------------------------------------------------------------
    # FULL PIPELINE
    # ------------------------------------------------------------------

    def analyze(self, report_text: str, macroscopy_text: str = "",
                case_no: str = "unknown") -> Dict[str, Any]:
        """Run full 6-pass analysis pipeline."""
        start = time.time()

        # If macroscopy not separated, it's part of report_text
        if not macroscopy_text:
            macroscopy_text = report_text

        # Run passes
        p1 = self.pass1_extract(report_text)
        p2 = self.pass2_compliance(p1)
        p3 = self.pass3_macroscopy(macroscopy_text)
        p4 = self.pass4_staging(p1)
        p5 = self.pass5_crossvalidate(p1, p2, p3, p4)
        p6 = self.pass6_summary(case_no, p1, p2, p3, p4, p5)

        elapsed = time.time() - start
        self.log(f"  Done ({elapsed:.0f}s total)")

        return {
            "case_no": case_no,
            "elapsed_seconds": elapsed,
            "pass1_extraction": p1,
            "pass2_compliance": p2,
            "pass3_macroscopy": p3,
            "pass4_staging": p4,
            "pass5_scores": p5,
            "summary_report": p6,
        }


# ============================================================================
# BATCH PROCESSING (EXCEL)
# ============================================================================

def run_batch(analyzer: MultiPassAnalyzer, excel_path: str,
              output_dir: str, save_intermediates: bool = False):
    """Process all reports from an Excel file."""
    import openpyxl

    output = Path(output_dir)
    reports_dir = output / "individual_reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    if save_intermediates:
        json_dir = output / "intermediates"
        json_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading references from {analyzer.skill_dir}...")
    for key, val in analyzer.refs.items():
        print(f"  {key}: {len(val)} chars")

    print(f"\nReading {excel_path}...")
    wb = openpyxl.load_workbook(excel_path, read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    total = len(rows)
    print(f"Found {total} reports to process.\n")

    results = []
    start_time = time.time()

    for i, row in enumerate(rows, 1):
        case_no = str(row[0] or f"case_{i:03d}")
        diagnosis = str(row[1] or "")
        macroscopy_text = str(row[2] or "")
        microscopy = str(row[3] or "") if len(row) > 3 and row[3] else ""

        # Build full report text (diagnosis + microscopy)
        report_parts = []
        if diagnosis:
            report_parts.append(f"PATHOLOGIC DIAGNOSIS:\n{diagnosis}")
        if macroscopy_text:
            report_parts.append(f"MACROSCOPY:\n{macroscopy_text}")
        if microscopy:
            report_parts.append(f"MICROSCOPY:\n{microscopy}")
        report_text = "\n\n".join(report_parts)

        print(f"[{i}/{total}] Processing {case_no}...", flush=True)
        t0 = time.time()

        try:
            result = analyzer.analyze(
                report_text=report_text,
                macroscopy_text=macroscopy_text,
                case_no=case_no,
            )
            elapsed = time.time() - t0
            print(f"  ✓ {case_no} complete ({elapsed:.0f}s)")

            # Save human-readable report
            report_path = reports_dir / f"{case_no}_qa.md"
            header = (
                f"# QA Report: {case_no}\n"
                f"- Analyzed: {datetime.now().isoformat()}\n"
                f"- Model: {analyzer.model}\n"
                f"- Method: Multi-pass (6 passes)\n"
                f"- Elapsed: {elapsed:.0f}s\n\n---\n\n"
            )
            report_path.write_text(header + result["summary_report"], encoding="utf-8")

            # Save intermediates if requested
            if save_intermediates:
                json_path = json_dir / f"{case_no}_intermediates.json"
                # Remove summary_report from JSON (it's text)
                intermediate_data = {k: v for k, v in result.items() if k != "summary_report"}
                json_path.write_text(safe_json_str(intermediate_data), encoding="utf-8")

            # Extract score for summary
            overall_score = None
            try:
                overall_score = result["pass5_scores"]["scores"]["overall_score"]
            except (KeyError, TypeError):
                pass

            results.append({
                "case_no": case_no,
                "status": "OK",
                "elapsed": elapsed,
                "score": overall_score,
            })

        except Exception as e:
            elapsed = time.time() - t0
            print(f"  ✗ {case_no} ERROR ({elapsed:.0f}s): {e}")

            report_path = reports_dir / f"{case_no}_qa.md"
            report_path.write_text(
                f"# QA Report: {case_no}\n\nERROR: {e}\n",
                encoding="utf-8"
            )
            results.append({
                "case_no": case_no,
                "status": f"ERROR: {e}",
                "elapsed": elapsed,
                "score": None,
            })

    # Summary report
    total_time = time.time() - start_time
    ok_count = sum(1 for r in results if r["status"] == "OK")
    err_count = total - ok_count
    scores = [r["score"] for r in results if r["score"] is not None]
    avg_score = sum(scores) / len(scores) if scores else 0

    summary = (
        f"# Batch Processing Summary\n\n"
        f"- Date: {datetime.now().isoformat()}\n"
        f"- Model: {analyzer.model}\n"
        f"- Method: Multi-pass (6 passes per report)\n"
        f"- Tumor type: {analyzer.tumor_type}\n"
        f"- Total reports: {total}\n"
        f"- Successful: {ok_count}\n"
        f"- Errors: {err_count}\n"
        f"- Total time: {total_time / 60:.1f} minutes\n"
        f"- Average time per report: {total_time / total:.0f}s\n"
        f"- Average compliance score: {avg_score:.1f}/100\n\n"
        f"## Per-Report Results\n\n"
        f"| Case | Status | Score | Time (s) |\n"
        f"|------|--------|-------|----------|\n"
    )
    for r in results:
        score_str = f"{r['score']:.0f}" if r["score"] is not None else "N/A"
        summary += f"| {r['case_no']} | {r['status']} | {score_str} | {r['elapsed']:.0f} |\n"

    summary_path = output / "summary_report.md"
    summary_path.write_text(summary, encoding="utf-8")

    print(f"\n{'='*50}")
    print(f"Done! {ok_count}/{total} reports processed successfully.")
    print(f"Average score: {avg_score:.1f}/100")
    print(f"Total time: {total_time / 60:.1f} minutes")
    print(f"Results saved to: {output}")


# ============================================================================
# MODEL DISCOVERY
# ============================================================================

def list_models(provider: str, base_url: str) -> List[str]:
    """List available models from provider."""
    if provider == "ollama":
        import requests
        try:
            resp = requests.get(f"{base_url}/api/tags", timeout=10)
            resp.raise_for_status()
            return [m["name"] for m in resp.json().get("models", [])]
        except Exception as e:
            print(f"Error listing models: {e}", file=sys.stderr)
            return []
    elif provider == "lmstudio":
        try:
            from openai import OpenAI
            client = OpenAI(base_url=base_url, api_key="not-needed")
            return [m.id for m in client.models.list().data]
        except Exception as e:
            print(f"Error listing models: {e}", file=sys.stderr)
            return []
    return []


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Multi-pass pathology report compliance checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single report
  python check_report_multipass.py -p ollama -f report.txt
  python check_report_multipass.py -p ollama -m mistral:latest -t colorectal -f report.txt

  # Batch from Excel
  python check_report_multipass.py -p ollama --batch data.xlsx --output-dir results/

  # Save intermediate JSON for debugging
  python check_report_multipass.py -p ollama --save-intermediates -f report.txt

  # List models
  python check_report_multipass.py -p ollama --list-models
"""
    )

    parser.add_argument("--file", "-f", type=str, help="Path to single report file")
    parser.add_argument("--batch", "-b", type=str, help="Path to Excel file for batch processing")
    parser.add_argument("--output-dir", "-o", type=str, default="./results", help="Output directory (batch mode)")
    parser.add_argument("--provider", "-p", type=str, default=os.environ.get("LLM_PROVIDER", "ollama"),
                        choices=["anthropic", "ollama", "lmstudio"])
    parser.add_argument("--model", "-m", type=str, default=os.environ.get("OLLAMA_MODEL"))
    parser.add_argument("--tumor-type", "-t", type=str, default="colorectal",
                        choices=["breast", "colorectal", "pancreas", "gastric"])
    parser.add_argument("--ollama-url", type=str, default=os.environ.get("OLLAMA_URL", DEFAULT_OLLAMA_URL))
    parser.add_argument("--lmstudio-url", type=str, default=os.environ.get("LMSTUDIO_URL", DEFAULT_LMSTUDIO_URL))
    parser.add_argument("--skill-dir", type=str, default=os.environ.get("SKILL_DIR"))
    parser.add_argument("--save-intermediates", action="store_true", help="Save intermediate JSON from each pass")
    parser.add_argument("--list-models", action="store_true", help="List available models and exit")
    parser.add_argument("--quiet", "-q", action="store_true")
    parser.add_argument("--json", "-j", action="store_true", help="Output all passes as JSON (single mode)")

    args = parser.parse_args()

    # Handle --list-models
    if args.list_models:
        base_url = args.lmstudio_url if args.provider == "lmstudio" else args.ollama_url
        models = list_models(args.provider, base_url)
        if models:
            print(f"Available models ({args.provider}):")
            for m in models:
                print(f"  {m}")
        else:
            print(f"No models found. Is {args.provider} running?", file=sys.stderr)
        sys.exit(0)

    # Resolve model
    model = args.model
    if not model:
        if args.provider == "anthropic":
            model = DEFAULT_ANTHROPIC_MODEL
        elif args.provider == "ollama":
            model = DEFAULT_OLLAMA_MODEL
        else:
            models = list_models(args.provider, args.lmstudio_url)
            model = models[0] if models else "default"

    # Resolve base URL
    base_url = ""
    if args.provider == "ollama":
        base_url = args.ollama_url
    elif args.provider == "lmstudio":
        base_url = args.lmstudio_url

    # Resolve skill dir
    skill_dir = Path(args.skill_dir) if args.skill_dir else get_skill_dir()

    # Create analyzer
    analyzer = MultiPassAnalyzer(
        provider=args.provider,
        model=model,
        base_url=base_url,
        skill_dir=skill_dir,
        tumor_type=args.tumor_type,
        quiet=args.quiet,
        save_intermediates=args.save_intermediates,
    )

    # Batch mode
    if args.batch:
        run_batch(analyzer, args.batch, args.output_dir, args.save_intermediates)
        return

    # Single report mode
    if args.file:
        report_text = Path(args.file).read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        report_text = sys.stdin.read()
    else:
        print("Error: Provide --file, --batch, or pipe via stdin.", file=sys.stderr)
        sys.exit(1)

    if not report_text.strip():
        print("Error: Empty report.", file=sys.stderr)
        sys.exit(1)

    try:
        result = analyzer.analyze(
            report_text=report_text,
            case_no=Path(args.file).stem if args.file else "stdin",
        )

        if args.json:
            # Output all intermediates as JSON
            output_data = {k: v for k, v in result.items() if k != "summary_report"}
            output_data["summary_report"] = result["summary_report"]
            print(json.dumps(output_data, indent=2, ensure_ascii=False))
        else:
            print(result["summary_report"])

        # Save intermediates if requested
        if args.save_intermediates:
            out_dir = Path(args.output_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
            json_path = out_dir / f"{result['case_no']}_intermediates.json"
            intermediate_data = {k: v for k, v in result.items() if k != "summary_report"}
            json_path.write_text(safe_json_str(intermediate_data), encoding="utf-8")
            print(f"\nIntermediates saved to: {json_path}", file=sys.stderr)

    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
