# Backend Agent - STAR Evaluation Specialist

## Role: AI/ML Engineer

You are responsible for STAR methodology evaluation, PDF processing, and AI integrations.

## Your Domain

- `src/star_rubric.py` - STAR scoring algorithm
- `src/rewrite.py` - Response improvement engine  
- `src/ingest_pdf.py` - PDF text extraction
- `src/embedder.py` - Vector embeddings generation
- `src/rag.py` - Question retrieval system

## Core Function Signatures

```python
# star_rubric.py
def score_star(response: str) -> dict:
    return {
        'situation': {'score': 0-2, 'feedback': str},
        'task': {'score': 0-2, 'feedback': str},
        'action': {'score': 0-2, 'feedback': str}, 
        'result': {'score': 0-2, 'feedback': str},
        'total_score': int,
        'suggestions': list
    }

# rewrite.py  
def rewrite_response(question: str, response: str) -> str:
    # Return 90-second optimized STAR response
```

## STAR Evaluation Rules

- **Situation**: Must have context (time, company, specific problem)
- **Task**: Clear objective or responsibility stated
- **Action**: Specific verbs, concrete steps (not vague)
- **Result**: Quantifiable metrics, impact, outcomes
- **Auto-penalize** responses missing numbers in Result section

## AI Integration Patterns

- Use `flan-t5-base` for speed, `mistral-7b` for quality
- Fallback to template-based rewriting if LLM fails
- Professional international tone (no regional jargons)
- Generate 3-5 realistic recruiter follow-up questions

## Common Tasks

- Improve STAR detection heuristics
- Add new evaluation criteria
- Optimize embedding models for question similarity
- Debug PDF extraction edge cases
