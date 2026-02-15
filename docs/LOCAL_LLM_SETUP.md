# Using check_report.py with Local LLM

Run pathology report compliance checks locally without sending data to the cloud.

## Prerequisites

- Python 3.8+
- `openai` package: `pip install openai`
- One of: **Ollama** or **LM Studio**

## Option A: Ollama Setup

### 1. Install Ollama

Download from https://ollama.com/download

### 2. Download a Model

```bash
ollama pull qwen2.5:3b          # Small (~2GB)
ollama pull llama3.1:8b         # Medium (~5GB)
ollama pull qwen2.5:14b         # Large (~9GB)
```

### 3. Run

```bash
python scripts/check_report.py -p ollama -m qwen2.5:3b "Check compliance" < report.txt
```

## Option B: LM Studio Setup

### 1. Install LM Studio

Download from https://lmstudio.ai

### 2. Download a Model

- Open LM Studio
- Search for `Qwen2.5-3B-Instruct-GGUF` or similar
- Download a `Q4_K_M` or `Q5_K_M` quantization

### 3. Configure Context Length

**Important:** The skill requires ~17,000 tokens context.

1. Go to **Local Server** tab
2. Set **Context Length** to `32768`
3. Load the model
4. Click **Start Server**

### 4. Run

```bash
python scripts/check_report.py -p lmstudio "Check compliance" < report.txt
```

## Usage Examples

```bash
# Basic compliance check
python scripts/check_report.py -p lmstudio "Check compliance" < report.txt

# Specify tumor type
python scripts/check_report.py -p ollama -m qwen2.5:3b -t breast "Check compliance" < report.txt

# Output to file
python scripts/check_report.py -p lmstudio "Check compliance" < report.txt > result.txt

# Quiet mode (no progress messages)
python scripts/check_report.py -p lmstudio -q "Check compliance" < report.txt

# Use file argument instead of stdin
python scripts/check_report.py -p lmstudio --file report.txt "Check compliance"
```

## Environment Variables

Set defaults to avoid typing flags:

```bash
# Windows
set LLM_PROVIDER=lmstudio
set OLLAMA_MODEL=qwen2.5:3b

# Linux/Mac
export LLM_PROVIDER=lmstudio
export OLLAMA_MODEL=qwen2.5:3b

# Then just run:
python scripts/check_report.py "Check compliance" < report.txt
```

## Recommended Models

| Model | Size | RAM Needed | Quality |
|-------|------|------------|---------|
| Qwen2.5-3B-Instruct | ~2GB | 8GB | Acceptable |
| Llama-3.1-8B-Instruct | ~5GB | 12GB | Good |
| Qwen2.5-14B-Instruct | ~9GB | 20GB | Very Good |
| Qwen2.5-32B-Instruct | ~20GB | 40GB | Excellent |

## Troubleshooting

### "Model not found"

```
Error: model 'llama3.1:70b' not found
```

**Fix:** Download the model first or specify the correct model name:
```bash
ollama list                    # See available models
ollama pull qwen2.5:3b         # Download model
```

### "Context length too small"

```
Error: context length of only 4096 tokens
```

**Fix:** Increase context length to 32768 in LM Studio settings, then reload the model.

### "openai package not installed"

```
Error: openai package not installed
```

**Fix:** Install the package:
```bash
pip install openai
```

### "Connection refused"

```
Error: Connection refused
```

**Fix:**
- Ollama: Ensure Ollama is running (`ollama serve`)
- LM Studio: Start the Local Server

## Privacy Note

With Ollama or LM Studio:
- All processing happens on your machine
- No data is sent to external servers
- Models are downloaded once, then work offline
- Your pathology reports remain completely private
