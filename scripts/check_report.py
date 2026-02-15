#!/usr/bin/env python3
"""
Single Pathology Report Checker

Analyzes a single pathology report against CAP/ICCR guidelines using either
Claude API or a local LLM via Ollama.

Usage:
    # With Claude (default)
    python check_report.py "Check this breast report" < report.txt
    python check_report.py --file report.txt "Check for CAP compliance"

    # With Ollama (local, private)
    python check_report.py --provider ollama "Check this report" < report.txt
    python check_report.py --provider ollama --model llama3.1:70b --file report.txt

    # With LM Studio (local, private)
    python check_report.py --provider lmstudio "Check this report" < report.txt

    # Output to file
    python check_report.py "Check compliance" < report.txt > result.txt

Arguments:
    prompt          The instruction/prompt for analysis
    --file, -f      Path to report file (alternative to stdin)
    --provider, -p  LLM provider: 'anthropic' (default) or 'ollama'
    --model, -m     Model name (default: claude-sonnet-4-20250514 or llama3.1:70b)
    --ollama-url    Ollama API base URL (default: http://localhost:11434/v1)
    --tumor-type    Tumor type hint: breast, colorectal, pancreas, gastric
    --json          Output raw JSON instead of formatted text
    --quiet, -q     Suppress progress messages (only output result)

Environment:
    ANTHROPIC_API_KEY   Required for Claude provider
    LLM_PROVIDER        Default provider (anthropic/ollama)
    OLLAMA_MODEL        Default Ollama model
    OLLAMA_URL          Default Ollama URL
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any


# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
DEFAULT_OLLAMA_MODEL = "llama3.1:70b"
DEFAULT_OLLAMA_URL = "http://localhost:11434/v1"
DEFAULT_LMSTUDIO_URL = "http://localhost:1234/v1"


# ============================================================================
# REFERENCE FILE LOADING
# ============================================================================

def get_skill_dir() -> Path:
    """Get the skill directory (parent of scripts/)."""
    return Path(__file__).parent.parent


def load_skill_file() -> str:
    """Load the main SKILL.md file."""
    skill_path = get_skill_dir() / "SKILL.md"
    if skill_path.exists():
        return skill_path.read_text(encoding="utf-8")
    return ""


def load_reference_file(tumor_type: str) -> str:
    """Load the appropriate reference file for the tumor type."""
    reference_map = {
        "pancreas": "diagnosis/exocrine_pancreas.md",
        "breast": "diagnosis/breast_invasive_carcinoma.md",
        "colorectal": "diagnosis/colorectal_resection.md",
        "gastric": "diagnosis/gastric_carcinoma.md",
        "stomach": "diagnosis/gastric_carcinoma.md",
    }

    filename = reference_map.get(tumor_type.lower() if tumor_type else "")
    if not filename:
        # Load all reference files if tumor type not specified
        refs = []
        ref_dir = get_skill_dir() / "references" / "diagnosis"
        if ref_dir.exists():
            for ref_file in ref_dir.glob("*.md"):
                refs.append(f"# {ref_file.stem}\n\n{ref_file.read_text(encoding='utf-8')}")
        return "\n\n---\n\n".join(refs)

    ref_path = get_skill_dir() / "references" / filename
    if ref_path.exists():
        return ref_path.read_text(encoding="utf-8")
    return ""


def load_staging_reference() -> str:
    """Load the TNM stage calculator reference file."""
    staging_path = get_skill_dir() / "references" / "staging" / "tnm_stage_calculator.md"
    if staging_path.exists():
        return staging_path.read_text(encoding="utf-8")
    return ""


# ============================================================================
# PROMPT TEMPLATE
# ============================================================================

ANALYSIS_PROMPT = """You are a pathology report compliance checker. Analyze the following surgical pathology cancer report against CAP (College of American Pathologists) and ICCR (International Collaboration on Cancer Reporting) guidelines.

<skill_instructions>
{skill_content}
</skill_instructions>

<reference_guidelines>
{reference_content}
</reference_guidelines>

<staging_reference>
{staging_content}
</staging_reference>

<pathology_report>
{report_text}
</pathology_report>

<user_instruction>
{user_prompt}
</user_instruction>

Analyze this report following the user's instruction. Provide a comprehensive response that includes:

1. **Compliance Assessment**: Score (0-100) and status
2. **Missing Elements**: List any critical, major, or minor gaps
3. **Present Elements**: Key findings extracted from the report
4. **Cross-Validation**: Check pT vs size, pN vs node count, margins vs R classification
5. **Staging Verification**: Compare reported stage with calculated stage (AJCC 8th)
6. **Quality Metrics**: Completeness, clarity, consistency scores
7. **Summary**: Brief narrative of findings and recommendations

Respond in the same language as the pathology report (English or Turkish).
"""


# ============================================================================
# LLM CLIENTS
# ============================================================================

def create_anthropic_client():
    """Create Anthropic client."""
    try:
        import anthropic
    except ImportError:
        print("Error: anthropic package not installed.", file=sys.stderr)
        print("Install with: pip install anthropic", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    return anthropic.Anthropic(api_key=api_key)


def create_ollama_client(base_url: str):
    """Create OpenAI-compatible client for Ollama."""
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed.", file=sys.stderr)
        print("Install with: pip install openai", file=sys.stderr)
        sys.exit(1)

    return OpenAI(base_url=base_url, api_key="ollama")


def call_anthropic(client, model: str, prompt: str, quiet: bool = False) -> str:
    """Call Anthropic API."""
    if not quiet:
        print(f"Analyzing with {model}...", file=sys.stderr)

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


def call_ollama(client, model: str, prompt: str, quiet: bool = False) -> str:
    """Call Ollama via OpenAI-compatible API."""
    if not quiet:
        print(f"Analyzing with {model} (local)...", file=sys.stderr)

    response = client.chat.completions.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def analyze_report(
    report_text: str,
    user_prompt: str,
    provider: str = "anthropic",
    model: Optional[str] = None,
    ollama_url: str = DEFAULT_OLLAMA_URL,
    tumor_type: Optional[str] = None,
    quiet: bool = False
) -> str:
    """Analyze a pathology report using the specified provider."""

    # Load skill and references
    if not quiet:
        print("Loading skill and references...", file=sys.stderr)

    skill_content = load_skill_file()
    reference_content = load_reference_file(tumor_type)
    staging_content = load_staging_reference()

    if not skill_content:
        print("Warning: SKILL.md not found", file=sys.stderr)

    # Build prompt
    full_prompt = ANALYSIS_PROMPT.format(
        skill_content=skill_content,
        reference_content=reference_content,
        staging_content=staging_content,
        report_text=report_text,
        user_prompt=user_prompt
    )

    # Call LLM
    if provider == "anthropic":
        client = create_anthropic_client()
        model = model or DEFAULT_ANTHROPIC_MODEL
        return call_anthropic(client, model, full_prompt, quiet)

    elif provider == "ollama":
        client = create_ollama_client(ollama_url)
        model = model or DEFAULT_OLLAMA_MODEL
        return call_ollama(client, model, full_prompt, quiet)

    elif provider == "lmstudio":
        # LM Studio uses same API as Ollama, just different default URL
        lmstudio_url = ollama_url if ollama_url != DEFAULT_OLLAMA_URL else DEFAULT_LMSTUDIO_URL
        client = create_ollama_client(lmstudio_url)
        # LM Studio typically uses the loaded model, pass through whatever is specified
        model = model or "local-model"
        return call_ollama(client, model, full_prompt, quiet)

    else:
        print(f"Error: Unknown provider '{provider}'", file=sys.stderr)
        sys.exit(1)


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Analyze a pathology report against CAP/ICCR guidelines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check report with Claude (requires ANTHROPIC_API_KEY)
  python check_report.py "Check this breast report for compliance" < report.txt

  # Check report with local Ollama
  python check_report.py --provider ollama "Check for CAP compliance" < report.txt

  # Check report with LM Studio
  python check_report.py --provider lmstudio "Check for CAP compliance" < report.txt

  # Specify model and output to file
  python check_report.py -p ollama -m qwen2.5:32b --file report.txt > result.txt

  # Generate synoptic template
  python check_report.py "Generate CAP synoptic template" < report.txt

  # Quiet mode (only output, no progress messages)
  python check_report.py -q "Check compliance" < report.txt
"""
    )

    parser.add_argument(
        "prompt",
        nargs="?",
        default="Check this pathology report for CAP/ICCR compliance and identify any missing or incomplete elements.",
        help="Instruction/prompt for analysis"
    )

    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Path to report file (alternative to stdin)"
    )

    parser.add_argument(
        "--provider", "-p",
        type=str,
        default=os.environ.get("LLM_PROVIDER", "anthropic"),
        choices=["anthropic", "ollama", "lmstudio"],
        help="LLM provider (default: anthropic, or LLM_PROVIDER env var)"
    )

    parser.add_argument(
        "--model", "-m",
        type=str,
        default=os.environ.get("OLLAMA_MODEL") if os.environ.get("LLM_PROVIDER") == "ollama" else None,
        help="Model name (default: claude-sonnet-4-20250514 for anthropic, llama3.1:70b for ollama)"
    )

    parser.add_argument(
        "--ollama-url",
        type=str,
        default=os.environ.get("OLLAMA_URL", DEFAULT_OLLAMA_URL),
        help=f"Ollama API base URL (default: {DEFAULT_OLLAMA_URL})"
    )

    parser.add_argument(
        "--tumor-type", "-t",
        type=str,
        choices=["breast", "colorectal", "pancreas", "gastric"],
        help="Tumor type hint (auto-detected if not specified)"
    )

    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Request JSON output format"
    )

    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress progress messages"
    )

    args = parser.parse_args()

    # Read report text
    if args.file:
        report_path = Path(args.file)
        if not report_path.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        report_text = report_path.read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        report_text = sys.stdin.read()
    else:
        print("Error: No report provided. Use --file or pipe via stdin.", file=sys.stderr)
        print("Example: python check_report.py 'Check compliance' < report.txt", file=sys.stderr)
        sys.exit(1)

    if not report_text.strip():
        print("Error: Empty report provided.", file=sys.stderr)
        sys.exit(1)

    # Modify prompt for JSON output if requested
    user_prompt = args.prompt
    if args.json:
        user_prompt += "\n\nReturn the analysis as a structured JSON object."

    # Analyze
    try:
        result = analyze_report(
            report_text=report_text,
            user_prompt=user_prompt,
            provider=args.provider,
            model=args.model,
            ollama_url=args.ollama_url,
            tumor_type=args.tumor_type,
            quiet=args.quiet
        )
        print(result)

    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
