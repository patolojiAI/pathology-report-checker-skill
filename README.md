# Pathology Report Checker

**A Claude skill for surgical pathology quality assurance**

Analyze cancer pathology reports for compliance with CAP/ICCR guidelines, validate TNM staging, generate synoptic templates, and more. Supports multiple tumor types and languages (English/Turkish).

## 🎯 What This Skill Does

- ✅ Checks report completeness against CAP and ICCR guidelines
- 🔬 Validates TNM staging (AJCC 8th edition)
- 📋 Generates synoptic templates (with optional pre-fill)
- 📊 Creates tumor board summaries
- 🔄 Converts free-text reports to synoptic format
- 🏥 Suggests SNOMED CT and ICD-O-3 codes
- ✏️ Generates amendments and addenda
- 🌐 Supports English and Turkish

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

See [.dev/TODO.md](.dev/TODO.md) for full roadmap.

**Coming Soon:**
- Pediatric tumors (Wilms, neuroblastoma, hepatoblastoma)
- Lung carcinoma (NSCLC)
- Prostate carcinoma

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

## 🚀 Installation

### Method 1: Manual Installation

1. Clone or download this repository
2. Copy the skill folder to `~/.claude/skills/`
3. Restart Claude Code or reload skills

```bash
# Clone the repository
git clone https://github.com/yourusername/pathology-report-checker-skill.git

# Copy to Claude skills directory
cp -r pathology-report-checker-skill ~/.claude/skills/

# Or create a symlink for easier development
ln -s /path/to/pathology-report-checker-skill ~/.claude/skills/pathology-report-checker
```

### Method 2: Direct Download

Download the skill package and extract to `~/.claude/skills/`

## 📖 Usage

### Basic Usage (Claude.ai / Claude Code)

Simply paste or upload a pathology report and use a trigger phrase:

```
Check this breast pathology report for CAP compliance
```

```
Generate a synoptic template for colorectal resection
```

```
Calculate TNM stage for pT2 N1 M0 breast cancer
```

### Claude CLI

```bash
# Check single report
claude "Check this report for CAP compliance" < report.txt

# Generate template
claude "Generate breast lumpectomy synoptic template"

# Tumor board summary
claude "Generate tumor board summary" < report.pdf
```

### Advanced Usage (Batch Processing)

For automated batch processing and folder monitoring, see [.dev/docs/USAGE.md](.dev/docs/USAGE.md)

## 📁 Skill Structure

```
pathology-report-checker-skill/
├── SKILL.md                    # Main skill entry point
├── README.md                   # This file
├── LICENSE                     # MIT License
├── CHANGELOG.md                # Version history
├── marketplace.json            # Marketplace metadata
├── .skillignore                # Files excluded from skill package
├── examples/                   # Example reports for testing
│   ├── breast_complete_en.txt
│   ├── colorectal_errors_en.txt
│   ├── pancreas_staging_error_en.txt
│   └── gastric_complete_en.txt
├── references/                 # Clinical reference files
│   ├── diagnosis/              # CAP/ICCR guidelines by tumor type
│   ├── macroscopy/             # AAPA gross description guidelines
│   ├── staging/                # TNM staging (AJCC 8th)
│   ├── templates/              # Synoptic templates (EN/TR)
│   ├── coding/                 # SNOMED CT / ICD-O-3
│   ├── summaries/              # Tumor board summary generator
│   ├── converters/             # Free-text to synoptic
│   ├── autofill/               # Auto-fill suggestions
│   ├── amendments/             # Amendment generator
│   └── biomarkers/             # Biomarker guidelines
└── .dev/                       # Development files (not in skill package)
    ├── scripts/                # Python automation scripts
    ├── docs/                   # Extended documentation
    ├── TODO.md                 # Development roadmap
    └── CLAUDE.md               # Claude Code development guide
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

## 📚 Documentation

| File | Description |
|------|-------------|
| `SKILL.md` | Core skill instructions |
| `README.md` | This overview (marketplace listing) |
| `CHANGELOG.md` | Version history |
| `marketplace.json` | Skill metadata |
| `.dev/docs/QUICK_REFERENCE.md` | 1-page cheat sheet |
| `.dev/docs/WORKFLOW.md` | Detailed compliance workflow |
| `.dev/docs/FEATURES.md` | Feature documentation |
| `.dev/docs/USAGE.md` | Advanced usage guide |

## 🤝 Contributing

Contributions are welcome! To add support for a new tumor type:

1. Create reference files in `references/diagnosis/` and `references/macroscopy/`
2. Follow existing format: Core/Conditional/Recommended elements
3. Include terminology tables (English ↔ Turkish)
4. Add cross-validation rules
5. Update SKILL.md and README.md
6. Submit a pull request

See [.dev/CLAUDE.md](.dev/CLAUDE.md) for detailed development guide.

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

## 🔗 Links

- **Repository**: [GitHub](https://github.com/yourusername/pathology-report-checker-skill)
- **Issues**: [Report bugs](https://github.com/yourusername/pathology-report-checker-skill/issues)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## ⚕️ Clinical Guidelines

This skill references the following standards:
- CAP Cancer Protocol Templates (2024)
- ICCR Cancer Datasets (2nd edition)
- AJCC TNM Staging Manual (8th edition)
- AAPA Macroscopic Examination Guidelines (3rd edition)
- WHO Classification of Tumours (5th edition)

## 🙏 Acknowledgments

Developed for surgical pathology quality assurance. This tool is designed to assist pathologists but does not replace clinical judgment.
