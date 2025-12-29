# Pathology Report Checker - Feature Roadmap

## Status Legend
- ⬜ Not started
- 🟡 In progress
- ✅ Completed

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
| A8 | Wilms tumor (nephroblastoma) | ⬜ | High | Pediatric, COG protocols |
| A9 | Neuroblastoma | ⬜ | High | Pediatric, INPC classification |
| A10 | Hepatoblastoma | ⬜ | High | Pediatric, PRETEXT staging |
| A11 | Rhabdomyosarcoma | ⬜ | High | Pediatric soft tissue |
| A12 | Biopsy specimens | ⬜ | Medium | Different requirements than resections |

---

## B. Report Generation

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| B1 | Synoptic template generator | ✅ | High | Generate blank template with all required fields |
| B2 | Auto-fill suggestions | ✅ | High | Suggest pT/pN/Stage based on context |
| B3 | Free-text → Synoptic converter | ✅ | Medium | Convert narrative reports to structured CAP format |
| B4 | Amendment generator | ✅ | Medium | Generate addendum/correction/amended report text |

---

## C. Coding & Integration

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| C1 | SNOMED CT codes | ✅ | Medium | Morphology/topography codes, ICD-O-3 |
| C2 | ICD-O-3 codes | ✅ | Medium | Included with SNOMED CT |
| C3 | TNM stage calculator | ✅ | High | AJCC 8th, input pT/pN/pM → stage group |
| C4 | Tumor board summary | ✅ | High | Concise 3-5 line MDT summary generator |

---

## D. Biomarker Protocols

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| D1 | HER2 scoring validation | ⬜ | Medium | Validate IHC 0/1+/2+/3+, FISH interpretation |
| D2 | MMR/MSI reporting | ⬜ | Medium | Check MLH1, MSH2, MSH6, PMS2 completeness |
| D3 | PD-L1 scoring | ⬜ | Medium | TPS/CPS validation by tumor type |
| D4 | Molecular panel | ⬜ | Low | KRAS, BRAF, EGFR, ALK, ROS1, etc. |

---

## E. Analytics & Reporting

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| E1 | Department dashboard | ⬜ | Medium | Visualize compliance trends over time |
| E2 | Pathologist comparison | ⬜ | Low | Compare compliance rates (anonymized) |
| E3 | Turnaround tracking | ⬜ | Low | Correlate completeness with TAT |
| E4 | Custom KPIs | ⬜ | Medium | Department-specific quality metrics |

---

## F. Educational

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| F1 | Training mode | ⬜ | Medium | Detailed explanations for residents |
| F2 | Clinical impact notes | ⬜ | Medium | Why each missing element matters |
| F3 | Case examples | ✅ | Low | Sample reports in samples/ folder |

---

## G. Workflow

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| G1 | Watch folder | ✅ | Low | Auto-process new reports in monitored directory |
| G2 | LIS integration | ⬜ | Low | API for lab information systems |
| G3 | Amendment tracking | ⬜ | Medium | Compare original vs amended reports |
| G4 | Prior comparison | ⬜ | Low | Compare to patient's previous pathology |

---

## H. Macroscopy/Gross Description

| # | Feature | Status | Priority | Notes |
|---|---------|--------|----------|-------|
| H1 | Gross description completeness | ✅ | High | AAPA guidelines, specimen-specific elements |
| H2 | Gross vs Diagnosis validation | ✅ | High | Size, margins, nodes, extent discrepancies |
| H3 | Specimen-specific requirements | ✅ | High | TME grading, Whipple margins, etc. |

---

## Implementation Order (Suggested)

### Phase 1: Core Expansion
1. ✅ H1-H3 - Macroscopy checker
2. ✅ A1 - Gastric carcinoma
3. ✅ C3 - TNM stage calculator
4. ✅ B1 - Synoptic template generator

### Phase 2: Pediatric Focus
5. A8 - Wilms tumor
6. A9 - Neuroblastoma
7. A10 - Hepatoblastoma

### Phase 3: Common Tumors
8. A2 - Lung carcinoma
9. A3 - Prostate carcinoma
10. A4 - Thyroid carcinoma

### Phase 4: Clinical Tools
11. C4 - Tumor board summary
12. B2 - Auto-fill suggestions
13. D2 - MMR/MSI reporting

### Phase 5: Analytics
14. E1 - Department dashboard
15. E4 - Custom KPIs

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
| AAPA Guidelines | 2024-12-28 | Merged into macroscopy files (breast, colorectal, pancreas, gastric) |
| Tumor board summary | 2024-12-28 | Concise 3-5 line MDT summary generator, EN+TR |
| Free-text → Synoptic | 2024-12-29 | Convert narrative reports to structured CAP format |
| Auto-fill suggestions | 2024-12-29 | Suggest pT/pN/Stage based on tumor characteristics |
| Amendment generator | 2024-12-29 | Addendum/correction/amended report templates |
| Watch folder | 2024-12-29 | Auto-process new reports dropped into directory |
| Documentation split | 2024-12-29 | SKILL.md split into modular docs/ folder |
| Sample reports | 2024-12-29 | 10 synthetic test cases (EN+TR, complete/incomplete/errors) |

---

## Notes

- All tumor types should include Turkish terminology mapping
- Reference files follow same structure: Core → Conditional → Recommended
- Cross-validation rules are tumor-specific (different staging systems)
- Pediatric tumors may use COG/SIOP protocols instead of CAP
- Macroscopy checker works with any specimen type
