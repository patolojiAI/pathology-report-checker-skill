# Changelog

All notable changes to the Pathology Report Checker skill.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.2.0] - 2026-05-31

### Added
- **`.skill` packaging**: `.dev/scripts/build_skill.py` builds a self-contained
  `dist/pathology-report-checker.skill` (SKILL.md + `references/` + `examples/`),
  uploadable via **Claude.ai → Settings → Capabilities → Skills → Upload skill**.
  The build honours `.skillignore`, so dev tooling, docs, and the website never
  ship inside the skill.
- **GitHub Pages project website** under `docs/` (`index.md` + `_config.yml`):
  usage guide, the ECDP2026 abstract (embedded PDF), the acceptance
  notification, the Hugging Face demo, and a citation.
- **Academic context**: README and website document the **ECDP2026 oral
  presentation** — *“A Skill for Large Language Models to Evaluate Pathology
  Report Quality”* (22nd European Congress on Digital Pathology, Graz, 19 June
  2026, Structured Reporting session) — plus a "How to cite" entry.
- README links the hosted **Hugging Face Space**
  (`patolojiai/pathology-report-checker-skill`) and a one-click **Download
  `.skill`** button.

### Changed
- README installation rewritten — Method 1: `.skill` upload (no terminal);
  Method 2: clone & symlink; Method 3: Hugging Face demo.
- Fixed placeholder `yourusername` repository URLs → `sbalci`.

### Removed
- Stopped tracking the personal `*.code-workspace` IDE file (kept on disk,
  now gitignored).

### Why
Prepares the skill for a public release: a one-click uploadable artifact, a
browsable project site, and clear academic provenance for the ECDP2026 work.

> **Post-merge release steps** (after the repo is transferred to the **patolojiAI**
> org and made public):
> 1. `python3 .dev/scripts/build_skill.py`
> 2. `gh release create v1.2.0 dist/pathology-report-checker.skill --title "v1.2.0" --notes-file CHANGELOG.md`
> 3. Enable Pages: **Settings → Pages → Source: `/docs`**.
> 4. Add `docs/CNAME` containing `reportskill.patoloji.dev` for the custom domain (patoloji.dev is managed in Cloudflare).
> 5. Swap `sbalci` → `patolojiAI` in URLs (GitHub keeps redirects, so old links keep working).

---

## [1.1.0-rc] - 2026-05-26

### Changed
- **SKILL.md rewritten against Anthropic's official "Complete Guide to Building Skills for Claude"**:
  - Description sharpened to include WHAT, WHEN, and explicit trigger phrases (1001/1024 chars)
  - Added negative triggers ("Do NOT use for non-cancer pathology, cytology...") to prevent over-triggering
  - Added `license: MIT` and `metadata` block (author, version, guidelines) to YAML frontmatter
  - Moved CRITICAL performance notes to the top so they are not buried
  - Tightened workflows, severity table, and example outputs
  - Added explicit "When Not To Use" section
- **`.skillignore`** expanded to keep README, marketplace docs, dev planning files, `local_studies/`, and the `shared_scripts` symlink out of the packaged skill
- **`marketplace.json`**: corrected repository URL to `sbalci/pathology-report-checker-skill`, bumped version to 1.1.0, updated author

### Why
Prepares the skill for marketplace release. Aligns with Anthropic's published best practices for description writing, progressive disclosure, and packaging hygiene.

---

## [2.6] - 2024-12-29

### Added
- **Sample reports**: 10 synthetic test cases for all 4 tumor types
  - 5 complete/compliant reports (EN + TR)
  - 3 incomplete reports with missing elements
  - 2 reports with cross-validation errors
- **Expected outputs**: Sample QA results for validation
- `samples/README.md` with test categories and usage

### Changed
- Updated TODO.md: F3 (Case examples) marked complete

---

## [2.5] - 2024-12-29

### Added
- **Modular documentation**: Split SKILL.md into focused docs
  - `docs/QUICK_REFERENCE.md` - 1-page cheat sheet (140 lines)
  - `docs/WORKFLOW.md` - Detailed compliance workflow (342 lines)
  - `docs/FEATURES.md` - Feature documentation (365 lines)
  - `docs/USAGE.md` - CLI and script usage guide (252 lines)

### Changed
- **SKILL.md**: Reduced from 1,116 → 230 lines (80% reduction)
- Updated file structure in README.md

---

## [2.4] - 2024-12-29

### Added
- **Watch folder script** (`scripts/watch_folder.py`)
  - Continuous directory monitoring with watchdog
  - Multiple processing modes: compliance, synoptic, summary, autofill
  - Duplicate prevention via MD5 hash tracking
  - Resume capability after restart
  - Supports: txt, md, pdf, docx, jpg, png, tiff

### Changed
- Documentation now clearly distinguishes API key requirements
  - Claude CLI / Claude.ai: No API key needed
  - Python scripts: API key required

---

## [2.3] - 2024-12-29

### Added
- **Amendment generator** (`references/amendments/amendment_generator.md`)
  - Addendum, Correction, Amended Report templates
  - 8 template categories (staging, margins, nodes, biomarkers, etc.)
  - Bilingual support (EN + TR)
  - Clinical impact statements
  - Best practices and timing guidelines

---

## [2.2] - 2024-12-29

### Added
- **Auto-fill suggestions** (`references/autofill/autofill_suggestions.md`)
  - Size → pT category mapping (all 4 tumors)
  - Node count → pN category mapping
  - pTNM → Stage Group calculation
  - Grade interpretation
  - Margin status suggestions
  - Biomarker interpretation (HER2, MMR)
  - Confidence levels (High/Medium/Low)

---

## [2.1] - 2024-12-29

### Added
- **Free-text to synoptic converter** (`references/converters/freetext_to_synoptic.md`)
  - Pattern matching for tumor size, grade, margins, nodes, LVI, PNI
  - Bilingual extraction (EN + TR)
  - Automatic staging calculation
  - Handling for missing/conflicting data

---

## [2.0] - 2024-12-28

### Added
- **Tumor board summary generator** (`references/summaries/tumor_board_summary.md`)
  - Concise 3-5 line MDT format
  - Templates for all 4 tumor types
  - Bilingual output (EN + TR)

---

## [1.9] - 2024-12-28

### Added
- **AAPA macroscopy guidelines** merged into organ-specific files
  - Pre-analytic requirements (fixation times, cold ischemia)
  - Specimen-specific gross requirements
  - Gross vs microscopic correlation checks

---

## [1.8] - 2024-12-28

### Added
- **SNOMED CT / ICD-O-3 coding** (`references/coding/snomed_ct_codes.md`)
  - Morphology codes for all tumor types
  - Topography codes by anatomic site
  - Behavior and grade codes
  - Procedure codes

---

## [1.7] - 2024-12-28

### Added
- **Synoptic template generator** (`references/templates/`)
  - Blank CAP-style templates for all 4 tumor types
  - English version: `synoptic_templates.md`
  - Turkish version: `synoptic_templates_tr.md`
  - Field markers: Required (*), Conditional (+), Optional (°)

---

## [1.6] - 2024-12-28

### Added
- **TNM stage calculator** (`references/staging/tnm_stage_calculator.md`)
  - AJCC 8th edition staging tables
  - All 4 tumor types supported
  - Cross-validation with reported stage
  - ypTNM prefix handling for neoadjuvant cases

---

## [1.5] - 2024-12-28

### Added
- **Gastric carcinoma** support
  - CAP Stomach protocol
  - ICCR Gastric Carcinoma dataset
  - Lauren classification (intestinal/diffuse/mixed)
  - Borrmann gross classification
  - HER2 testing requirements
  - Minimum 16 lymph nodes

---

## [1.4] - 2024-12-28

### Added
- **Macroscopy checker** (`references/macroscopy/`)
  - AAPA-based gross description guidelines
  - Organ-specific requirements (breast, colorectal, pancreas, gastric)
  - Common elements (`MACROSCOPY_COMMON.md`)
  - Gross vs diagnosis cross-validation

---

## [1.3] - 2024-12-28

### Added
- **Batch processing script** (`scripts/batch_checker.py`)
  - Claude API integration
  - Folder and Excel/CSV input support
  - Summary statistics and CSV/Excel output

---

## [1.2] - 2024-12-28

### Added
- **CLI modes**: Folder of reports, Excel/CSV input
- **Quality metrics**: Completeness, Clarity, Consistency scores
- **Trend tracking**: Historical JSON data for department analytics

---

## [1.1] - 2024-12-28

### Added
- **Exocrine pancreas carcinoma** support
  - CAP Panc.Exo protocol
  - 6 margin protocol for Whipple specimens
  - R classification (R0/R1/R2)
- **Severity scoring**: Critical (-15), Major (-5), Minor (-2)
- **Cross-validation checks**: pT vs size, pN vs nodes, margin vs R
- **Field status detection**: Missing vs Empty fields

---

## [1.0] - 2024-12-27

### Added
- Initial release
- **Breast invasive carcinoma** support
  - CAP Breast.Invasive protocol
  - ICCR Invasive Carcinoma of the Breast dataset
  - ER/PR/HER2/Ki-67 biomarkers
- **Colorectal resection** support
  - CAP ColoRectal protocol
  - ICCR Colorectal Cancer dataset
  - MMR/MSI status
- Bilingual support (English + Turkish)
- Compliance scoring (0-100)
- QA report generation

---

## Legend

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features to be removed in future
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements
