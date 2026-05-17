#!/usr/bin/env python3
"""
Multi-Pass Pathology Report Checker (v3 — optimized for small local LLMs)

Pipeline:
  Pass 1 — Element Extraction    (report → structured JSON)
  Pass 2 — Compliance Check      (extracted JSON → gaps)
  Pass 3 — Macroscopy Evaluation  (macroscopy text → assessment)
  Pass 4 — Staging Verification   (pT/pN/M → stage check)
  Pass 5 — Cross-validation       (all JSONs → consistency + score)
  Pass 6 — Summary Report         (all JSONs → human-readable report)

Key design: Each pass gets ONLY inline checklist items — no large reference
files stuffed into context. This keeps prompts under 2K tokens, leaving room
for the model to reason and respond within a small context window.

Usage:
    python check_report_multipass.py -p ollama -f report.txt
    python check_report_multipass.py -p ollama --batch data.xlsx -o results/
    python check_report_multipass.py -p ollama -m llama3.1:8b -t colorectal -f report.txt
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
DEFAULT_OLLAMA_MODEL = "llama3.2:latest"   # 3B fits fully on 4GB GPU
DEFAULT_OLLAMA_URL = "http://localhost:11434"
DEFAULT_LMSTUDIO_URL = "http://localhost:1234/v1"

# Per-pass Ollama settings (context + max output tokens)
# Small context = faster inference + more model on GPU
PASS_CONFIG = {
    "pass1": {"num_ctx": 8192, "num_predict": 1500},  # Needs room for report text
    "pass2": {"num_ctx": 4096, "num_predict": 1500},  # JSON in, JSON out
    "pass3": {"num_ctx": 4096, "num_predict": 1024},  # Macroscopy only
    "pass4": {"num_ctx": 2048, "num_predict": 1024},  # Tiny — just staging values
    "pass5": {"num_ctx": 6144, "num_predict": 1500},  # Receives all prior JSONs
    "pass6": {"num_ctx": 6144, "num_predict": 2048},  # Readable report output
}


# ============================================================================
# LLM CALLING
# ============================================================================

def call_ollama_native(prompt: str, model: str, base_url: str,
                       system: str = "", num_ctx: int = 4096,
                       num_predict: int = 1500) -> str:
    """Call Ollama native /api/chat."""
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
            "options": {"num_ctx": num_ctx, "num_predict": num_predict},
        },
        timeout=600,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


def call_openai_compat(prompt: str, model: str, base_url: str,
                       system: str = "", **kwargs) -> str:
    """Call OpenAI-compatible API (LM Studio)."""
    from openai import OpenAI
    client = OpenAI(base_url=base_url, api_key="not-needed")
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=model, max_tokens=kwargs.get("num_predict", 2048), messages=messages,
    )
    return response.choices[0].message.content


def call_anthropic_api(prompt: str, model: str, system: str = "", **kwargs) -> str:
    """Call Anthropic API."""
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    kw = {"model": model, "max_tokens": 4096,
          "messages": [{"role": "user", "content": prompt}]}
    if system:
        kw["system"] = system
    return client.messages.create(**kw).content[0].text


def call_llm(prompt: str, provider: str, model: str, base_url: str = "",
             system: str = "", pass_name: str = "") -> str:
    """Unified LLM caller with per-pass config."""
    cfg = PASS_CONFIG.get(pass_name, {"num_ctx": 4096, "num_predict": 1500})

    if provider == "ollama":
        return call_ollama_native(prompt, model, base_url or DEFAULT_OLLAMA_URL,
                                  system, cfg["num_ctx"], cfg["num_predict"])
    elif provider == "lmstudio":
        return call_openai_compat(prompt, model, base_url or DEFAULT_LMSTUDIO_URL,
                                  system, **cfg)
    elif provider == "anthropic":
        return call_anthropic_api(prompt, model or DEFAULT_ANTHROPIC_MODEL, system)
    else:
        raise ValueError(f"Unknown provider: {provider}")


# ============================================================================
# JSON PARSING
# ============================================================================

def extract_json(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown fences."""
    # Direct parse
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # From code fences
    for pattern in [r'```json\s*\n(.*?)\n\s*```', r'```\s*\n(.*?)\n\s*```']:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue

    # First { to last }
    start, end = text.find('{'), text.rfind('}')
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    return {"_raw": text, "_error": "JSON parse failed"}


def jstr(data: dict) -> str:
    """Compact JSON string — saves tokens when passing between passes."""
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))


def jstr_pretty(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


# ============================================================================
# TUMOR-TYPE SPECIFIC CHECKLISTS (inline, no file loading needed)
# ============================================================================

CHECKLISTS = {
    "colorectal": {
        "extraction_fields": """SPECIMEN: specimen_type, laterality
TUMOR: tumor_site, tumor_size_cm, histologic_type, histologic_grade, depth_of_invasion
STAGING: pT (pTis/1/2/3/4a/4b), pN (pN0/1a/1b/1c/2a/2b), pM, reported_stage_group
NODES: total_nodes_examined, positive_nodes, tumor_deposits
MARGINS: proximal_margin, distal_margin, radial_margin, margin_status_overall (R0/R1/R2)
FEATURES: lymphovascular_invasion, perineural_invasion, tumor_budding
MOLECULAR: mismatch_repair, microsatellite_instability, kras_braf_status
OTHER: treatment_effect, additional_findings""",

        "required_elements": """CRITICAL (must have): histologic_type, histologic_grade, pT, pN, margins, depth_of_invasion
MAJOR (CAP required): LVI, PNI, tumor_deposits, total_nodes_examined, tumor_budding, mismatch_repair
MINOR (recommended): tumor_size_cm, specimen_type, microsatellite_instability, radial_margin""",

        "macroscopy_checklist": """1. Specimen type and dimensions
2. Tumor location and distance from margins
3. Tumor size (3 dimensions)
4. Tumor appearance (polypoid/ulcerated/annular)
5. Depth of penetration (gross)
6. Serosal involvement
7. Margin descriptions (proximal, distal, radial)
8. Lymph node count from gross
9. Other lesions (polyps, diverticula)
10. Background mucosa""",

        "staging_rules": """AJCC 8th Colorectal:
pT1=submucosa, pT2=muscularis, pT3=pericolorectal, pT4a=serosa, pT4b=adjacent organs
pN1a=1 node, pN1b=2-3 nodes, pN1c=tumor deposits only, pN2a=4-6 nodes, pN2b=7+ nodes
Stage I: T1-2 N0, Stage IIA: T3 N0, Stage IIB: T4a N0, Stage IIC: T4b N0
Stage IIIA: T1-2 N1 or T1 N2a, Stage IIIB: T3-4a N1 or T2-3 N2a or T1-2 N2b
Stage IIIC: T4a N2a or T3-4a N2b or T4b N1-2, Stage IV: any T any N M1
Minimum 12 nodes for adequate staging.""",
    },

    "breast": {
        "extraction_fields": """SPECIMEN: specimen_type (lumpectomy/mastectomy), laterality (left/right)
TUMOR: tumor_site, tumor_size_cm, histologic_type, histologic_grade (Nottingham 1-3), tubule_score, nuclear_score, mitotic_score
STAGING: pT (pTis/1mi/1a/1b/1c/2/3/4a-d), pN (pN0/0i+/1mi/1a/1b/1c/2a/2b/3a), pM
NODES: total_nodes_examined, positive_nodes, sentinel_nodes_examined, sentinel_nodes_positive, extranodal_extension
MARGINS: closest_margin_mm, margin_status (negative/positive/close), specific_margins
FEATURES: lymphovascular_invasion, perineural_invasion, DCIS_component, DCIS_size, DCIS_grade, DCIS_necrosis
BIOMARKERS: ER_status, ER_percent, PR_status, PR_percent, HER2_status, HER2_method, Ki67_percent
MOLECULAR: oncotype_score, mammaprint
OTHER: skin_involvement, nipple_involvement, treatment_effect (RCB/Miller-Payne), additional_findings""",

        "required_elements": """CRITICAL: histologic_type, histologic_grade, pT, pN, margins, ER, PR, HER2
MAJOR: LVI, tumor_size, total_nodes_examined, extranodal_extension, DCIS_component, Ki67
MINOR: PNI, tubule/nuclear/mitotic scores, specimen_type""",

        "macroscopy_checklist": """1. Specimen type, laterality, orientation
2. Specimen dimensions and weight
3. Tumor location (quadrant/clock position)
4. Tumor size (3 dimensions)
5. Tumor appearance and consistency
6. Distance to margins (superior, inferior, medial, lateral, anterior, posterior)
7. Skin/nipple involvement
8. Lymph node description
9. Additional lesions
10. Inking protocol""",

        "staging_rules": """AJCC 8th Breast:
pT1mi≤1mm, pT1a>1-5mm, pT1b>5-10mm, pT1c>10-20mm, pT2>20-50mm, pT3>50mm, pT4=chest wall/skin
pN0=no nodes, pN0(i+)=ITC, pN1mi=micromet>0.2-2mm, pN1a=1-3 nodes, pN1b=internal mammary
pN2a=4-9 nodes, pN3a=10+ nodes
Stage IA: T1 N0, Stage IB: T0-1 N1mi, Stage IIA: T0-1 N1 or T2 N0
Stage IIB: T2 N1 or T3 N0, Stage IIIA: T0-2 N2 or T3 N1-2
Stage IIIB: T4 N0-2, Stage IIIC: any T N3""",
    },

    "gastric": {
        "extraction_fields": """SPECIMEN: specimen_type, tumor_site (cardia/fundus/body/antrum/pylorus)
TUMOR: tumor_size_cm, histologic_type (Lauren: intestinal/diffuse/mixed), histologic_grade, depth_of_invasion
STAGING: pT (pT1a/1b/2/3/4a/4b), pN (pN0/1/2/3a/3b), pM
NODES: total_nodes_examined, positive_nodes
MARGINS: proximal_margin, distal_margin, radial_margin
FEATURES: lymphovascular_invasion, perineural_invasion
MOLECULAR: HER2_status, MSI_status, PD_L1
OTHER: treatment_effect, additional_findings (intestinal metaplasia, H.pylori)""",

        "required_elements": """CRITICAL: histologic_type, histologic_grade, pT, pN, margins, depth_of_invasion
MAJOR: LVI, PNI, total_nodes_examined (minimum 16), HER2
MINOR: tumor_size, Lauren classification, MSI, PD-L1""",

        "macroscopy_checklist": """1. Specimen type and dimensions
2. Tumor location and size (3D)
3. Tumor appearance (Borrmann type)
4. Depth of penetration
5. Distance to margins
6. Serosal involvement
7. Lymph node count
8. Other lesions""",

        "staging_rules": """AJCC 8th Gastric:
pT1a=lamina propria/muscularis mucosae, pT1b=submucosa, pT2=muscularis propria
pT3=subserosa, pT4a=serosa, pT4b=adjacent structures
pN1=1-2 nodes, pN2=3-6, pN3a=7-15, pN3b=16+
Minimum 16 nodes recommended.""",
    },

    "pancreas": {
        "extraction_fields": """SPECIMEN: specimen_type (Whipple/distal), tumor_site (head/body/tail)
TUMOR: tumor_size_cm, histologic_type, histologic_grade (well/moderate/poor), depth_of_invasion
STAGING: pT (pT1a/1b/1c/2/3/4), pN (pN0/1/2), pM
NODES: total_nodes_examined, positive_nodes
MARGINS: pancreatic_neck_margin, uncinate_margin, bile_duct_margin, anterior_surface, posterior_margin
FEATURES: lymphovascular_invasion, perineural_invasion
OTHER: treatment_effect, additional_findings (PanIN, IPMN)""",

        "required_elements": """CRITICAL: histologic_type, histologic_grade, pT, pN, all margins (especially uncinate/SMA)
MAJOR: LVI, PNI, total_nodes_examined (minimum 12)
MINOR: tumor_size, anterior surface status""",

        "macroscopy_checklist": """1. Specimen type and components
2. Tumor location and size
3. Relationship to ducts and vessels
4. All margin distances
5. Lymph node count
6. Pancreatic parenchyma""",

        "staging_rules": """AJCC 8th Pancreas:
pT1a≤0.5cm, pT1b>0.5-1cm, pT1c>1-2cm, pT2>2-4cm, pT3>4cm, pT4=celiac axis/SMA/hepatic
pN1=1-3 nodes, pN2=4+ nodes""",
    },
}


# ============================================================================
# PASS PROMPTS — lean, no reference file injection
# ============================================================================

PASS1_SYSTEM = "You are a pathology data extractor. Output ONLY valid JSON."

PASS1_PROMPT = """Extract structured data from this pathology report.

Fields to extract (use null if not found):
{extraction_fields}

REPORT:
{report_text}

Return ONLY a JSON object. No commentary."""


PASS2_SYSTEM = "You are a pathology compliance checker. Output ONLY valid JSON."

PASS2_PROMPT = """Given these extracted elements from a pathology report, identify what is missing or incomplete.

EXTRACTED:
{extracted_json}

REQUIRED ELEMENTS:
{required_elements}

For each required element, check if present, missing, or incomplete.

Return JSON:
{{"elements": [{{"name":"...","status":"present|missing|incomplete","severity":"critical|major|minor","note":"..."}}], "critical_missing":[], "major_missing":[], "minor_missing":[], "total_required":0, "total_present":0, "compliance_pct":0}}"""


PASS3_SYSTEM = "You are a pathology macroscopy evaluator. Output ONLY valid JSON."

PASS3_PROMPT = """Evaluate this gross/macroscopic description for completeness.

MACROSCOPY TEXT:
{macroscopy_text}

REQUIRED ELEMENTS:
{macroscopy_checklist}

Return JSON:
{{"elements":[{{"name":"...","status":"present|missing|incomplete","note":"..."}}],"score":0,"gaps":[],"strengths":[]}}"""


PASS4_SYSTEM = "You are a TNM staging calculator. Output ONLY valid JSON."

PASS4_PROMPT = """Verify TNM staging for this case.

pT={pT}, pN={pN}, pM={pM}
Reported stage: {reported_stage}
Nodes examined: {total_nodes}, Positive: {positive_nodes}
Tumor deposits: {tumor_deposits}
Depth: {depth_of_invasion}

STAGING RULES:
{staging_rules}

Check: 1) pT matches depth? 2) pN matches node count? 3) Calculate stage group. 4) Matches reported? 5) ≥12 nodes?

Return JSON:
{{"reported_stage":"{reported_stage}","calculated_stage":"...","match":true,"pT_ok":true,"pN_ok":true,"nodes_adequate":true,"issues":[]}}"""


PASS5_SYSTEM = "You are a pathology QA scorer. Output ONLY valid JSON."

PASS5_PROMPT = """Score this pathology report based on all analysis results.

EXTRACTION: {p1}
COMPLIANCE: {p2}
MACROSCOPY: {p3}
STAGING: {p4}

Cross-check: pT vs depth, pN vs node count, margins vs R status, macro vs micro agreement.

Compute scores (0-100): diagnosis_completeness, macroscopy_completeness, staging_accuracy, internal_consistency.
Overall = diagnosis*0.4 + macroscopy*0.15 + staging*0.25 + consistency*0.2

Return JSON:
{{"checks":[{{"name":"...","result":"pass|fail|warning","note":"..."}}],"scores":{{"diagnosis":0,"macroscopy":0,"staging":0,"consistency":0,"overall":0}},"status":"Excellent|Good|Needs Improvement|Significant Gaps","critical_issues":[],"recommendations":[]}}"""


PASS6_SYSTEM = "You are a pathology QA reporter. Write a clear, actionable report. Use same language as the original report."

PASS6_PROMPT = """Write a QA report from these analysis results.

Case: {case_no} | Type: {tumor_type} | Model: {model}

EXTRACTED DATA: {p1}
COMPLIANCE: {p2}
MACROSCOPY: {p3}
STAGING: {p4}
SCORES: {p5}

Write sections:
1. OVERALL — score and one-line verdict
2. KEY FINDINGS — what was correctly reported
3. MISSING ELEMENTS — by severity
4. STAGING — reported vs calculated
5. MACROSCOPY — completeness
6. RECOMMENDATIONS — prioritized action items

Be concise. No JSON."""


# ============================================================================
# MULTI-PASS ANALYZER
# ============================================================================

class MultiPassAnalyzer:

    def __init__(self, provider: str, model: str, base_url: str = "",
                 tumor_type: str = "colorectal", quiet: bool = False):
        self.provider = provider
        self.model = model
        self.base_url = base_url
        self.tumor_type = tumor_type
        self.quiet = quiet
        self.checklist = CHECKLISTS.get(tumor_type, CHECKLISTS["colorectal"])

    def log(self, msg: str):
        if not self.quiet:
            print(msg, file=sys.stderr, flush=True)

    def _call(self, prompt: str, system: str, pass_name: str) -> str:
        return call_llm(prompt, self.provider, self.model,
                        self.base_url, system, pass_name)

    def _call_json(self, prompt: str, system: str, pass_name: str) -> dict:
        raw = self._call(prompt, system, pass_name)
        result = extract_json(raw)
        if "_error" in result:
            self.log(f"  ↳ JSON retry...")
            raw = self._call(
                prompt + "\n\nRETURN ONLY VALID JSON. Nothing else.",
                system, pass_name
            )
            result = extract_json(raw)
        return result

    def pass1_extract(self, report_text: str) -> dict:
        self.log("  Pass 1/6 — Element Extraction...")
        t = time.time()
        result = self._call_json(
            PASS1_PROMPT.format(
                extraction_fields=self.checklist["extraction_fields"],
                report_text=report_text,
            ),
            PASS1_SYSTEM, "pass1"
        )
        self.log(f"           ({time.time()-t:.0f}s)")
        return result

    def pass2_compliance(self, extracted: dict) -> dict:
        self.log("  Pass 2/6 — Compliance Check...")
        t = time.time()
        result = self._call_json(
            PASS2_PROMPT.format(
                extracted_json=jstr(extracted),
                required_elements=self.checklist["required_elements"],
            ),
            PASS2_SYSTEM, "pass2"
        )
        self.log(f"           ({time.time()-t:.0f}s)")
        return result

    def pass3_macroscopy(self, macroscopy_text: str) -> dict:
        self.log("  Pass 3/6 — Macroscopy...")
        t = time.time()
        if not macroscopy_text or macroscopy_text.strip() in ("", "(not provided)"):
            self.log(f"           (skipped — no macroscopy)")
            return {"score": 0, "elements": [], "gaps": ["No macroscopy provided"],
                    "strengths": []}

        result = self._call_json(
            PASS3_PROMPT.format(
                macroscopy_text=macroscopy_text,
                macroscopy_checklist=self.checklist["macroscopy_checklist"],
            ),
            PASS3_SYSTEM, "pass3"
        )
        self.log(f"           ({time.time()-t:.0f}s)")
        return result

    def pass4_staging(self, extracted: dict) -> dict:
        self.log("  Pass 4/6 — Staging...")
        t = time.time()
        result = self._call_json(
            PASS4_PROMPT.format(
                pT=extracted.get("pT") or "not reported",
                pN=extracted.get("pN") or "not reported",
                pM=extracted.get("pM") or "not reported",
                reported_stage=extracted.get("reported_stage_group") or "not reported",
                total_nodes=extracted.get("total_nodes_examined") or "not reported",
                positive_nodes=extracted.get("positive_nodes") or "not reported",
                tumor_deposits=extracted.get("tumor_deposits") or "not reported",
                depth_of_invasion=extracted.get("depth_of_invasion") or "not reported",
                staging_rules=self.checklist["staging_rules"],
            ),
            PASS4_SYSTEM, "pass4"
        )
        self.log(f"           ({time.time()-t:.0f}s)")
        return result

    def pass5_score(self, p1: dict, p2: dict, p3: dict, p4: dict) -> dict:
        self.log("  Pass 5/6 — Scoring...")
        t = time.time()
        result = self._call_json(
            PASS5_PROMPT.format(p1=jstr(p1), p2=jstr(p2), p3=jstr(p3), p4=jstr(p4)),
            PASS5_SYSTEM, "pass5"
        )
        self.log(f"           ({time.time()-t:.0f}s)")
        return result

    def pass6_summary(self, case_no: str, p1: dict, p2: dict,
                      p3: dict, p4: dict, p5: dict) -> str:
        self.log("  Pass 6/6 — Summary...")
        t = time.time()
        result = self._call(
            PASS6_PROMPT.format(
                case_no=case_no, tumor_type=self.tumor_type, model=self.model,
                p1=jstr(p1), p2=jstr(p2), p3=jstr(p3), p4=jstr(p4), p5=jstr(p5),
            ),
            PASS6_SYSTEM, "pass6"
        )
        self.log(f"           ({time.time()-t:.0f}s)")
        return result

    def analyze(self, report_text: str, macroscopy_text: str = "",
                case_no: str = "unknown") -> Dict[str, Any]:
        start = time.time()
        if not macroscopy_text:
            macroscopy_text = report_text

        p1 = self.pass1_extract(report_text)
        p2 = self.pass2_compliance(p1)
        p3 = self.pass3_macroscopy(macroscopy_text)
        p4 = self.pass4_staging(p1)
        p5 = self.pass5_score(p1, p2, p3, p4)
        p6 = self.pass6_summary(case_no, p1, p2, p3, p4, p5)

        elapsed = time.time() - start
        self.log(f"  Total: {elapsed:.0f}s ({elapsed/60:.1f} min)")

        return {
            "case_no": case_no,
            "elapsed": elapsed,
            "pass1_extraction": p1,
            "pass2_compliance": p2,
            "pass3_macroscopy": p3,
            "pass4_staging": p4,
            "pass5_scores": p5,
            "summary_report": p6,
        }


# ============================================================================
# OUTPUT HELPERS
# ============================================================================

def save_result(result: dict, output_dir: Path, save_intermediates: bool = False):
    """Save QA report and optionally intermediate JSONs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    case = result["case_no"]

    # Human-readable report
    report_path = output_dir / f"{case}_qa.md"
    header = (
        f"# QA Report: {case}\n"
        f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"- Method: Multi-pass (6 passes)\n"
        f"- Time: {result['elapsed']:.0f}s\n\n---\n\n"
    )
    report_path.write_text(header + result["summary_report"], encoding="utf-8")

    # Intermediates
    if save_intermediates:
        int_path = output_dir / f"{case}_intermediates.json"
        data = {k: v for k, v in result.items() if k != "summary_report"}
        int_path.write_text(jstr_pretty(data), encoding="utf-8")

    return report_path


# ============================================================================
# BATCH PROCESSING
# ============================================================================

def run_batch(analyzer: MultiPassAnalyzer, excel_path: str,
              output_dir: str, save_intermediates: bool = False):
    import openpyxl

    output = Path(output_dir)
    reports_dir = output / "individual_reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    print(f"Reading {excel_path}...")
    wb = openpyxl.load_workbook(excel_path, read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    total = len(rows)
    print(f"Found {total} reports.\n")

    results = []
    start_time = time.time()

    for i, row in enumerate(rows, 1):
        case_no = str(row[0] or f"case_{i:03d}")
        diagnosis = str(row[1] or "")
        macroscopy = str(row[2] or "")
        microscopy = str(row[3] or "") if len(row) > 3 and row[3] else ""

        parts = []
        if diagnosis:
            parts.append(f"DIAGNOSIS:\n{diagnosis}")
        if macroscopy:
            parts.append(f"MACROSCOPY:\n{macroscopy}")
        if microscopy:
            parts.append(f"MICROSCOPY:\n{microscopy}")
        report_text = "\n\n".join(parts)

        print(f"[{i}/{total}] {case_no}")

        try:
            result = analyzer.analyze(report_text, macroscopy, case_no)
            save_result(result, reports_dir, save_intermediates)

            score = None
            try:
                score = result["pass5_scores"]["scores"]["overall"]
            except (KeyError, TypeError):
                pass

            results.append({"case": case_no, "status": "OK",
                            "time": result["elapsed"], "score": score})
            print(f"  ✓ {result['elapsed']:.0f}s | score={score}")

        except Exception as e:
            results.append({"case": case_no, "status": f"ERROR: {e}",
                            "time": 0, "score": None})
            print(f"  ✗ {e}")

    # Summary
    total_time = time.time() - start_time
    ok = sum(1 for r in results if r["status"] == "OK")
    scores = [r["score"] for r in results if r["score"] is not None]
    avg = sum(scores) / len(scores) if scores else 0

    summary = (
        f"# Batch Summary\n\n"
        f"- Date: {datetime.now().isoformat()}\n"
        f"- Model: {analyzer.model}\n"
        f"- Reports: {ok}/{total} OK\n"
        f"- Time: {total_time/60:.1f} min (avg {total_time/total:.0f}s/report)\n"
        f"- Avg score: {avg:.0f}/100\n\n"
        f"| Case | Status | Score | Time |\n|------|--------|-------|------|\n"
    )
    for r in results:
        s = f"{r['score']:.0f}" if r["score"] is not None else "N/A"
        summary += f"| {r['case']} | {r['status']} | {s} | {r['time']:.0f}s |\n"

    (output / "summary.md").write_text(summary, encoding="utf-8")
    print(f"\nDone! {ok}/{total} OK | Avg score: {avg:.0f} | {total_time/60:.1f} min")
    print(f"Results: {output}")


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Multi-pass pathology report QA checker")
    parser.add_argument("--file", "-f", type=str, help="Single report file")
    parser.add_argument("--batch", "-b", type=str, help="Excel file for batch")
    parser.add_argument("--output-dir", "-o", type=str, default="./results")
    parser.add_argument("--provider", "-p", type=str, default="ollama",
                        choices=["anthropic", "ollama", "lmstudio"])
    parser.add_argument("--model", "-m", type=str)
    parser.add_argument("--tumor-type", "-t", type=str, default="colorectal",
                        choices=["breast", "colorectal", "pancreas", "gastric"])
    parser.add_argument("--ollama-url", type=str, default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--lmstudio-url", type=str, default=DEFAULT_LMSTUDIO_URL)
    parser.add_argument("--save-intermediates", action="store_true")
    parser.add_argument("--quiet", "-q", action="store_true")
    parser.add_argument("--list-models", action="store_true")

    args = parser.parse_args()

    if args.list_models:
        import requests
        try:
            r = requests.get(f"{args.ollama_url}/api/tags", timeout=5)
            for m in r.json().get("models", []):
                print(f"  {m['name']}")
        except Exception as e:
            print(f"Error: {e}")
        sys.exit(0)

    # Resolve model
    model = args.model
    if not model:
        if args.provider == "anthropic":
            model = DEFAULT_ANTHROPIC_MODEL
        else:
            model = DEFAULT_OLLAMA_MODEL

    base_url = args.ollama_url if args.provider == "ollama" else args.lmstudio_url

    analyzer = MultiPassAnalyzer(
        provider=args.provider, model=model, base_url=base_url,
        tumor_type=args.tumor_type, quiet=args.quiet,
    )

    # Batch mode
    if args.batch:
        run_batch(analyzer, args.batch, args.output_dir, args.save_intermediates)
        return

    # Single report mode
    if args.file:
        report_text = Path(args.file).read_text(encoding="utf-8")
        case_name = Path(args.file).stem
    elif not sys.stdin.isatty():
        report_text = sys.stdin.read()
        case_name = "stdin"
    else:
        print("Error: provide --file, --batch, or pipe stdin", file=sys.stderr)
        sys.exit(1)

    if not report_text.strip():
        print("Error: empty report", file=sys.stderr)
        sys.exit(1)

    try:
        result = analyzer.analyze(report_text, case_no=case_name)

        # Always save to file
        out_dir = Path(args.output_dir)
        saved = save_result(result, out_dir, args.save_intermediates)
        print(f"\n{'='*50}")
        print(result["summary_report"])
        print(f"\n{'='*50}")
        print(f"Saved to: {saved}")
        if args.save_intermediates:
            print(f"Intermediates: {out_dir / f'{case_name}_intermediates.json'}")

    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
