# Usage Guide

Two usage modes with different authentication requirements.

---

## Quick Reference

| Method | API Key? | Best For |
|--------|----------|----------|
| Claude.ai / Claude App | ❌ No | Manual report checking |
| Claude CLI | ❌ No | One-time folder analysis |
| `batch_checker.py` | ✅ Yes | Automated batch processing |
| `watch_folder.py` | ✅ Yes | Continuous monitoring |

---

## Option 1: Claude CLI / Claude.ai (No API Key)

Uses your existing Claude authentication.

### Claude.ai / Claude App

Paste or upload a pathology report and use a trigger phrase:

```
Check this pathology report for CAP/ICCR compliance:

[paste report text or upload file]
```

### Claude CLI

```bash
# Single report - pipe or paste
claude "Check this breast pathology report for CAP compliance" < report.txt

# Folder of reports
claude "Analyze all pathology reports in /data/reports/ for compliance"

# Convert to synoptic format
claude "Convert this report to CAP synoptic format" < narrative_report.txt

# Generate tumor board summary
claude "Generate a tumor board summary from this report" < report.pdf

# Generate template
claude "Generate a breast synoptic template"

# Calculate staging
claude "What stage is pT2 N1a M0 breast cancer?"
```

### Supported File Formats

| Type | Extensions |
|------|------------|
| Text | `.txt`, `.md` |
| PDF | `.pdf` |
| Word | `.docx` |
| Images | `.jpg`, `.jpeg`, `.png`, `.tiff` |

### CLI Workflow

1. Claude reads skill reference files automatically
2. Detects tumor type from report content
3. Loads appropriate guidelines
4. Analyzes report
5. Generates output in conversation

---

## Option 2: Python Scripts (API Key Required)

Makes direct API calls. For automated/scheduled processing.

### Setup

```bash
# Install dependencies
pip install anthropic watchdog openpyxl pypdf python-docx

# Set API key (required!)
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Batch Processing Script

Process multiple reports at once.

```bash
# Basic usage
python scripts/batch_checker.py /input/folder /output/folder

# Specify tumor type
python scripts/batch_checker.py /input /output --tumor-type pancreas

# Limit number of reports
python scripts/batch_checker.py /input /output --limit 10

# Use different model
python scripts/batch_checker.py /input /output --model claude-sonnet-4-20250514
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `input_dir` | Folder containing reports |
| `output_dir` | Folder for results |
| `--tumor-type` | Specify type (breast, colorectal, pancreas, gastric) |
| `--limit` | Maximum reports to process |
| `--model` | Claude model to use |

**Output Files:**

```
output/
├── report1_qa.txt         # Individual QA reports
├── report2_qa.txt
├── summary_report.txt     # Overall statistics
├── compliance_data.csv    # Structured data
└── compliance_data.xlsx   # Excel workbook
```

### Watch Folder Script

Continuously monitor a folder for new reports.

```bash
# Watch folder for compliance checking (default)
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

**Arguments:**

| Argument | Description |
|----------|-------------|
| `watch_dir` | Folder to monitor |
| `--output` | Folder for results (default: watch_dir/results) |
| `--mode` | Processing mode (compliance, synoptic, summary, autofill) |
| `--interval` | Polling interval in seconds |
| `--process-existing` | Process files already in folder |
| `--no-watch` | One-time processing, don't watch |

**Processing Modes:**

| Mode | Output |
|------|--------|
| `compliance` | CAP/ICCR compliance QA report |
| `synoptic` | Structured synoptic format conversion |
| `summary` | 3-5 line tumor board summary |
| `autofill` | Suggested values for missing fields |

**Output Files:**

```
results/
├── report1_compliance_20241229_143052.txt
├── report2_synoptic_20241229_143215.txt
├── report3_summary_20241229_143422.txt
└── .processed_files.json   # Tracker (prevents reprocessing)
```

**Features:**

- **Automatic detection**: New files processed immediately
- **Duplicate prevention**: Tracks processed files by hash
- **Multiple formats**: Handles text, PDF, Word, images
- **Logging**: Activity logged with timestamps
- **Resume capability**: Picks up after restart

---

## Excel/CSV Input

Both CLI and scripts support Excel/CSV input:

**Claude CLI:**
```bash
claude "Check compliance for reports in /path/to/reports.xlsx"
```

**Expected Excel Format:**

| Column | Description |
|--------|-------------|
| `report_id` or `case_id` | Unique identifier |
| `report_text` or `diagnosis` | Full report text |
| `tumor_type` (optional) | breast, colorectal, pancreas, gastric |

---

## Language Support

All modes support both English and Turkish:

**English:**
```bash
claude "Check this report for CAP compliance"
```

**Turkish:**
```bash
claude "Bu raporu CAP uyumluluğu için kontrol et"
```

The skill automatically detects report language and responds accordingly.

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "API key not set" | `export ANTHROPIC_API_KEY="your-key"` |
| "Module not found" | `pip install anthropic watchdog openpyxl` |
| "Permission denied" | Check folder permissions |
| "Rate limited" | Reduce batch size or add delays |

### Script Logs

Watch folder logs activity to console:
```
2024-12-29 14:30:52 - INFO - Processing: report1.txt
2024-12-29 14:30:55 - INFO - Completed: report1.txt
2024-12-29 14:30:55 - INFO - Result saved: report1_compliance_20241229_143055.txt
```

### Testing

Test with a simple report:
```bash
echo "Left breast, lumpectomy: 2cm invasive ductal carcinoma, Grade 2" | \
  claude "Check this for CAP compliance"
```
