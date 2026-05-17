# Skill Improvement Plan (Skill-Creator Analysis)

**Analysis Date**: January 17, 2026
**Analyzed Skill**: pathology-report-checker v1.0.0
**Framework**: Anthropic skill-creator best practices

---

## Executive Summary

The pathology-report-checker skill is **well-structured** but has opportunities for optimization based on skill-creator principles. Key improvements focus on: fixing broken references, adding table of contents to large files, creating utility scripts, and enhancing progressive disclosure.

**Overall Grade**: B+ (Good structure, needs refinement)

---

## 1. Conciseness Analysis ✅ GOOD

### Current State
- **SKILL.md**: 230 lines (well under 500 limit) ✅
- **Description**: 669 characters (under 1024 limit) ✅
- **Assumes Claude intelligence**: Mostly good ✅

### Issues Found
❌ **Line 118**: `> 📋 **See also:** docs/FEATURES.md for detailed feature documentation`
❌ **Line 154**: `> 📋 **See also:** docs/USAGE.md for detailed usage instructions`
❌ **Lines 219-226**: References to `docs/` which is now in `.dev/` (not accessible to users)

### Recommended Fix
```markdown
# REMOVE these lines (docs/ is in .dev/ now):
- Line 118: > 📋 **See also:** `docs/FEATURES.md`...
- Line 154: > 📋 **See also:** `docs/USAGE.md`...
- Lines 219-226: Documentation table with docs/ references

# KEEP only what users need in SKILL.md
```

**Impact**: Medium - Broken references confuse Claude
**Effort**: Low - Simple deletion

---

## 2. Progressive Disclosure ⚠️ NEEDS IMPROVEMENT

### Current State
✅ **Good**: Reference files organized by domain (diagnosis/, macroscopy/, etc.)
✅ **Good**: Clear navigation table mapping tumor types to files
⚠️ **Issue**: Large reference files lack table of contents

### Large Files (>100 lines) Without TOC

| File | Lines | Needs TOC? |
|------|-------|-----------|
| `synoptic_templates.md` | 942 | ✅ YES - Critical |
| `synoptic_templates_tr.md` | 906 | ✅ YES - Critical |
| `amendment_generator.md` | 687 | ✅ YES |
| `freetext_to_synoptic.md` | 553 | ✅ YES |
| `autofill_suggestions.md` | 559 | ✅ YES |
| `colorectal_macroscopy.md` | 550 | ✅ YES |
| `tnm_stage_calculator.md` | 493 | ✅ YES |
| `gastric_macroscopy.md` | 466 | ⚠️ Maybe |
| `snomed_ct_codes.md` | 464 | ⚠️ Maybe |
| `pancreas_macroscopy.md` | 456 | ⚠️ Maybe |

### Recommended Fix

**Add table of contents to all files >100 lines:**

```markdown
# Synoptic Template Generator

## Contents
- [Usage](#usage)
- [Template Format Standards](#template-format-standards)
- [Breast Invasive Carcinoma Template](#breast-invasive-carcinoma-template)
  - Lumpectomy / Partial Mastectomy
  - Total Mastectomy
- [Colorectal Resection Template](#colorectal-resection-template)
  - Colon Resection
  - Rectal Resection
- [Pancreas Template](#pancreas-template)
  - Whipple (Pancreaticoduodenectomy)
  - Distal Pancreatectomy
- [Gastric Carcinoma Template](#gastric-carcinoma-template)
  - Total Gastrectomy
  - Partial Gastrectomy

---

[Rest of file...]
```

**Impact**: High - Enables Claude to see full scope even with partial reads
**Effort**: Medium - Add TOC to 10+ files

---

## 3. Search Pattern Enhancement 🚀 NEW FEATURE

### Current State
❌ **Missing**: No grep search patterns for large reference files

### Recommended Addition

Add to SKILL.md after "Reference Files" section:

```markdown
## Quick Search Patterns

For large reference files, use grep to find specific content:

**Find tumor type template:**
```bash
grep -A 50 "## Breast Invasive" references/templates/synoptic_templates.md
grep -A 50 "## Colorectal" references/templates/synoptic_templates.md
```

**Find specific staging table:**
```bash
grep -A 20 "Breast Cancer Stage" references/staging/tnm_stage_calculator.md
grep -A 20 "Pancreas Stage" references/staging/tnm_stage_calculator.md
```

**Find SNOMED code:**
```bash
grep -i "ductal carcinoma" references/coding/snomed_ct_codes.md
grep -i "adenocarcinoma" references/coding/snomed_ct_codes.md
```

**Find amendment template type:**
```bash
grep -A 15 "Addendum Template" references/amendments/amendment_generator.md
grep -A 15 "Correction Template" references/amendments/amendment_generator.md
```
```

**Impact**: High - Much faster navigation of large files
**Effort**: Low - Add one section to SKILL.md

---

## 4. Utility Scripts 🎯 OPPORTUNITY

### Current State
✅ **Good**: Python scripts exist in `.dev/scripts/`
❌ **Issue**: Scripts are excluded from skill package (.skillignore)

### Skill-Creator Principle
Scripts bundled in the skill are:
- More reliable than generated code
- Token-efficient (execute without loading into context)
- Ensure consistency

### Recommended Addition

**Create `scripts/` folder in skill root** (not .dev/) with utility scripts:

```
pathology-report-checker-skill/
├── SKILL.md
├── scripts/                    # NEW - Bundled utilities
│   ├── validate_staging.py    # Validate pT/pN against size/nodes
│   ├── calculate_score.py     # Calculate compliance score
│   ├── extract_elements.py    # Extract elements from report text
│   └── check_consistency.py   # Cross-validation checks
└── references/
```

**Example: validate_staging.py**

```python
#!/usr/bin/env python3
"""
Validate TNM staging consistency
Usage: python scripts/validate_staging.py --pt T2 --size 2.3 --tumor-type breast
"""
import argparse

def validate_pt_size(pt_category, size_cm, tumor_type):
    """Returns True if pT matches tumor size per AJCC 8th"""
    staging_rules = {
        'breast': {
            'T1': (0, 2.0),
            'T2': (2.0, 5.0),
            'T3': (5.0, float('inf'))
        },
        'colorectal': {
            'T1': 'submucosa',
            'T2': 'muscularis',
            'T3': 'subserosa',
            'T4': 'peritoneum'
        }
    }
    # Validation logic here
    return True, "Valid"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pt', required=True)
    parser.add_argument('--size', type=float)
    parser.add_argument('--tumor-type', required=True)
    args = parser.parse_args()

    valid, msg = validate_pt_size(args.pt, args.size, args.tumor_type)
    print(f"{'✓' if valid else '✗'} {msg}")
```

**Update SKILL.md to reference scripts:**

```markdown
## Validation Utilities

For critical validation tasks, use the bundled scripts:

**Validate staging consistency:**
```bash
python scripts/validate_staging.py --pt T2 --size 2.3 --tumor-type breast
```

**Calculate compliance score:**
```bash
python scripts/calculate_score.py --critical 1 --major 2 --minor 3
# Output: Score: 77/100 (INCOMPLETE - MINOR)
```

**Extract elements from report:**
```bash
python scripts/extract_elements.py report.txt
# Output: JSON with extracted elements
```
```

**Impact**: High - More reliable, faster execution
**Effort**: High - Create 4 utility scripts

---

## 5. Workflow Improvements 📋 ENHANCEMENT

### Current State
✅ **Good**: Clear 6-step workflow
⚠️ **Could improve**: Add validation checkpoints

### Recommended Enhancement

Add feedback loop pattern:

```markdown
## Core Workflow (with Validation)

### Step 1: Determine Report Type
From report content, identify organ, specimen type, and tumor type.

### Step 2: Load Reference Files
Load the appropriate diagnosis and macroscopy reference files.

### Step 3: Extract Elements
Parse report text using terminology equivalents (EN/TR).

**→ Validation checkpoint**: Run `scripts/extract_elements.py` to verify extraction

### Step 4: Analyze
- **4a**: Check for missing/empty elements by severity
- **4b**: Cross-validate (pT vs size, pN vs nodes, margins vs R)
  - **→ Use**: `scripts/validate_staging.py` for cross-validation
- **4c**: Calculate quality metrics
  - **→ Use**: `scripts/calculate_score.py` for scoring
- **4d**: Check macroscopy/gross description

### Step 5: Generate Output
Produce QA report with compliance score.

**→ Validation checkpoint**: Review score and ensure all checks passed

### Step 6: Verify Staging
Cross-check pTNM categories against stage group.

**→ Use**: `references/staging/tnm_stage_calculator.md`
```

**Impact**: Medium - Clearer validation
**Effort**: Low - Add validation notes

---

## 6. Conditional Workflow Pattern 🔄 ENHANCEMENT

### Current State
❌ **Missing**: No guidance on which mode to use

### Recommended Addition

```markdown
## Mode Selection Guide

Determine the task type before proceeding:

**User wants compliance checking?** → Follow "Compliance Check Workflow"
**User wants template generation?** → Follow "Template Generation Workflow"
**User wants tumor board summary?** → Follow "Summary Generation Workflow"
**User wants staging calculation only?** → Read `references/staging/tnm_stage_calculator.md`

### Compliance Check Workflow
1. Determine report type
2. Load diagnosis + macroscopy references
3. Extract elements
4. Analyze and score
5. Generate QA report

### Template Generation Workflow
1. Identify tumor type and specimen
2. Read `references/templates/synoptic_templates.md` (or `_tr.md` for Turkish)
3. Use grep to find specific template: `grep -A 100 "## Breast Invasive"`
4. Optionally pre-fill with provided values
5. Return formatted template

### Summary Generation Workflow
1. Extract key findings from report
2. Read `references/summaries/tumor_board_summary.md`
3. Generate 3-5 line MDT summary
4. Follow format examples in reference
```

**Impact**: High - Clearer task routing
**Effort**: Low - Add one section

---

## 7. Language Detection Enhancement 🌐 IMPROVEMENT

### Current State
✅ **Good**: Mentions language handling
⚠️ **Could improve**: Add explicit detection guidance

### Recommended Addition

```markdown
## Language Detection

**Auto-detect language from report content:**

1. Scan for Turkish keywords:
   - "invaziv", "karsinom", "lenfovasküler", "sinir", "pozitif"
2. Scan for English keywords:
   - "invasive", "carcinoma", "lymphovascular", "perineural", "positive"
3. If both present, prefer language with more matches
4. Default to English if unclear

**Use the same language for output:**
- Turkish report → Turkish QA report
- English report → English QA report

**Terminology tables in reference files:**
All diagnosis references include English ↔ Turkish mapping tables.
```

**Impact**: Medium - Clearer language handling
**Effort**: Low - Add explicit guidance

---

## 8. Example Pattern Addition 📝 ENHANCEMENT

### Current State
⚠️ **Limited**: Only one tumor board summary example

### Recommended Addition

Add examples for each major mode:

```markdown
## Output Examples

### Compliance Check Example

**Input:** Breast lumpectomy report with missing ER/PR/HER2

**Output:**
```
COMPLIANCE ANALYSIS - Breast Invasive Carcinoma
Protocol: CAP Breast.Invasive

SCORE: 85/100
STATUS: 🟡 INCOMPLETE - MINOR

MISSING CRITICAL ELEMENTS (1):
🔴 ER/PR/HER2 status (-15 points)

RECOMMENDATIONS:
1. Add immunohistochemistry for ER, PR, HER2
```

### Template Generation Example

**Input:** "Generate breast lumpectomy template for 2.3cm Grade 2 IDC"

**Output:**
```
═══════════════════════════════════════
BREAST - INVASIVE CARCINOMA
Lumpectomy / Partial Mastectomy
═══════════════════════════════════════

SPECIMEN:
* Procedure: Lumpectomy, left breast
* Laterality: Left

TUMOR:
* Tumor Site: ___
* Histologic Type: Invasive ductal carcinoma (pre-filled)
* Histologic Grade: Grade 2 (pre-filled)
* Tumor Size: 2.3 cm (pre-filled)
[...]
```

### Staging Validation Example

**Input:** "Is pT2 N1 M0 Stage IIB correct for breast cancer?"

**Output:**
```
✅ YES - Staging is correct

pT2 (tumor >2cm, ≤5cm) + N1 (1-3 positive nodes) + M0 = Stage IIB

Reference: AJCC 8th Edition Breast Cancer Staging
```
```

**Impact**: High - Clearer output expectations
**Effort**: Medium - Create examples for each mode

---

## 9. Reference File Organization 🗂️ OPTIMIZATION

### Current State
✅ **Good**: Organized by domain
⚠️ **Could improve**: Add index files for each domain

### Recommended Addition

Create index files for each reference subdirectory:

**references/diagnosis/INDEX.md:**
```markdown
# Diagnosis Reference Index

Quick navigation for CAP/ICCR required elements:

## Available Tumor Types
- [Breast Invasive Carcinoma](breast_invasive_carcinoma.md) - 206 lines
- [Colorectal Resection](colorectal_resection.md) - 257 lines
- [Exocrine Pancreas](exocrine_pancreas.md) - 274 lines
- [Gastric Carcinoma](gastric_carcinoma.md) - 348 lines

## Quick Search
```bash
# Find specific element
grep -r "margin" references/diagnosis/
grep -r "lymphovascular" references/diagnosis/
```

## Common Elements Across All Types
- pT category
- pN category
- Histologic type
- Histologic grade
- Margins
- Lymphovascular invasion
- Regional lymph nodes examined/positive
```

**Impact**: Medium - Faster navigation
**Effort**: Medium - Create 6 index files

---

## 10. Error Handling Guidance 🛡️ NEW ADDITION

### Current State
❌ **Missing**: No guidance on handling errors or edge cases

### Recommended Addition

```markdown
## Handling Edge Cases

### Unknown Tumor Type
If report doesn't match supported types:
1. Inform user: "This skill supports breast, colorectal, pancreas, gastric"
2. Offer generic analysis: staging validation, SNOMED coding
3. Suggest which tumor type is closest

### Incomplete Report
If report is too brief to analyze:
1. Extract what's available
2. Note: "Report appears incomplete, limited analysis possible"
3. Suggest minimum required elements

### Mixed Languages
If report contains both English and Turkish:
1. Detect dominant language (count keyword frequency)
2. Respond in dominant language
3. Note: "Report contains mixed terminology"

### Conflicting Information
If report has contradictions (e.g., size 1.5cm but pT3):
1. Flag as cross-validation error
2. List all conflicts
3. Suggest corrections
4. Do NOT attempt to "fix" - report the discrepancy

### Missing Reference Files
If a reference file is not found:
1. Check file path in SKILL.md reference table
2. Inform user which reference is missing
3. Offer alternative (e.g., use common macroscopy if specific missing)
```

**Impact**: High - More robust error handling
**Effort**: Low - Add guidance section

---

## Implementation Priority

### 🔴 High Priority (Do First)

1. **Fix broken docs/ references** (Lines 118, 154, 219-226)
   - **Effort**: 15 minutes
   - **Impact**: Prevents confusion

2. **Add table of contents to large files** (10 files >100 lines)
   - **Effort**: 2-3 hours
   - **Impact**: Major improvement in navigation

3. **Add search patterns section**
   - **Effort**: 30 minutes
   - **Impact**: Much faster file navigation

4. **Add conditional workflow pattern**
   - **Effort**: 45 minutes
   - **Impact**: Clearer mode selection

### 🟡 Medium Priority (Do Next)

5. **Add example outputs**
   - **Effort**: 1-2 hours
   - **Impact**: Clearer expectations

6. **Add error handling guidance**
   - **Effort**: 1 hour
   - **Impact**: More robust

7. **Create index files for reference subdirectories**
   - **Effort**: 1 hour
   - **Impact**: Better organization

### 🟢 Low Priority (Nice to Have)

8. **Create utility scripts** (validate_staging.py, calculate_score.py, etc.)
   - **Effort**: 4-6 hours
   - **Impact**: More reliable validation

9. **Enhance language detection**
   - **Effort**: 30 minutes
   - **Impact**: Minor clarity improvement

10. **Add workflow validation checkpoints**
    - **Effort**: 30 minutes
    - **Impact**: Minor clarity improvement

---

## Estimated Total Effort

- **High Priority**: 4-5 hours
- **Medium Priority**: 3-4 hours
- **Low Priority**: 5-7 hours

**Total**: 12-16 hours for complete implementation

---

## Expected Improvements

### Token Efficiency
- **Before**: May load full 942-line template file
- **After**: Use grep to load only relevant section (50-100 lines)
- **Savings**: ~850 tokens per template generation

### Navigation Speed
- **Before**: Read full file to find content
- **After**: Use TOC or grep to jump directly
- **Improvement**: 3-5x faster for large files

### Reliability
- **Before**: Claude generates validation logic
- **After**: Execute pre-built validation scripts
- **Improvement**: More consistent, faster

### User Experience
- **Before**: May be confused by broken references
- **After**: Clear, working references
- **Improvement**: Professional, polished

---

## Testing Plan

### After Implementation

1. **Test each mode**:
   - Compliance checking with sample reports
   - Template generation for each tumor type
   - Tumor board summaries
   - Staging validation
   - SNOMED coding

2. **Test edge cases**:
   - Unknown tumor types
   - Mixed language reports
   - Incomplete reports
   - Conflicting information

3. **Test search patterns**:
   - Grep commands for each large file
   - Verify TOC links work

4. **Test with different models**:
   - Haiku (fast, economical)
   - Sonnet (balanced)
   - Opus (powerful)

---

## Conclusion

The pathology-report-checker skill is **well-designed** but has **concrete opportunities for optimization** following skill-creator principles:

**Strengths:**
- ✅ Good structure and organization
- ✅ Appropriate conciseness
- ✅ Clear progressive disclosure
- ✅ Comprehensive reference files

**Key Improvements:**
- 🔧 Fix broken docs/ references (critical)
- 🔧 Add table of contents to large files (high impact)
- 🔧 Add search patterns (high impact, low effort)
- 🔧 Add conditional workflows (clarity)

**Recommended Approach:**
1. Implement high-priority fixes first (4-5 hours)
2. Test thoroughly with sample reports
3. Gather user feedback
4. Implement medium-priority enhancements
5. Consider utility scripts for future iteration

This plan follows the skill-creator philosophy: **start with high-impact, low-effort improvements, then iterate based on real usage**.
