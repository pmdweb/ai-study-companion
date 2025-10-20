# 🎯 AI Study Companion - Interview Mentor

An AI-powered interview mentor focused on **STAR methodology feedback**. Upload PDF questions, provide responses, and get structured feedback with AI-enhanced improvements.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **📊 STAR Evaluation**: Comprehensive scoring of Situation, Task, Action, Result components
- **🚀 AI Enhancement**: Automatically rewrite weak responses into professional STAR format
- **🤔 Follow-up Questions**: Generate realistic recruiter follow-up questions for practice
- **📄 Session Export**: Save complete interview sessions with original and enhanced responses
- **🔄 Score Comparison**: See improvement metrics before and after enhancement
- **🏠 Local-First**: No external API dependencies, runs completely offline

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-study-companion.git
cd ai-study-companion

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Run the application
streamlit run app.py
```

Open your browser to `http://localhost:8501`

## 🎯 How It Works

1. **Select Question**: Choose from sample interview questions (PDF upload coming soon)
2. **Enter Response**: Write your answer in the text area
3. **Get Evaluation**: Click "Evaluate Response" to see STAR methodology scores
4. **Generate Enhancement**: Click "Generate Improved Response" for AI-optimized version
5. **Compare & Learn**: Review score improvements and follow-up questions
6. **Export Session**: Save your complete interview practice session

## 🏗️ Architecture

### Tech Stack
- **UI**: Streamlit (single-page application)
- **NLP**: transformers + spaCy (sentence processing)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (local disk storage)
- **PDF Processing**: PyMuPDF (robust text extraction)
- **LLM**: Template-based with fallback to local models

### Project Structure
```
ai-study-companion/
├── app.py                 # Streamlit main UI
├── requirements.txt       # Python dependencies
├── .github/
│   ├── copilot-instructions.md    # Main AI agent instructions
│   ├── agent-frontend.md          # Frontend specialist instructions
│   ├── agent-backend.md           # Backend specialist instructions
│   ├── agent-devops.md            # DevOps specialist instructions
│   └── multi-agent-setup.md       # Multi-agent coordination guide
├── data/
│   ├── corpus/           # PDFs and indexed texts
│   └── chroma/           # Vector database (local storage)
└── src/
    ├── star_rubric.py    # STAR methodology evaluator & rewriter
    ├── ingest_pdf.py     # PDF text extraction & cleaning (planned)
    ├── embedder.py       # Sentence embeddings generation (planned)
    └── rag.py            # Question retrieval & ranking (planned)
```

## 🎯 STAR Methodology

The application evaluates responses using the STAR framework:

- **🎬 Situation**: Context (time, place, company, specific problem)
- **🎯 Task**: Clear objective/responsibility ("my goal was...")
- **⚡ Action**: Specific steps with action verbs (avoid generic descriptions)
- **🏆 Result**: Quantifiable impact (numbers, metrics, outcomes)

**Scoring**: Each component receives 0-2 points (max 8 total)

## 🔧 Development

### Multi-Agent Development
This project supports multi-agent development with specialized roles:

- **Frontend Agent**: UI/UX, Streamlit components
- **Backend Agent**: STAR evaluation, AI integration
- **DevOps Agent**: Testing, deployment, performance

See `.github/multi-agent-setup.md` for detailed coordination patterns.

### Running Tests
```bash
# Test STAR evaluation
python src/star_rubric.py

# Test specific functionality
python -c "from src.star_rubric import score_star; print(score_star('I fixed a bug'))"
```

### Development Commands
```bash
# PDF processing pipeline (when implemented)
python src/ingest_pdf.py path/to/questions.pdf
python src/embedder.py

# Start development server
streamlit run app.py --server.runOnSave true
```

## 📈 Roadmap

- [ ] **PDF Upload**: Direct PDF question bank upload and processing
- [ ] **Audio Recording**: Voice response recording and transcription
- [ ] **LLM Integration**: Local model integration (flan-t5-base, mistral-7b)
- [ ] **Industry Templates**: Specialized response templates by industry
- [ ] **Progress Tracking**: User progress analytics and improvement metrics
- [ ] **Mobile App**: React Native mobile application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
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