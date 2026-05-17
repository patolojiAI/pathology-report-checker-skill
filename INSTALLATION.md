# Installation Guide

## Prerequisites

- Claude Code CLI, Claude.ai, or Claude Desktop App
- No API key required for basic usage
- Optional: Python 3.8+ for batch processing scripts

## Installation Methods

### Method 1: Manual Installation (Recommended)

1. **Download the skill**
   ```bash
   git clone https://github.com/yourusername/pathology-report-checker-skill.git
   ```

2. **Copy to Claude skills directory**
   ```bash
   cp -r pathology-report-checker-skill ~/.claude/skills/
   ```

3. **Restart Claude Code** or reload skills
   ```bash
   # If using Claude Code CLI
   claude --reload-skills
   ```

### Method 2: Symlink Installation (for Development)

Create a symlink instead of copying for easier updates:

```bash
ln -s /path/to/pathology-report-checker-skill ~/.claude/skills/pathology-report-checker
```

### Method 3: Direct Download

1. Download the ZIP from GitHub
2. Extract to `~/.claude/skills/pathology-report-checker-skill/`
3. Restart Claude Code

## Verification

Test the installation:

```bash
# In Claude Code CLI
claude "List available skills"

# Or test directly
claude "Check this breast report for CAP compliance" < examples/breast_complete_en.txt
```

## Troubleshooting

### Skill Not Detected

- Ensure the folder is in `~/.claude/skills/`
- Verify SKILL.md exists in the root of the skill folder
- Check YAML frontmatter is properly formatted
- Restart Claude Code

### Permission Issues

```bash
chmod -R 755 ~/.claude/skills/pathology-report-checker-skill
```

### Path Issues on Windows

Windows users should use:
```
%USERPROFILE%\.claude\skills\
```

## Advanced Setup (Optional)

### Batch Processing Scripts

If you want to use the Python batch processing scripts:

1. **Install dependencies**
   ```bash
   cd ~/.claude/skills/pathology-report-checker-skill/.dev
   pip install anthropic watchdog openpyxl pypdf python-docx
   ```

2. **Set API key**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

3. **Run batch processor**
   ```bash
   python scripts/batch_checker.py /input/folder /output/folder
   ```

See `.dev/docs/USAGE.md` for detailed script documentation.

## Updating

### Git Installation

```bash
cd ~/.claude/skills/pathology-report-checker-skill
git pull origin main
```

### Manual Installation

1. Download the latest version
2. Replace the existing folder
3. Restart Claude Code

## Uninstallation

```bash
rm -rf ~/.claude/skills/pathology-report-checker-skill
```

## Next Steps

- See [README.md](README.md) for usage examples
- Try the example reports in `examples/`
- Read [MARKETPLACE.md](MARKETPLACE.md) for feature overview
- Check [.dev/docs/QUICK_REFERENCE.md](.dev/docs/QUICK_REFERENCE.md) for trigger phrases
