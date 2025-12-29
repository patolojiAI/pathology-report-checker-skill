# Pathology Report Compliance Checker

A Claude skill for analyzing surgical pathology cancer reports against international guidelines and best practices.

## Overview

This skill helps pathologists and pathology departments ensure their cancer reports meet CAP (College of American Pathologists), ICCR (International Collaboration on Cancer Reporting), and AAPA (American Association of Pathology Assistants) standards.

## Features

### ✅ Completed Features

#### Report Compliance Checking
| Feature | Description |
|---------|-------------|
| **Breast invasive carcinoma** | CAP Breast.Invasive + ICCR dataset validation |
| **Colorectal resection** | CAP ColoRectal + ICCR dataset validation |
| **Exocrine pancreas** | CAP Panc.Exo + ICCR dataset validation |
| **Gastric carcinoma** | CAP Stomach + ICCR dataset, HER2/MSI, Laurén/Borrmann |

#### Macroscopy/Gross Description
| Feature | Description |
|---------|-------------|
| **Gross description completeness** | AAPA guidelines, specimen-specific required elements |
| **Gross vs Diagnosis validation** | Size, margins, nodes, tumor extent discrepancies |
| **Specimen-specific requirements** | TME grading, Whipple margins, mastectomy elements |

#### Analysis Capabilities
| Feature | Description |
|---------|-------------|
| **Severity scoring** | Critical/Major/Minor classification of gaps |
| **Empty vs Missing detection** | Distinguishes blank fields from absent fields |
| **Cross-validation** | pT vs size, pN vs node count, margin vs R classification |
| **Quality metrics** | Completeness, clarity, consistency scores |
| **Trend tracking** | Historical data for department QA |
| **TNM stage calculator** | AJCC 8th edition stage verification for all tumor types |
| **Synoptic template generator** | Generate blank CAP templates with all required fields |
| **SNOMED CT / ICD-O-3 coding** | Suggest morphology, topography, and procedure codes |
| **AAPA Macroscopy** | Integrated AAPA protocols in macroscopy files (all 4 tumor types) |
| **Tumor board summary** | Generate concise 3-5 line MDT summaries from reports |
| **Free-text → Synoptic** | Convert narrative reports to structured CAP format |
| **Auto-fill suggestions** | Suggest pT/pN/Stage based on tumor size, node count, findings |
| **Amendment generator** | Generate addendum/correction/amended report text |
| **Watch folder** | Auto-process new reports dropped into monitored directory |

#### Input Modes
| Feature | Description |
|---------|-------------|
| **Interactive** | Paste report text in chat |
| **File mode** | Single or multiple report files |
| **CLI folder mode** | Process folder of images, PDFs, text files |
| **CLI spreadsheet mode** | Process Excel/CSV with report contents |
| **Batch processing** | Python script with Claude API |

#### Output Formats
| Feature | Description |
|---------|-------------|
| **Individual QA reports** | Detailed per-report analysis |
| **Summary statistics** | Aggregate compliance metrics |
| **CSV export** | Structured data for analysis |
| **Excel export** | Multi-sheet workbook with details |
| **Trend history** | JSON for longitudinal tracking |

### 🟡 In Progress

*None currently*

### ⬜ Planned Features

See [TODO.md](TODO.md) for full roadmap.

**Coming Soon:**
- Pediatric tumors (Wilms, neuroblastoma, hepatoblastoma)
- Tumor board summary generator
- Lung carcinoma (NSCLC)
- Auto-fill suggestions

## Supported Languages

Reports can be in any language. Designed and tested with:
- Turkish
- English

Terminology mapping tables included in reference files.

## Trigger Phrases

### Report Compliance Check

**English:**
```
Check this pathology report for CAP/ICCR compliance
Analyze this report for missing elements
Is this breast cancer report complete?
What's missing from this colorectal pathology report?
Review this Whipple report against CAP guidelines
```

**Turkish (Türkçe):**
```
Bu patoloji raporunu CAP/ICCR uyumluluğu için kontrol et
Bu raporda eksik elementleri analiz et
Bu meme kanseri raporu tam mı?
Bu kolorektal patoloji raporunda eksikler neler?
```

### Synoptic Template Generation

**English:**
```
Generate a synoptic template for breast lumpectomy
Give me a CAP template for Whipple specimen
Create a gastric carcinoma report template
I need a colorectal resection template
Blank pancreas cancer report form
Create a mastectomy synoptic report template for a 2.5cm Grade 2 IDC
```

**Turkish (Türkçe):**
```
Meme lumpektomi için sinoptik şablon oluştur
Whipple materyali için CAP şablonu ver
Mide karsinomu rapor şablonu oluştur
Kolorektal rezeksiyon şablonu istiyorum
Pankreas kanseri için boş rapor formu
2.3cm Grade 2 invaziv duktal karsinom için meme şablonu
Total gastrektomi sinoptik rapor şablonu
```

### Tumor Board Summary

**English:**
```
Generate a tumor board summary
Create an MDT summary from this report
Summarize for tumor board
Write a brief oncology summary
Give me a 3-line case summary
```

**Turkish (Türkçe):**
```
Tümör kurulu özeti oluştur
MDT özeti yaz
Onkoloji konsültasyon özeti
Vaka özeti hazırla
Kısa patoloji özeti ver
```

### TNM Stage Calculation

**English:**
```
Calculate TNM stage for pT2 N1 M0 breast cancer
What stage is pT3 N1b colorectal cancer?
Verify the staging in this report
Is pT2 N1 M0 Stage IIB correct for breast?
```

**Turkish (Türkçe):**
```
pT2 N1 M0 meme kanseri için TNM evresini hesapla
pT3 N1b kolorektal kanser hangi evre?
Bu rapordaki evrelemeyi doğrula
```

### SNOMED CT / ICD-O-3 Coding

**English:**
```
What's the SNOMED code for invasive ductal carcinoma?
Give me ICD-O-3 codes for this tumor
Suggest morphology and topography codes
Code this report with SNOMED CT
```

**Turkish (Türkçe):**
```
İnvaziv duktal karsinom için SNOMED kodu nedir?
Bu tümör için ICD-O-3 kodları ver
Morfoloji ve topografi kodları öner
```

### Free-Text to Synoptic Conversion

**English:**
```
Convert this report to synoptic format
Generate synoptic report from this text
Transform to CAP format
Create structured report
Free-text to synoptic
```

**Turkish (Türkçe):**
```
Bu raporu sinoptik formata dönüştür
Sinoptik rapor oluştur
CAP formatına çevir
Yapılandırılmış rapor oluştur
Serbest metinden sinoptik çıkar
```

### Auto-Fill Suggestions

**English:**
```
Suggest values for this report
Auto-fill staging
What should pT be for this tumor?
Calculate stage from these findings
Fill in missing fields
Suggest pTNM
```

**Turkish (Türkçe):**
```
Bu rapor için değerler öner
Evrelemeyi otomatik doldur
Bu tümör için pT ne olmalı?
Bu bulgulardan evreyi hesapla
Eksik alanları doldur
pTNM öner
```

### Amendment Generator

**English:**
```
Generate an amendment for this report
Create an addendum for missing staging
Write a correction for margin status
Draft amendment for node count change
Prepare amended report text
Fix this staging error
```

**Turkish (Türkçe):**
```
Bu rapor için düzeltme oluştur
Eksik evreleme için ek rapor yaz
Sınır durumu düzeltmesi hazırla
Lenf nodu sayısı değişikliği için düzeltme
Düzeltilmiş rapor metni hazırla
```

### Pre-fill Examples

```
# English - with tumor details
Generate breast template for 1.8cm Grade 1 invasive lobular carcinoma

# Turkish - with tumor details  
3.2cm az diferansiye adenokarsinom için kolon şablonu oluştur
```

## Usage

### Option 1: Claude CLI / Claude.ai / Claude App (No API Key)

Uses your existing Claude authentication. No additional API key required.

**Claude.ai / Claude App:**
```
Simply paste or upload a pathology report and use any of the trigger phrases above.
```

**Claude CLI:**
```bash
# Single report
claude "Check this breast pathology report for CAP compliance" < report.txt

# Folder of reports
claude "Analyze all pathology reports in /path/to/reports/ for CAP/ICCR compliance"

# Convert to synoptic format
claude "Convert this report to CAP synoptic format" < narrative_report.txt

# Generate tumor board summary
claude "Generate a tumor board summary from this report" < report.pdf

# Excel/CSV file
claude "Check compliance for reports in /path/to/reports.xlsx"
```

---

### Option 2: Python Scripts (API Key Required)

Makes direct API calls. Requires `ANTHROPIC_API_KEY` environment variable.

**When to use Python scripts:**
- Automated/scheduled batch processing
- Continuous folder monitoring
- Integration with LIS/pipelines
- Cron jobs

#### Batch Processing Script

```bash
# Install dependencies
pip install anthropic openpyxl

# Set API key (required!)
export ANTHROPIC_API_KEY="your-api-key-here"

# Run batch analysis
python scripts/batch_checker.py /input/folder /output/folder --tumor-type pancreas
```

#### Watch Folder Script (Automatic Processing)

```bash
# Install dependencies
pip install anthropic watchdog openpyxl pypdf python-docx

# Set API key (required!)
export ANTHROPIC_API_KEY="your-api-key-here"

# Watch folder for compliance checking
python scripts/watch_folder.py /path/to/reports --output /path/to/results

# Different processing modes
python scripts/watch_folder.py /reports --mode synoptic      # Convert to synoptic
python scripts/watch_folder.py /reports --mode summary       # Tumor board summaries
python scripts/watch_folder.py /reports --mode autofill      # Suggest missing values

# Process existing files on startup
python scripts/watch_folder.py /reports --process-existing

# One-time batch (no continuous watching)
python scripts/watch_folder.py /reports --no-watch --process-existing

# Custom polling interval (seconds)
python scripts/watch_folder.py /reports --interval 30
```

**Supported file types:** `.txt`, `.md`, `.pdf`, `.docx`, `.jpg`, `.png`, `.tiff`

---

### Quick Reference

| Scenario | Method | API Key? |
|----------|--------|----------|
| Check a few reports manually | Claude.ai / Claude App | ❌ No |
| One-time folder analysis | Claude CLI | ❌ No |
| Daily automated batch job | `batch_checker.py` | ✅ Yes |
| Continuous folder monitoring | `watch_folder.py` | ✅ Yes |

## File Structure

```
pathology-report-checker/
├── SKILL.md                    # Main skill instructions (streamlined)
├── README.md                   # This file
├── TODO.md                     # Feature roadmap
├── docs/                       # Detailed documentation
│   ├── QUICK_REFERENCE.md      # 1-page cheat sheet
│   ├── WORKFLOW.md             # Detailed compliance workflow
│   ├── FEATURES.md             # Feature documentation
│   └── USAGE.md                # CLI and script usage
├── samples/                    # Test reports (synthetic/anonymized)
│   ├── README.md               # Sample descriptions and usage
│   ├── breast_complete_en.txt  # Complete breast (EN)
│   ├── breast_incomplete_en.txt # Incomplete breast (EN)
│   ├── breast_complete_tr.txt  # Complete breast (TR)
│   ├── colorectal_complete_en.txt
│   ├── colorectal_errors_en.txt # Cross-validation errors
│   ├── colorectal_incomplete_tr.txt
│   ├── pancreas_complete_en.txt
│   ├── pancreas_staging_error_en.txt
│   ├── gastric_complete_en.txt
│   ├── gastric_incomplete_tr.txt
│   └── expected_outputs/       # Expected QA results
├── scripts/
│   ├── batch_checker.py        # Python batch processor (API key required)
│   └── watch_folder.py         # Watch folder processor (API key required)
└── references/
    ├── diagnosis/              # Microscopic diagnosis guidelines (CAP/ICCR)
    │   ├── breast_invasive_carcinoma.md
    │   ├── colorectal_resection.md
    │   ├── exocrine_pancreas.md
    │   └── gastric_carcinoma.md
    ├── macroscopy/             # Gross description guidelines (AAPA-integrated)
    │   ├── MACROSCOPY_COMMON.md
    │   ├── breast_macroscopy.md
    │   ├── colorectal_macroscopy.md
    │   ├── pancreas_macroscopy.md
    │   └── gastric_macroscopy.md
    ├── staging/                # TNM staging calculator (AJCC 8th)
    │   └── tnm_stage_calculator.md
    ├── templates/              # Synoptic report templates (CAP)
    │   ├── synoptic_templates.md
    │   └── synoptic_templates_tr.md  # Turkish version
    ├── coding/                 # SNOMED CT / ICD-O-3 codes
    │   └── snomed_ct_codes.md
    ├── summaries/              # Summary generators
    │   └── tumor_board_summary.md
    ├── converters/             # Format converters
    │   └── freetext_to_synoptic.md
    ├── autofill/               # Auto-fill suggestions
    │   └── autofill_suggestions.md
    ├── amendments/             # Amendment templates
    │   └── amendment_generator.md
    └── biomarkers/             # Biomarker reporting guidelines (ASCO/CAP)
        └── BIOMARKERS_INDEX.md
```

## Guidelines Referenced

| Organization | Guidelines |
|--------------|------------|
| **CAP** | Cancer Protocol Templates (2024) |
| **ICCR** | Cancer Datasets (2nd edition) |
| **AJCC** | TNM Staging 8th Edition |
| **AAPA** | Macroscopic Examination Guidelines (3rd edition) |
| **WHO** | Classification of Tumours (5th edition) |

## Quality Metrics

### Compliance Score
```
Score = 100 - (Critical × 15) - (Major × 5) - (Minor × 2)

90-100: COMPLIANT
70-89:  INCOMPLETE - MINOR
50-69:  INCOMPLETE - MAJOR
<50:    INCOMPLETE - CRITICAL
```

### Cross-Validation Checks
- pT category vs tumor size (AJCC 8th)
- pN category vs positive node count
- R classification vs margin distance (ICCR)
- Lymph node adequacy (minimum counts)
- Gross vs microscopic consistency

### Macroscopy Checks
- Gross description completeness by specimen type
- Tumor size: gross vs microscopic (>20% discrepancy flagged)
- Margin status: gross distance vs microscopic involvement
- Lymph node count: gross vs microscopic
- Tumor extent: gross impression vs microscopic staging

## Documentation

| File | Description |
|------|-------------|
| `SKILL.md` | Core skill instructions (streamlined) |
| `docs/QUICK_REFERENCE.md` | 1-page cheat sheet with all triggers and references |
| `docs/WORKFLOW.md` | Detailed step-by-step compliance workflow |
| `docs/FEATURES.md` | Documentation for all features |
| `docs/USAGE.md` | CLI and script usage guide |
| `README.md` | This overview file |
| `TODO.md` | Feature roadmap and completion status |

## Contributing

To add a new tumor type:
1. Create reference file in `references/` following existing format
2. Include: Core elements, Conditional elements, Recommended elements
3. Add Turkish-English terminology table
4. Add cross-validation rules
5. Update TODO.md and README.md

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-27 | Initial release: breast, colorectal |
| 1.1 | 2024-12-28 | Added pancreas, severity scoring, cross-validation |
| 1.2 | 2024-12-28 | Quality metrics, trend tracking, CLI modes |
| 1.3 | 2024-12-28 | LLM-powered batch processing |
| 1.4 | 2024-12-28 | Macroscopy checker (AAPA guidelines) |
| 1.5 | 2024-12-28 | Gastric carcinoma (CAP/ICCR, HER2, Laurén) |
| 1.6 | 2024-12-28 | TNM stage calculator (AJCC 8th, all tumors) |
| 1.7 | 2024-12-28 | Synoptic template generator (blank CAP templates) |
| 1.8 | 2024-12-28 | SNOMED CT / ICD-O-3 coding (morphology, topography) |
| 1.9 | 2024-12-28 | AAPA Guidelines (breast macroscopy, pre-analytics) |
| 2.0 | 2024-12-28 | Tumor board summary generator (3-5 line MDT summaries) |
| 2.1 | 2024-12-29 | Free-text to synoptic converter |
| 2.2 | 2024-12-29 | Auto-fill suggestions (pT/pN/Stage from context) |
| 2.3 | 2024-12-29 | Amendment generator (addendum/correction/amended report) |
| 2.4 | 2024-12-29 | Watch folder (auto-process new reports) |
| 2.5 | 2024-12-29 | Documentation split (SKILL.md → modular docs/) |
| 2.6 | 2024-12-29 | Sample reports (10 synthetic test cases) |
| 2.7 | (next) | Pediatric tumors (Wilms, neuroblastoma) |

## License

For use with Claude by Anthropic.

## Author

Developed collaboratively with Claude for surgical pathology quality assurance.
