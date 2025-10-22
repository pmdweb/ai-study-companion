# 🎯 AI Study Companion - Interview Mentor

> Transform weak interview responses into compelling STAR-format answers with AI-powered feedback.
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/framework-Streamlit-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
## ✨ Features

- **📊 STAR Evaluation**: Comprehensive scoring of Situation, Task, Action, Result components
- **🚀 AI Enhancement**: Automatically rewrite weak responses into professional STAR format
- **🤔 Follow-up Questions**: Generate realistic recruiter follow-up questions for practice
- **📄 Session Export**: Save complete interview sessions with original and enhanced responses
- **🔄 Score Comparison**: See improvement metrics before and after enhancement
- **🏠 Local-First**: No external API dependencies, runs completely offline

## 🚀 Quick Start
### Prerequisites
Open your browser to `http://localhost:8501`.
# 🎯 AI Study Companion - Interview Mentor

> Transform interview responses into polished STAR-format answers with actionable AI feedback.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/framework-Streamlit-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- **📊 STAR Evaluation**: Scores Situation, Task, Action, Result components (0-2 each).
- **🚀 AI Enhancement**: Rewrites answers into concise, professional STAR responses.
- **🤔 Follow-up Questions**: Generates realistic recruiter follow-ups for practice.
- **📄 Session Export**: Save interview sessions (original + enhanced answers).
- **🔄 Score Comparison**: See before/after improvement metrics.
- **🏠 Local-First**: Runs offline with local models and no external API keys.

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Git

### Installation (Windows PowerShell)

```powershell
# Clone the repository
- Git

# Create and activate a virtual environment
python -m venv .venv; .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run the app
streamlit run app.py
```

Open your browser to http://localhost:8501

## 🎯 How It Works

1. Select a sample question or add your own.
2. Write your response in the text area.
3. Click "Evaluate Response" to receive STAR scores and targeted feedback.
4. Click "Generate Improved Response" to get a polished STAR answer.
5. Export the session for review.

## 🏗️ Architecture

### Tech Stack

- UI: Streamlit
- NLP: spaCy + sentence-transformers
- Embeddings: all-MiniLM-L6-v2
- Vector DB: ChromaDB (local)
- PDF Processing: PyMuPDF (planned)
- LLMs: Template-based prompts with optional local models

### Project Structure

```text
ai-study-companion/
├── app.py                 # Streamlit UI
├── requirements.txt       # Python deps
├── .github/               # Agent instructions & CI
├── data/                  # PDFs and vector DB
└── src/                   # Core modules (star_rubric, rag, embedder)
```

## 🎯 STAR Methodology

The evaluator checks:

- Situation: context and setup
- Task: objective and responsibility
- Action: concrete steps and verbs
- Result: quantifiable outcomes or impact

Each item scores 0-2 (max 8). Missing metrics in Result reduce the score.

## 🔧 Development

### Multi-Agent Development

The repo includes guidance for multiple specialized agents (frontend, backend, docs, presentation). See `.github/` for instructions.

### Running Tests

```bash
# Quick smoke tests
python -c "from src.star_rubric import score_star; print(score_star('I fixed a bug by improving logging'))"
```

### Dev Commands

```bash
# PDF ingest (planned)
python src/ingest_pdf.py path/to/questions.pdf
python src/embedder.py

# Start dev server
streamlit run app.py --server.runOnSave true
```

## 📈 Roadmap

- PDF question bank upload & indexing
- Audio recording & transcription
- Local LLM integrations (flan-t5, mistral)
- Industry-specific templates
- Progress tracking dashboard

## 🤝 Contributing

1. Fork the repo
2. Create a branch: git checkout -b feature/x
3. Commit & push
4. Open a PR

Code style: follow PEP 8 and add docstrings to core modules.

## 📝 License

MIT. See LICENSE file.
# Run the application
# 🎯 AI Study Companion - Interview Mentor

> Transform interview responses into polished STAR-format answers with actionable AI feedback.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/framework-Streamlit-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- **📊 STAR Evaluation** — Scores Situation, Task, Action, Result components (0-2 each).
- **🚀 AI Enhancement** — Rewrites answers into concise, professional STAR responses.
- **🤔 Follow-up Questions** — Generates realistic recruiter follow-ups for practice.
- **📄 Session Export** — Save interview sessions (original + enhanced answers).
- **🔄 Score Comparison** — See before/after improvement metrics.
- **🏠 Local-First** — Runs offline with local models and no external API keys.

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Git

### Installation (Windows PowerShell)

```powershell
# Clone the repository
git clone https://github.com/yourusername/ai-study-companion.git; cd ai-study-companion

# Create and activate a virtual environment
python -m venv .venv; .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run the app
streamlit run app.py
```

Open your browser to [http://localhost:8501](http://localhost:8501).

## 🎯 How It Works

1. Select a sample question or add your own.
2. Write your response in the text area.
3. Click "Evaluate Response" to receive STAR scores and targeted feedback.
4. Click "Generate Improved Response" to get a polished STAR answer.
5. Export the session for review.

## 🏗️ Architecture

### Tech Stack

- UI: Streamlit
- NLP: spaCy + sentence-transformers
- Embeddings: all-MiniLM-L6-v2
- Vector DB: ChromaDB (local)
- PDF Processing: PyMuPDF (planned)
- LLMs: Template-based prompts with optional local models

### Project Structure

```text
ai-study-companion/
├── app.py                 # Streamlit UI
├── requirements.txt       # Python deps
├── .github/               # Agent instructions & CI
├── data/                  # PDFs and vector DB
└── src/                   # Core modules (star_rubric, rag, embedder)
```

## 🎯 STAR Methodology

The evaluator checks:

- Situation: context and setup
- Task: objective and responsibility
- Action: concrete steps and verbs
- Result: quantifiable outcomes or impact

Each item scores 0-2 (max 8). Missing metrics in Result reduce the score.

## 🔧 Development

### Multi-Agent Development

The repo includes guidance for multiple specialized agents (frontend, backend, docs, presentation). See `.github/` for instructions.

### Running Tests

```bash
# Quick smoke tests
python -c "from src.star_rubric import score_star; print(score_star('I fixed a bug by improving logging'))"
```

### Dev Commands

```bash
# PDF ingest (planned)
python src/ingest_pdf.py path/to/questions.pdf
python src/embedder.py

# Start dev server
streamlit run app.py --server.runOnSave true
```

## 📈 Roadmap

- PDF question bank upload & indexing
- Audio recording & transcription
- Local LLM integrations (flan-t5, mistral)
- Industry-specific templates
- Progress tracking dashboard

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/x`
3. Commit & push
4. Open a PR

Code style: follow PEP 8 and add docstrings to core modules.

## 📝 License

MIT. See LICENSE file.

---

Focus: STAR methodology accuracy and realistic recruiter-style feedback. This tool is for interview preparation, not general study use.

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Test STAR evaluation accuracy

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for rapid prototyping
- Uses [sentence-transformers](https://www.sbert.net/) for semantic search
- Inspired by the STAR methodology for behavioral interviews
- Multi-agent development pattern for efficient collaboration

## 📞 Support

If you have questions or need help:

1. Check the [Issues](https://github.com/yourusername/ai-study-companion/issues) page
2. Review the `.github/` directory for agent-specific guidance
3. Open a new issue with detailed information

---

**Focus on STAR methodology accuracy and interview realism. This is interview preparation, not a general study tool.** 🎯