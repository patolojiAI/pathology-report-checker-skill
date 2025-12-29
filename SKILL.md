---
name: pathology-report-checker
description: Analyzes surgical pathology cancer reports for compliance with CAP and ICCR guidelines. Compares report content against required elements and generates QA reports showing missing features. Can also generate blank synoptic templates for new reports. Supports reports in any language (designed for Turkish). Use when user provides a pathology report text (pasted, uploaded, or file path) and wants to check completeness against international standards, or when user wants a blank CAP template. Supports breast invasive carcinoma, colorectal resection, exocrine pancreas carcinoma, and gastric carcinoma.
---

# Pathology Report Compliance Checker

Analyze surgical pathology cancer reports against CAP (College of American Pathologists) and ICCR (International Collaboration on Cancer Reporting) guidelines.

## Quick Reference

> 📋 **See also:** `docs/QUICK_REFERENCE.md` for a 1-page cheat sheet

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

## Core Workflow

> 📋 **See also:** `docs/WORKFLOW.md` for detailed step-by-step instructions

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
Cross-check pTNM categories against stage group.

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

> 📋 **See also:** `docs/FEATURES.md` for detailed feature documentation

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

> 📋 **See also:** `docs/USAGE.md` for detailed usage instructions

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

---

## Documentation

| File | Contents |
|------|----------|
| `docs/QUICK_REFERENCE.md` | 1-page cheat sheet |
| `docs/WORKFLOW.md` | Detailed compliance workflow |
| `docs/FEATURES.md` | Feature documentation |
| `docs/USAGE.md` | CLI and script usage |
| `README.md` | User-facing overview |
| `TODO.md` | Feature roadmap |
