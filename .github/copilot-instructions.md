# AI Study Companion - Interview Mentor

## Project Purpose
STAR methodology interview feedback tool. Upload PDF → Select question → User responds → Get structured feedback + rewrite.

**Stack**: Streamlit UI + ChromaDB + sentence-transformers + local LLM (flan-t5-base/mistral-7b)

## Quick Start
```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt && python -m spacy download en_core_web_sm
streamlit run app.py
```

## Key Files & Patterns
- `app.py` - Single-page Streamlit UI (sidebar upload → main eval → export)
- `src/star_rubric.py` - STAR scorer returning `{'situation': {'score': 0-2, 'feedback': str}, ...}`
- `src/rewrite.py` - Response rewriter (90-second target, professional tone)
- `data/chroma/` - Local vector DB (no external deps)

## STAR Evaluation Rules
**Score 0-2 each**: Situation (context), Task (objective), Action (specific verbs), Result (metrics)
- Missing numbers in Result = automatic score reduction
- Template fallback if LLM unavailable
- Generate 3-5 recruiter follow-ups

## Critical Conventions
- `src/` modules use underscore_case
- ChromaDB on disk (local-first architecture) 
- all-MiniLM-L6-v2 for embeddings (lightweight)
- Professional international tone (no jargons)

## Development Commands
```bash
# PDF processing pipeline
python src/ingest_pdf.py path/to/questions.pdf  # Extract + normalize
python src/embedder.py                          # Generate embeddings

# Test STAR evaluation
python -c "from src.star_rubric import score_star; print(score_star('I fixed a bug'))"
```

## Common Tasks
**Add new STAR heuristic**: Edit `src/star_rubric.py` - check for action verbs, quantified results
**Improve rewriting**: Modify `src/rewrite.py` prompt template
**UI changes**: Single file `app.py` - sidebar(upload) → main(eval) → export
**Vector search**: ChromaDB queries in `src/rag.py` by category tags

## Quality Gates
✅ STAR scores identify missing elements correctly  
✅ Rewritten responses are 90s speaking time  
✅ Follow-up questions sound recruiter-realistic  
✅ Works offline (no API dependencies)

---
*This is interview prep focused on STAR methodology - not general study tool*