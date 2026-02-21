# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Claude Skill for analyzing surgical pathology cancer reports against CAP (College of American Pathologists), ICCR (International Collaboration on Cancer Reporting), and AAPA (American Association of Pathology Assistants) guidelines. The skill checks report completeness, validates staging, cross-checks consistency, and generates synoptic templates.

**Supported tumor types:** Breast invasive carcinoma, Colorectal resection, Exocrine pancreas carcinoma, Gastric carcinoma.

**Supported languages:** English and Turkish (with terminology mapping).

## Repository Structure

```
pathology-report-checker-skill/
├── SKILL.md                    # Main skill entry point (YAML frontmatter + markdown)
├── pathology-report-checker.skill  # Large compiled version (90k+ tokens)
├── references/                 # Clinical reference files (markdown)
│   ├── diagnosis/              # CAP/ICCR required elements by tumor type
│   ├── macroscopy/             # AAPA gross description guidelines
│   ├── staging/                # TNM stage calculator (AJCC 8th)
│   ├── templates/              # Synoptic report templates (EN/TR)
│   ├── coding/                 # SNOMED CT / ICD-O-3 codes
│   ├── summaries/              # Tumor board summary generator
│   ├── converters/             # Free-text to synoptic converter
│   ├── autofill/               # Auto-fill suggestions
│   ├── amendments/             # Amendment generator
│   └── biomarkers/             # Biomarker reporting guidelines
├── scripts/                    # Python automation scripts
│   ├── batch_checker.py        # Batch processing with Claude API
│   └── watch_folder.py         # Auto-process new reports in folder
├── samples/                    # Test reports (synthetic/anonymized)
├── docs/                       # Detailed documentation
└── README.md, TODO.md          # User documentation and roadmap
```

## Key Architecture Concepts

### 1. Skill-Based Design

The skill follows Claude's skill architecture:
- **SKILL.md**: Core skill definition with YAML frontmatter (name, description) and markdown instructions
- **Reference files**: External knowledge files loaded on-demand (diagnosis guidelines, staging tables, templates)
- **Modular documentation**: Quick reference, workflow, features, usage guides in `docs/`

When Claude processes a pathology report:
1. Determines tumor type from report content
2. Loads corresponding reference files from `references/diagnosis/` and `references/macroscopy/`
3. Extracts elements using terminology equivalents (EN/TR mappings in reference files)
4. Validates against CAP/ICCR guidelines with severity scoring
5. Cross-validates (pT vs size, pN vs nodes, margins vs R classification)
6. Generates QA report with compliance score

### 2. Severity-Based Scoring System

Elements are classified by clinical impact:
- **CRITICAL** (−15 points): pT, pN, margins, grade, receptors
- **MAJOR** (−5 points): LVI, PNI, tumor size, node counts
- **MINOR** (−2 points): Focality, gross details

Score = 100 − (Critical × 15) − (Major × 5) − (Minor × 2)

Status thresholds: 90-100 (Compliant), 70-89 (Minor), 50-69 (Major), <50 (Critical)

### 3. Cross-Validation Rules

The skill performs automated consistency checks:
- **pT vs Size**: Tumor size must match AJCC pT category
- **pN vs Nodes**: Positive node count must match pN category
- **Margin vs R**: R classification must match margin distance (ICCR: R1 if ≤1mm)
- **Node Adequacy**: Minimum node counts (12 for colorectal, 15 for breast, etc.)
- **Gross vs Microscopic**: Size, margin status, node count, tumor extent

### 4. Multi-Language Support

Reference files contain terminology tables mapping Turkish ↔ English:
```markdown
| English | Turkish (Türkçe) |
|---------|------------------|
| Invasive ductal carcinoma | İnvaziv duktal karsinom |
| Lymphovascular invasion | Lenfovasküler invazyon |
```

The skill recognizes both languages and responds in the same language as the input report.

### 5. Multiple Processing Modes

The skill operates in several modes:
- **Compliance checking**: Analyze against CAP/ICCR guidelines
- **Synoptic template generation**: Generate blank CAP templates (with optional pre-fill)
- **Tumor board summaries**: Generate concise 3-5 line MDT summaries
- **Free-text conversion**: Convert narrative reports to synoptic format
- **Auto-fill**: Suggest pT/pN/Stage based on report context
- **Amendment generation**: Create addendum/correction/amended report text

## Working with Python Scripts

### batch_checker.py

**Purpose:** Batch processing of reports using Claude API

**Key components:**
- Data classes: `GapInfo`, `ValidationIssue`, `QualityMetrics`, `StagingInfo`, `ReportResult`
- Reference loading: `load_reference_file()`, `load_staging_reference()`, `load_skill_file()`
- LLM analysis: `analyze_report_with_llm()` - sends report + references to Claude
- Export functions: `export_to_csv()`, `export_to_excel()`, `save_trend_data()`

**Usage:**
```bash
# Requires ANTHROPIC_API_KEY environment variable
python scripts/batch_checker.py /input/folder /output/folder --tumor-type pancreas
```

**Output:** Individual QA reports, summary statistics, CSV/Excel exports, trend history JSON

### watch_folder.py

**Purpose:** Continuous monitoring and auto-processing of new reports

**Key components:**
- `ProcessedFilesTracker`: Tracks processed files by MD5 hash (prevents reprocessing)
- `ReportProcessor`: Handles different processing modes (compliance, synoptic, summary, autofill)
- `ReportHandler`: FileSystemEventHandler that processes new files
- Watchdog integration for file system events (falls back to polling if unavailable)

**Usage:**
```bash
python scripts/watch_folder.py /reports --output /results --mode compliance
python scripts/watch_folder.py /reports --mode synoptic --process-existing
```

**Supported file types:** .txt, .md, .pdf, .docx, .jpg, .png, .tiff (images require OCR/vision)

## Modifying the Skill

### Adding a New Tumor Type

1. Create diagnosis reference file: `references/diagnosis/[tumor_name].md`
   - Follow existing format: Core Elements, Conditional Elements, Recommended Elements
   - Include severity classification (CRITICAL/MAJOR/MINOR)
   - Add EN/TR terminology table
   - Define cross-validation rules

2. Create macroscopy reference file: `references/macroscopy/[tumor_name]_macroscopy.md`
   - Based on AAPA guidelines
   - Specimen-specific requirements
   - Gross vs microscopic correlation checks

3. Update staging reference: `references/staging/tnm_stage_calculator.md`
   - Add AJCC 8th edition staging table
   - Include pT/pN definitions

4. Update `SKILL.md`:
   - Add to "Supported Report Types" table
   - Update reference files table

5. Update batch_checker.py:
   - Add entry to `reference_map` in `load_reference_file()`

6. Update TODO.md and README.md

### Editing Templates or Guidelines

**Synoptic templates:** Edit `references/templates/synoptic_templates.md` (EN) or `synoptic_templates_tr.md` (TR)

**Biomarker guidelines:** Update `references/biomarkers/BIOMARKERS_INDEX.md`

**Amendment templates:** Modify `references/amendments/amendment_generator.md`

**SNOMED codes:** Edit `references/coding/snomed_ct_codes.md`

## Testing the Skill

### Using Sample Reports

Test reports are in `samples/`:
- `breast_complete_en.txt` - Complete breast report (should score 100)
- `breast_incomplete_en.txt` - Missing critical elements
- `colorectal_errors_en.txt` - Contains cross-validation errors
- `pancreas_staging_error_en.txt` - Stage discrepancy

### Testing Locally

**Interactive (no API key needed):**
```bash
claude "Check this breast report for CAP compliance" < samples/breast_complete_en.txt
```

**Batch processing (requires API key):**
```bash
export ANTHROPIC_API_KEY="your-key"
python scripts/batch_checker.py samples/ output/
```

**Watch folder:**
```bash
python scripts/watch_folder.py samples/ --output results/ --process-existing --no-watch
```

## Important Notes

1. **Reference files are the source of truth**: The skill loads clinical guidelines from `references/` at runtime. Always update reference files rather than hardcoding rules in SKILL.md.

2. **SKILL.md vs pathology-report-checker.skill**: SKILL.md is the editable source (7KB). The .skill file (135KB) appears to be an expanded/compiled version. Edit SKILL.md.

3. **Language detection**: The skill auto-detects language from report content and responds in the same language. No explicit language parameter needed.

4. **Terminology equivalents**: When adding new terms, update the terminology tables in reference files to support both English and Turkish.

5. **Severity matters**: Element severity drives the compliance score. Changing severity classification significantly impacts scoring.

6. **Cross-validation is automatic**: When pT, pN, margins, tumor size, or node counts are present, cross-validation runs automatically. Add new rules in Step 4b of docs/WORKFLOW.md.

7. **TNM staging uses AJCC 8th edition**: All staging calculations reference AJCC 8th (2017). Future updates to AJCC 9th would require updating `references/staging/tnm_stage_calculator.md`.

8. **Quality metrics are weighted**: Overall Quality = 40% Completeness + 20% Clarity + 40% Consistency. Adjust weights in batch_checker.py if needed.

## Common Tasks

### Run batch analysis
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python scripts/batch_checker.py /path/to/reports /path/to/output --tumor-type breast
```

### Generate synoptic template
```bash
claude "Generate a breast lumpectomy synoptic template for 2.3cm Grade 2 IDC"
```

### Convert free-text to synoptic
```bash
claude "Convert this report to CAP synoptic format" < narrative_report.txt
```

### Check compliance
```bash
claude "Check this pancreas Whipple report for CAP/ICCR compliance" < report.txt
```

### Generate tumor board summary
```bash
claude "Generate tumor board summary from this report" < report.pdf
```

### Calculate TNM stage
```bash
claude "What stage is pT3 N1 M0 for pancreas carcinoma?"
```

## Documentation Files

- **SKILL.md**: Core skill instructions (edit this file)
- **docs/QUICK_REFERENCE.md**: 1-page cheat sheet with all triggers and references
- **docs/WORKFLOW.md**: Detailed step-by-step compliance checking workflow
- **docs/FEATURES.md**: Feature documentation
- **docs/USAGE.md**: CLI and script usage guide
- **README.md**: User-facing overview
- **TODO.md**: Feature roadmap and completion tracking
