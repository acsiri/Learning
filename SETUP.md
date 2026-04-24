# Environment Setup Guide

## Quick Start

### 1. Python Environment Setup

**Windows:**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

Then update `SetupGemini.py` to read from environment:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
```

### 4. Verify Installation

```bash
python testme.py
```

## Troubleshooting

### ModuleNotFoundError

**Solution:** Ensure virtual environment is activated:
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### API Key Issues

- Verify API key is correct in Google AI Studio
- Check that API has been enabled in your Google Cloud project
- Ensure key is not expired or revoked

### Embedding Model Download

The first run will download the embedding model (~90MB). This requires internet connection.

## Updating Dependencies

```bash
pip install --upgrade google-generativeai sentence-transformers
```

## Deactivating Environment

```bash
deactivate
```

---

For more help, see the main [README.md](README.md)
