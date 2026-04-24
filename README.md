# Learning Repository - Generative AI & Embeddings

A learning project exploring Google's Generative AI (Gemini) and sentence embeddings using modern AI libraries.

## Overview

This repository contains code for experimenting with:
- **Google Generative AI (Gemini 1.5 Flash)** - For text generation and AI tasks
- **Sentence Transformers** - For generating sentence embeddings

This is an educational project designed to demonstrate integration with state-of-the-art AI models.

## Project Structure

```
.
├── SetupGemini.py      # Gemini API setup and embedding model initialization
├── testme.py           # Basic test file with print statements
└── README.md           # This file
```

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Virtual environment (recommended)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/acsiri/Learning.git
   cd Learning
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install required dependencies:**
   ```bash
   pip install google-generativeai sentence-transformers
   ```

## Configuration

### Gemini API Setup

Before running the code, you need to configure your Gemini API key in `SetupGemini.py`:

```python
genai.configure(api_key="YOUR_GEMINI_API_KEY")
```

Replace `"YOUR_GEMINI_API_KEY"` with your actual API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Usage

### SetupGemini.py

Initializes the Gemini model and embedding model:

```python
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

# Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
```

Run the setup:
```bash
python SetupGemini.py
```

### testme.py

A simple test script:

```bash
python testme.py
```

Output:
```
hello world
ima done
this is the third story
testing the commits
```

## Models Used

### Gemini 1.5 Flash
- **Purpose:** Fast, efficient text generation
- **Use Cases:** Quick responses, creative content, Q&A
- **Documentation:** [Google Generative AI](https://ai.google.dev/)

### SentenceTransformer (all-MiniLM-L6-v2)
- **Purpose:** Generate sentence embeddings for semantic search
- **Model Size:** Lightweight and fast
- **Applications:** Text similarity, semantic search, clustering
- **Documentation:** [Sentence Transformers](https://www.sbert.net/)

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `google-generativeai` | Latest | Google Gemini API integration |
| `sentence-transformers` | Latest | Sentence embedding generation |

## Next Steps

- Expand `SetupGemini.py` with actual AI queries and embeddings
- Create a proper application structure with separate modules
- Add error handling and logging
- Implement semantic search functionality
- Add unit tests

## Getting Help

- **Gemini API Documentation:** https://ai.google.dev/
- **Sentence Transformers Guide:** https://www.sbert.net/
- **Google Generative AI Python Client:** https://github.com/google/generative-ai-python

## License

This repository is for educational purposes.

## Author

**Repository Owner:** acsiri

---

**Last Updated:** April 2026
