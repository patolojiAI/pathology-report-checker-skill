# Pathology Report Checker

> A comprehensive Claude skill for surgical pathology quality assurance and compliance checking

## Overview

The Pathology Report Checker is a professional tool for analyzing surgical pathology cancer reports against international standards. It helps pathologists and pathology departments ensure their reports meet CAP (College of American Pathologists), ICCR (International Collaboration on Cancer Reporting), and AAPA (American Association of Pathology Assistants) guidelines.

## Key Features

### 🔍 Compliance Checking
- Automated analysis against CAP and ICCR guidelines
- Severity-based scoring system (Critical/Major/Minor)
- Cross-validation of pT/pN staging with tumor measurements
- Comprehensive quality metrics (completeness, clarity, consistency)

### 🏥 Supported Tumor Types
- **Breast** invasive carcinoma (CAP Breast.Invasive protocol)
- **Colorectal** resection (CAP ColoRectal protocol)
- **Exocrine pancreas** carcinoma (CAP Panc.Exo protocol)
- **Gastric** carcinoma (CAP Stomach protocol)

### 📋 Template Generation
- Generate blank CAP-compliant synoptic templates
- Optional pre-fill with known values
- Available in English and Turkish
- Includes all required, conditional, and recommended elements

### 🔬 TNM Staging Validation
- AJCC 8th edition staging calculator
- Automatic verification of stage groups
- Cross-checks between pT categories and tumor size
- Validates pN categories against lymph node counts

### 📊 Additional Capabilities
- **Tumor Board Summaries**: Generate concise 3-5 line MDT summaries
- **Free-text Conversion**: Convert narrative reports to synoptic format
- **SNOMED Coding**: Suggest SNOMED CT and ICD-O-3 codes
- **Amendment Generation**: Create addenda and corrections
- **Auto-fill Suggestions**: Recommend pT/pN/Stage values based on context

### 🌐 Multi-Language Support
- Full support for English and Turkish
- Terminology mapping tables included
- Auto-detection of report language
- Responds in the same language as input

## Who Should Use This Skill?

- **Pathologists**: Ensure reports meet international standards before sign-out
- **Pathology Residents**: Learn required elements for different tumor types
- **Quality Assurance Teams**: Audit report completeness and consistency
- **Pathology Departments**: Standardize reporting practices across staff
- **Research Teams**: Validate staging and element completeness in retrospective studies

## Clinical Standards Referenced

This skill is built on authoritative clinical guidelines:
- **CAP** Cancer Protocol Templates (2024)
- **ICCR** Cancer Datasets (2nd edition)
- **AJCC** TNM Staging Manual (8th edition, 2017)
- **AAPA** Macroscopic Examination Guidelines (3rd edition)
- **WHO** Classification of Tumours (5th edition)

## How It Works

### Simple Trigger Phrases

**Compliance Checking:**
```
Check this breast report for CAP compliance
Is this colorectal pathology report complete?
Review this Whipple report against ICCR guidelines
```

**Template Generation:**
```
Generate a breast lumpectomy synoptic template
Create a CAP template for colorectal resection
Give me a gastric carcinoma report template
```

**TNM Staging:**
```
Calculate stage for pT2 N1 M0 breast cancer
Verify the staging in this report
What stage is pT3 N1b colorectal cancer?
```

**Tumor Board Summary:**
```
Generate a tumor board summary from this report
Create an MDT summary
Summarize this case for oncology
```

### Scoring System

Reports are scored based on missing elements:
- **Critical** elements (pT, pN, margins, grade): -15 points each
- **Major** elements (LVI, PNI, tumor size): -5 points each
- **Minor** elements (focality, gross details): -2 points each

**Score Interpretation:**
- **90-100**: ✅ COMPLIANT
- **70-89**: 🟡 INCOMPLETE - MINOR
- **50-69**: 🟠 INCOMPLETE - MAJOR
- **<50**: 🔴 INCOMPLETE - CRITICAL

### Cross-Validation

The skill automatically checks for inconsistencies:
- pT category must match tumor size (AJCC criteria)
- pN category must match positive lymph node count
- R classification must match margin distance (ICCR R1 ≤1mm)
- Minimum lymph node counts (12 for colorectal, 15 for breast)
- Gross vs microscopic concordance (size, margins, nodes)

## Installation

### Quick Install

1. Download or clone this skill
2. Copy to `~/.claude/skills/`
3. Restart Claude Code or reload skills

```bash
# Copy to skills directory
cp -r pathology-report-checker-skill ~/.claude/skills/

# Or create a symlink
ln -s /path/to/skill ~/.claude/skills/pathology-report-checker
```

### Usage

Simply paste or upload a pathology report and use a trigger phrase:

```bash
# In Claude.ai or Claude Code
Check this breast pathology report for CAP compliance
```

```bash
# Claude CLI
claude "Check this report for CAP compliance" < report.txt
claude "Generate breast lumpectomy template"
```

## Example Output

```
COMPLIANCE ANALYSIS
Tumor: Breast invasive carcinoma
Protocol: CAP Breast.Invasive

COMPLIANCE SCORE: 82/100
STATUS: 🟡 INCOMPLETE - MINOR

MISSING ELEMENTS (3):
🔴 CRITICAL (1):
  - ER/PR/HER2 status [receptor studies] (-15 points)

🟠 MAJOR (2):
  - Lymphovascular invasion status (-5 points)
  - Perineural invasion status (-5 points)

CROSS-VALIDATION:
✅ pT2 consistent with 2.3cm tumor size (AJCC 8th)
✅ pN1a consistent with 2 positive nodes
✅ Margins negative (5mm) - R0 classification correct

RECOMMENDATIONS:
1. Add immunohistochemistry results for ER, PR, HER2
2. Document LVI presence/absence
3. Document PNI presence/absence
```

## Advanced Features

For automated batch processing, folder monitoring, and integration with laboratory information systems, see the `.dev/` folder for Python scripts and detailed documentation.

## Disclaimer

This skill is designed to assist pathologists in quality assurance and does not replace clinical judgment. Always review generated content and verify against primary sources. The skill references published guidelines but may not reflect the most recent updates.

## Support & Contributing

- **Issues**: Report bugs or request features on GitHub
- **Contributing**: Pull requests welcome for new tumor types or features
- **Documentation**: See README.md and .dev/docs/ for detailed guides

## License

MIT License - Free for academic and commercial use

---

**Version**: 1.0.0
**Last Updated**: January 2025
**Compatibility**: Claude 3.5 Sonnet and later
