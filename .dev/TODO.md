# Pathology Report Checker - Feature Roadmap

## Status Legend
- ⬜ Not started
- 🟡 In progress
- ✅ Completed
- 🔵 New suggestion

---

## Progress Overview

| Section | Completed | Total | Progress |
|---------|-----------|-------|----------|
| A. Tumor Types | 1 | 12 | 8% |
| B. Report Generation | 4 | 4 | 100% ✅ |
| C. Coding & Integration | 4 | 4 | 100% ✅ |
| D. Biomarker Protocols | 0 | 4 | 0% ⚠️ |
| E. Analytics | 0 | 4 | 0% |
| F. Educational | 1 | 3 | 33% |
| G. Workflow | 1 | 4 | 25% |
| H. Macroscopy | 3 | 3 | 100% ✅ |
| I. Quality & Testing | 0 | 4 | 0% (NEW) |
| J. Clinical Safety | 0 | 3 | 0% (NEW) |
| **Overall** | **14** | **45** | **31%** |

---

## A. More Tumor Types

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| A1 | Gastric carcinoma | ✅ | High | CAP Stomach, ICCR Gastric |
| A2 | Lung carcinoma (NSCLC) | ⬜ | High | Complex staging, multiple subtypes |
| A3 | Prostate carcinoma | ⬜ | High | Gleason/ISUP Grade Group validation |
| A4 | Thyroid carcinoma | ⬜ | Medium | Papillary, follicular, medullary, anaplastic |
| A5 | Renal cell carcinoma | ⬜ | Medium | Clear cell, papillary, chromophobe |
| A6 | Endometrial carcinoma | ⬜ | Medium | FIGO staging, molecular classification |
| A7 | Ovarian carcinoma | ⬜ | Medium | Pediatric cases relevant |
| A8 | Wilms tumor (nephroblastoma) | ⬜ | **Critical** | Pediatric, COG protocols |
| A9 | Neuroblastoma | ⬜ | **Critical** | Pediatric, INPC classification |
| A10 | Hepatoblastoma | ⬜ | **Critical** | Pediatric, PRETEXT staging |
| A11 | Rhabdomyosarcoma | ⬜ | High | Pediatric soft tissue |
| A12 | Biopsy specimens | ⬜ | Medium | Different requirements than resections |

### Suggested Additions (Section A)
| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| A13 | 🔵 Melanoma | ⬜ | Medium | Breslow thickness, Clark level, ulceration |
| A14 | 🔵 Soft tissue sarcoma (adult) | ⬜ | Low | FNCLCC grading |
| A15 | 🔵 CNS tumors | ⬜ | Low | WHO 2021 classification, molecular |

---

## B. Report Generation (COMPLETE ✅)

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| B1 | Synoptic template generator | ✅ | High | Generate blank template with all required fields |
| B2 | Auto-fill suggestions | ✅ | High | Suggest pT/pN/Stage based on context |
| B3 | Free-text → Synoptic converter | ✅ | Medium | Convert narrative reports to structured CAP format |
| B4 | Amendment generator | ✅ | Medium | Generate addendum/correction/amended report text |

### Suggested Additions (Section B)
| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| B5 | 🔵 Report comparison (diff) | ⬜ | Low | Compare two versions, highlight changes |
| B6 | 🔵 Template customization | ⬜ | Low | Department-specific template variants |

---

## C. Coding & Integration (COMPLETE ✅)

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| C1 | SNOMED CT codes | ✅ | Medium | Morphology/topography codes, ICD-O-3 |
| C2 | ICD-O-3 codes | ✅ | Medium | Included with SNOMED CT |
| C3 | TNM stage calculator | ✅ | High | AJCC 8th, input pT/pN/pM → stage group |
| C4 | Tumor board summary | ✅ | High | Concise 3-5 line MDT summary generator |

### Suggested Additions (Section C)
| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| C5 | 🔵 ICD-10-CM codes | ⬜ | Low | Diagnosis codes for billing |
| C6 | 🔵 CPT codes | ⬜ | Low | Procedure codes for billing |

---

## D. Biomarker Protocols ⚠️ (0% - HIGH PRIORITY)

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| D1 | HER2 scoring validation | ⬜ | **High** | Validate IHC 0/1+/2+/3+, FISH interpretation |
| D2 | MMR/MSI reporting | ⬜ | **High** | Check MLH1, MSH2, MSH6, PMS2 completeness |
| D3 | PD-L1 scoring | ⬜ | Medium | TPS/CPS validation by tumor type |
| D4 | Molecular panel | ⬜ | Low | KRAS, BRAF, EGFR, ALK, ROS1, etc. |

### Why This Section Matters
- Biomarker errors directly affect treatment decisions
- HER2 status determines eligibility for targeted therapy
- MMR status affects immunotherapy and Lynch syndrome screening
- Missing biomarkers = incomplete staging for treatment planning

### Suggested Additions (Section D)
| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| D5 | 🔵 ER/PR interpretation | ⬜ | High | Allred score, % positive, intensity |
| D6 | 🔵 Ki-67 interpretation | ⬜ | Medium | Threshold validation by tumor type |
| D7 | 🔵 Biomarker turnaround | ⬜ | Low | Flag if biomarkers pending >48 hours |

---

## E. Analytics & Reporting

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| E1 | Department dashboard | ⬜ | Medium | Visualize compliance trends over time |
| E2 | Pathologist comparison | ⬜ | Low | Compare compliance rates (anonymized) |
| E3 | Turnaround tracking | ⬜ | Low | Correlate completeness with TAT |
| E4 | Custom KPIs | ⬜ | Medium | Department-specific quality metrics |

### Suggested Additions (Section E)
| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| E5 | 🔵 Compliance trending | ⬜ | Medium | Track improvement over time |
| E6 | 🔵 Common error analysis | ⬜ | Medium | Identify most frequent gaps |
| E7 | 🔵 Export to Excel/PDF | ⬜ | Low | Formatted reports for QA meetings |

---

## F. Educational

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| F1 | Training mode | ⬜ | Medium | Detailed explanations for residents |
| F2 | Clinical impact notes | ⬜ | **High** | Why each missing element matters |
| F3 | Case examples | ✅ | Low | Sample reports in samples/ folder |

### Why F2 (Clinical Impact) Matters
Every missing element should explain:
- **What**: Element definition
- **Why**: Clinical significance
- **Impact**: What happens if missing
- **Action**: How to fix

Example:
```
pN Category (CRITICAL)
- What: Lymph node stage based on positive node count
- Why: Determines need for adjuvant therapy
- Impact: Cannot calculate stage, delays treatment planning
- Action: Count positive nodes, apply AJCC criteria
```

### Suggested Additions (Section F)
| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| F4 | 🔵 Common pitfalls guide | ⬜ | Medium | Frequent mistakes and how to avoid |
| F5 | 🔵 Quiz mode | ⬜ | Low | Test knowledge of required elements |
| F6 | 🔵 Before/after examples | ⬜ | Medium | Show correction process |

---

## G. Workflow

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| G1 | Watch folder | ✅ | Low | Auto-process new reports in monitored directory |
| G2 | LIS integration | ⬜ | Low | API for lab information systems |
| G3 | Amendment tracking | ⬜ | Medium | Compare original vs amended reports |
| G4 | Prior comparison | ⬜ | Low | Compare to patient's previous pathology |

### Suggested Additions (Section G)
| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| G5 | 🔵 Slack/Teams notifications | ⬜ | Low | Alert on critical gaps |
| G6 | 🔵 Email digest | ⬜ | Low | Daily summary of processed reports |

---

## H. Macroscopy/Gross Description (COMPLETE ✅)

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| H1 | Gross description completeness | ✅ | High | AAPA guidelines, specimen-specific elements |
| H2 | Gross vs Diagnosis validation | ✅ | High | Size, margins, nodes, extent discrepancies |
| H3 | Specimen-specific requirements | ✅ | High | TME grading, Whipple margins, etc. |

---

## I. Quality & Testing (NEW SECTION)

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| I1 | 🔵 Unit tests | ⬜ | Medium | Automated tests for each tumor type |
| I2 | 🔵 Regression testing | ⬜ | Medium | Ensure updates don't break existing |
| I3 | 🔵 Sample report expansion | ⬜ | Low | More edge cases (rare tumors, unusual presentations) |
| I4 | 🔵 Validation against CAP checklists | ⬜ | High | Verify reference files match current CAP protocols |

---

## J. Clinical Safety (NEW SECTION)

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| J1 | 🔵 Critical alert system | ⬜ | **High** | Highlight life-threatening omissions |
| J2 | 🔵 Staging error prevention | ⬜ | **High** | Block obvious errors (pT3 for 1cm tumor) |
| J3 | 🔵 Treatment implication flags | ⬜ | High | Note which gaps affect treatment decisions |

### Clinical Safety Examples
```
⚠️ CRITICAL SAFETY ALERT
Missing HER2 status for breast cancer.
Treatment Implication: Cannot determine eligibility for 
trastuzumab (Herceptin). Delays treatment initiation.
Action Required: Order HER2 testing immediately.
```

---

## K. Documentation (NEW SECTION)

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| K1 | 🔵 CHANGELOG.md | ⬜ | Low | Track version changes |
| K2 | 🔵 Troubleshooting guide | ⬜ | Medium | Common errors and solutions |
| K3 | 🔵 FAQ | ⬜ | Low | User questions |
| K4 | 🔵 Video tutorials | ⬜ | Low | Screen recordings of usage |

---

## Implementation Order (REVISED)

### Phase 1: Core Expansion ✅ COMPLETE
1. ✅ H1-H3 - Macroscopy checker
2. ✅ A1 - Gastric carcinoma
3. ✅ C3 - TNM stage calculator
4. ✅ B1-B4 - Report generation tools
5. ✅ F3 - Sample reports

### Phase 2: Clinical Safety (NEXT PRIORITY)
6. **D1 - HER2 scoring validation**
7. **D2 - MMR/MSI reporting**
8. **F2 - Clinical impact notes**
9. **J1 - Critical alert system**

### Phase 3: Pediatric Tumors (YOUR SPECIALTY)
10. **A8 - Wilms tumor** (COG staging, favorable vs unfavorable histology)
11. **A9 - Neuroblastoma** (INPC, MYCN, risk stratification)
12. **A10 - Hepatoblastoma** (PRETEXT, risk groups)
13. A11 - Rhabdomyosarcoma

### Phase 4: Common Adult Tumors
14. A2 - Lung carcinoma (NSCLC)
15. A3 - Prostate carcinoma (Gleason/ISUP)
16. A4 - Thyroid carcinoma

### Phase 5: Quality & Analytics
17. I4 - CAP checklist validation
18. E1 - Department dashboard
19. E6 - Common error analysis

### Phase 6: Advanced Features
20. G3 - Amendment tracking
21. E5 - Compliance trending
22. F1 - Training mode

---

## Quick Wins (< 2 hours each)

| Task | Effort | Impact | Priority |
|------|--------|--------|----------|
| F2 - Clinical impact notes (for existing tumors) | Low | High | ⭐⭐⭐ |
| D5 - ER/PR interpretation rules | Low | High | ⭐⭐⭐ |
| K1 - CHANGELOG.md | Low | Medium | ⭐⭐ |
| F4 - Common pitfalls guide | Medium | High | ⭐⭐⭐ |
| I3 - More sample reports | Low | Medium | ⭐⭐ |

---

## Completed Features

| Feature | Date | Notes |
|---------|------|-------|
| Breast invasive carcinoma | 2024-12-27 | CAP + ICCR |
| Colorectal resection | 2024-12-27 | CAP + ICCR |
| Exocrine pancreas | 2024-12-28 | CAP + ICCR |
| Severity scoring | 2024-12-28 | Critical/Major/Minor |
| Empty vs Missing detection | 2024-12-28 | Field status |
| Cross-validation | 2024-12-28 | pT/size, pN/nodes, margin/R |
| Quality metrics | 2024-12-28 | Completeness, clarity, consistency |
| Trend tracking | 2024-12-28 | Historical JSON data |
| Batch processing (LLM) | 2024-12-28 | Claude API |
| CLI folder mode | 2024-12-28 | Images, PDFs, text files |
| CLI Excel/CSV mode | 2024-12-28 | Spreadsheet input |
| Macroscopy checker | 2024-12-28 | AAPA guidelines, gross vs diagnosis |
| Gastric carcinoma | 2024-12-28 | CAP + ICCR, Borrmann, Laurén, HER2 |
| TNM stage calculator | 2024-12-28 | AJCC 8th, breast/colorectal/pancreas/gastric |
| Synoptic template generator | 2024-12-28 | Blank CAP templates, all tumor types, TR+EN |
| SNOMED CT / ICD-O-3 coding | 2024-12-28 | Morphology, topography, behavior, grade codes |
| AAPA Guidelines | 2024-12-28 | Merged into macroscopy files |
| Tumor board summary | 2024-12-28 | Concise 3-5 line MDT summary generator, EN+TR |
| Free-text → Synoptic | 2024-12-29 | Convert narrative reports to structured CAP format |
| Auto-fill suggestions | 2024-12-29 | Suggest pT/pN/Stage based on tumor characteristics |
| Amendment generator | 2024-12-29 | Addendum/correction/amended report templates |
| Watch folder | 2024-12-29 | Auto-process new reports dropped into directory |
| Documentation split | 2024-12-29 | SKILL.md split into modular docs/ folder |
| Sample reports | 2024-12-29 | 10 synthetic test cases (EN+TR, complete/incomplete/errors) |
| CHANGELOG.md | 2024-12-29 | Version history with detailed changes |

---

## Notes

- All tumor types should include Turkish terminology mapping
- Reference files follow same structure: Core → Conditional → Recommended
- Cross-validation rules are tumor-specific (different staging systems)
- Pediatric tumors use COG/SIOP protocols instead of CAP
- Macroscopy checker works with any specimen type
- **Priority should reflect your practice focus (pediatric pathology)**
- **Biomarker validation is clinically critical but currently 0% complete**
- **Clinical impact notes add significant educational value with low effort**
