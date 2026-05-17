---
name: pathology-report-checker
description: Analyzes surgical pathology cancer reports for compliance with CAP (College of American Pathologists) and ICCR (International Collaboration on Cancer Reporting) guidelines. Validates TNM staging (AJCC 8th edition), checks element completeness, generates synoptic templates, creates tumor board summaries, suggests SNOMED/ICD-O-3 codes, and converts free-text reports to structured format. Use when user mentions pathology reports, cancer staging, CAP compliance, synoptic templates, tumor board summaries, or provides report text for breast, colorectal, pancreas, or gastric carcinoma. Supports English and Turkish.
---

# Pathology Report Compliance Checker

Analyze surgical pathology cancer reports against CAP (College of American Pathologists) and ICCR (International Collaboration on Cancer Reporting) guidelines.

## Quick Reference

### Trigger Phrases

| Action | English | Turkish |
|--------|---------|---------|
| **Compliance Check** | "Check this report for CAP compliance" | "Bu raporu CAP uyumluluğu için kontrol et" |
| **Synoptic Template** | "Generate breast synoptic template" | "Meme sinoptik şablonu oluştur" |
| **Tumor Board Summary** | "Generate tumor board summary" | "Tümör kurulu özeti oluştur" |
| **Free-text → Synoptic** | "Convert to synoptic format" | "Sinoptik formata dönüştür" |
| **Auto-fill** | "Suggest pTNM staging" | "pTNM evrelemesi öner" |
| **Amendment** | "Generate amendment for this" | "Düzeltme oluştur" |
| **SNOMED Coding** | "What's the SNOMED code for..." | "... için SNOMED kodu nedir?" |
| **TNM Calculator** | "Calculate stage for pT2 N1 M0" | "pT2 N1 M0 için evreyi hesapla" |

---

## Supported Input Formats

This skill supports multiple input formats for maximum flexibility:

| Format | Extensions | Use Case | Processing Method |
|--------|------------|----------|-------------------|
| **Plain Text** | `.txt`, `.md` | Interactive CLI, direct paste | Direct reading (UTF-8/Latin-1) |
| **Excel Batch** | `.xlsx`, `.xls` | Multiple reports at once | Pandas + batch processing |
| **Excel Structured** | `.xlsx`, `.xls` | LIS exports, pre-filled forms | Field extraction |
| **CSV** | `.csv` | Database exports | Batch processing |
| **PDF** | `.pdf` | Scanned or digital reports | pypdf + Claude Vision API fallback |
| **Images** | `.jpg`, `.png`, `.tiff` | Scanned paper reports | Claude Vision API |
| **Word** | `.docx` | Office documents | python-docx |

### Interactive Use (Claude CLI)
```bash
# Text file
claude "Check this report using pathology-report-checker" < report.txt

# PDF
claude "Analyze this PDF using pathology-report-checker" < report.pdf

# Image
claude "Extract and check this scanned report" < scan.jpg
```

### Batch Processing
```bash
# Excel batch list (one report per row)
python .dev/scripts/batch_checker.py reports.xlsx output_dir/

# Process entire directory (mixed formats)
python .dev/scripts/batch_checker.py input_dir/ output_dir/

# Watch folder for new files
python .dev/scripts/watch_folder.py input_dir/ output_dir/ compliance
```

### Excel Batch Format Requirements

**Expected columns:**
- `report_text` (required): Full pathology report text
- `patient_id` (optional): Patient/case identifier
- `tumor_type` (optional): breast, colorectal, gastric, pancreas (auto-detect if not specified)

**Example:**
| report_text | patient_id | tumor_type |
|-------------|------------|------------|
| PATHOLOGY REPORT<br>Specimen: Mastectomy... | P12345 | breast |
| PATHOLOGY REPORT<br>Specimen: Right hemicolectomy... | P12346 | colorectal |

### Excel Structured Format

**Two-column layout:**
- Column A: Field names (Procedure, Tumor Size, Grade, Margins, etc.)
- Column B: Values

**Example:**
| Field | Value |
|-------|-------|
| Procedure | Total mastectomy |
| Tumor Site | Upper outer quadrant |
| Tumor Size | 2.3 cm |
| Histologic Type | Invasive ductal carcinoma |
| Histologic Grade | G2 |
| ER Status | Positive (95%) |
| PR Status | Positive (80%) |
| HER2 Status | Negative |

The skill will automatically detect which format and extract accordingly.

---

## Supported Report Types

| Type | CAP Protocol | ICCR Dataset |
|------|--------------|--------------|
| Breast invasive carcinoma | Breast.Invasive | Invasive Carcinoma of the Breast |
| Colorectal primary resection | ColoRectal | Colorectal Cancer |
| Exocrine pancreas carcinoma | Panc.Exo | Carcinoma of the Exocrine Pancreas |
| Gastric carcinoma | Stomach | Gastric Carcinoma |

---

## Reference Files

### Diagnosis (CAP/ICCR Required Elements)
| Tumor | File |
|-------|------|
| Breast | `references/diagnosis/breast_invasive_carcinoma.md` |
| Colorectal | `references/diagnosis/colorectal_resection.md` |
| Pancreas | `references/diagnosis/exocrine_pancreas.md` |
| Gastric | `references/diagnosis/gastric_carcinoma.md` |

### Macroscopy (AAPA-integrated)
| Tumor | File |
|-------|------|
| Common | `references/macroscopy/MACROSCOPY_COMMON.md` |
| Breast | `references/macroscopy/breast_macroscopy.md` |
| Colorectal | `references/macroscopy/colorectal_macroscopy.md` |
| Pancreas | `references/macroscopy/pancreas_macroscopy.md` |
| Gastric | `references/macroscopy/gastric_macroscopy.md` |

### Other References
| Feature | File |
|---------|------|
| TNM Staging | `references/staging/tnm_stage_calculator.md` |
| Synoptic Templates (EN) | `references/templates/synoptic_templates.md` |
| Synoptic Templates (TR) | `references/templates/synoptic_templates_tr.md` |
| SNOMED CT / ICD-O-3 | `references/coding/snomed_ct_codes.md` |
| Tumor Board Summary | `references/summaries/tumor_board_summary.md` |
| Free-text Converter | `references/converters/freetext_to_synoptic.md` |
| Auto-fill Suggestions | `references/autofill/autofill_suggestions.md` |
| Amendment Generator | `references/amendments/amendment_generator.md` |
| Biomarker Index | `references/biomarkers/BIOMARKERS_INDEX.md` |

---

## Quick Search Patterns

For large reference files, use grep to find specific content quickly:

**Find tumor type template:**
```bash
grep -A 50 "## Breast Invasive" references/templates/synoptic_templates.md
grep -A 50 "## Colorectal" references/templates/synoptic_templates.md
grep -A 50 "## Pancreas" references/templates/synoptic_templates.md
grep -A 50 "## Gastric" references/templates/synoptic_templates.md
```

**Find specific staging table:**
```bash
grep -A 20 "Breast Cancer Stage" references/staging/tnm_stage_calculator.md
grep -A 20 "Colorectal Stage" references/staging/tnm_stage_calculator.md
grep -A 20 "Pancreas Stage" references/staging/tnm_stage_calculator.md
```

**Find SNOMED code:**
```bash
grep -i "ductal carcinoma" references/coding/snomed_ct_codes.md
grep -i "adenocarcinoma" references/coding/snomed_ct_codes.md
```

**Find amendment template:**
```bash
grep -A 15 "Addendum Template" references/amendments/amendment_generator.md
grep -A 15 "Correction Template" references/amendments/amendment_generator.md
```

---

## Mode Selection Guide

Determine the task type before proceeding:

**User wants compliance checking?** → Follow "Compliance Check Workflow" below
**User wants template generation?** → Follow "Template Generation Workflow" below
**User wants tumor board summary?** → Follow "Summary Generation Workflow" below
**User wants staging calculation only?** → Read `references/staging/tnm_stage_calculator.md`
**User wants SNOMED codes?** → Read `references/coding/snomed_ct_codes.md`
**User wants to convert free-text?** → Read `references/converters/freetext_to_synoptic.md`

---

## Core Workflow

### Compliance Check Workflow

### Step 1: Determine Report Type
From report content, identify organ, specimen type, and tumor type.

### Step 2: Load Reference Files
Load the appropriate diagnosis and macroscopy reference files.

### Step 3: Extract Elements
Parse report text using terminology equivalents (EN/TR).

### Step 4: Analyze
- **4a**: Check for missing/empty elements by severity
- **4b**: Cross-validate (pT vs size, pN vs nodes, margins vs R)
- **4c**: Calculate quality metrics
- **4d**: Check macroscopy/gross description

### Step 5: Generate Output
Produce QA report with compliance score.

### Step 6: Verify Staging
Cross-check pTNM categories against stage group using `references/staging/tnm_stage_calculator.md`.

### Template Generation Workflow

1. Identify tumor type and specimen type from user request
2. Read appropriate section from `references/templates/synoptic_templates.md` (or `_tr.md` for Turkish)
3. Use grep to find specific template: `grep -A 100 "## Breast Invasive" references/templates/synoptic_templates.md`
4. Optionally pre-fill with provided values if user specifies (e.g., "2.3cm Grade 2 IDC")
5. Return formatted template with all required CAP elements

### Summary Generation Workflow

1. Extract key findings from the pathology report
2. Read `references/summaries/tumor_board_summary.md` for format and examples
3. Generate concise 3-5 line MDT summary
4. Include: patient age/sex, diagnosis, procedure, stage, margins, nodes, biomarkers
5. Follow format examples in reference file

---

## Severity Levels

| Level | Elements | Score Impact |
|-------|----------|--------------|
| 🔴 **CRITICAL** | pT, pN, margins, grade, receptors | -15 each |
| 🟠 **MAJOR** | LVI, PNI, tumor size, node counts | -5 each |
| 🟡 **MINOR** | Focality, gross details | -2 each |

**Score:** `100 - (Critical × 15) - (Major × 5) - (Minor × 2)`

| Score | Status |
|-------|--------|
| 90-100 | ✅ COMPLIANT |
| 70-89 | 🟡 INCOMPLETE - MINOR |
| 50-69 | 🟠 INCOMPLETE - MAJOR |
| <50 | 🔴 INCOMPLETE - CRITICAL |

---

## Features

### Template Generation
Generate blank CAP-style synoptic templates for any tumor type.
- EN + TR versions
- Pre-fill with known values
- All CAP elements included

### Tumor Board Summary
Generate concise 3-5 line MDT summaries:
```
58F with invasive ductal carcinoma of the left breast.
Lumpectomy: 2.3 cm IDC, Grade 2, pT2 N1a M0 (Stage IIB).
Margins: Negative. LVI: Present. Nodes: 2/15 positive.
ER 95%/PR 80%/HER2 neg/Ki-67 25%.
```

### Free-Text → Synoptic Converter
Convert narrative reports to structured CAP format.

### Auto-Fill Suggestions
Suggest pT/pN/Stage based on tumor size, node count, findings.

### Amendment Generator
Generate addendum/correction/amended report text.

### TNM Stage Calculator
Calculate stage groups from pT/pN/pM categories (AJCC 8th).

### SNOMED CT / ICD-O-3 Coding
Suggest morphology and topography codes.

---

## Usage

### Option 1: Claude CLI / Claude.ai (No API Key)

Uses your existing Claude authentication.

```bash
# Check single report
claude "Check this breast report for CAP compliance" < report.txt

# Analyze folder
claude "Analyze all pathology reports in /data/reports/"

# Generate summary
claude "Generate tumor board summary" < report.pdf
```

### Option 2: Python Scripts (API Key Required)

For automated/scheduled processing.

```bash
# Setup
pip install anthropic watchdog openpyxl pypdf python-docx
export ANTHROPIC_API_KEY="your-key"

# Batch processing
python scripts/batch_checker.py /input /output --tumor-type pancreas

# Watch folder
python scripts/watch_folder.py /reports --mode compliance
```

### Quick Reference

| Method | API Key? | Best For |
|--------|----------|----------|
| Claude.ai / App | ❌ No | Manual checking |
| Claude CLI | ❌ No | One-time analysis |
| `batch_checker.py` | ✅ Yes | Automated batches |
| `watch_folder.py` | ✅ Yes | Continuous monitoring |

---

## Language Handling

- Reports may be in English or Turkish
- Use terminology equivalents from reference files
- Respond in the same language as the report
- Templates available in both languages

---

## Important Notes

1. **Always read the appropriate reference file** before analyzing a report
2. **Cross-validate** pT/pN/Stage, size, margins, node counts
3. **Check macroscopy** for gross-microscopic correlation
4. **Report language**: Match the input language
5. **Severity matters**: Prioritize critical gaps over minor ones

