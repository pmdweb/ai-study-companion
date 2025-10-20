# Multi-Agent Setup - AI Study Companion

## Agent Roles & Responsibilities

### 🎨 Frontend Agent (`agent-frontend.md`)

**Focus**: Streamlit UI, user experience, visual feedback
**Tools**: GitHub Copilot, Cursor (UI-focused)
**Commands**: `streamlit run app.py`, UI testing

### 🧠 Backend Agent (`agent-backend.md`)

**Focus**: STAR evaluation, AI models, PDF processing
**Tools**: Claude, ChatGPT (AI/ML tasks)
**Commands**: Python scripts, model testing

### ⚙️ DevOps Agent (`agent-devops.md`)

**Focus**: Testing, deployment, performance optimization  
**Tools**: GitHub Actions, Docker, monitoring tools
**Commands**: `pytest`, `docker build`, deployment scripts

## How to Use Multiple Agents

### **Method 1: Sequential Workflow**

1. **DevOps Agent**: Set up environment and testing
2. **Backend Agent**: Implement STAR logic and AI integration
3. **Frontend Agent**: Build UI and connect to backend
4. **DevOps Agent**: Deploy and monitor

### **Method 2: Parallel Development**

- **Frontend Agent**: Works on `app.py` UI components
- **Backend Agent**: Develops `src/` modules simultaneously  
- **DevOps Agent**: Prepares infrastructure and testing

### **Method 3: Feature-Based**

Each agent takes complete ownership of specific features:

- **PDF Processing**: Backend Agent
- **STAR Evaluation**: Backend Agent  
- **User Interface**: Frontend Agent
- **Performance**: DevOps Agent

## Coordination Patterns

### **Handoff Protocol**

```markdown
@frontend-agent: UI ready for STAR integration
- Completed: File upload, question selection
- Next: Need score_star() function integration
- Interface: Expects dict with 'situation', 'task', 'action', 'result'
```

### **Shared Interfaces**

All agents must respect these contracts:

```python
# Backend provides this interface
score_star(text: str) -> dict  # STAR scores
rewrite_response(question: str, response: str) -> str  # Improved response

# Frontend consumes these interfaces  
display_star_scores(scores: dict)  # Visual feedback
export_session(data: dict)  # Save functionality
```

## Agent Assignment Examples

### **Task**: "Add audio recording feature"

- **Frontend Agent**: UI recording controls, audio upload
- **Backend Agent**: Audio-to-text processing integration
- **DevOps Agent**: Audio codec dependencies, storage optimization

### **Task**: "Improve STAR detection accuracy"  

- **Backend Agent**: Algorithm improvements, ML model tuning
- **DevOps Agent**: Performance testing, benchmarking
- **Frontend Agent**: Better feedback visualization

### **Task**: "Deploy to production"

- **DevOps Agent**: Infrastructure setup, CI/CD pipeline
- **Backend Agent**: Model optimization for production
- **Frontend Agent**: Production UI polish and error handling

## Tool Recommendations

| Agent | Primary Tool | Secondary Tool | Reason |
|-------|-------------|----------------|---------|
| Frontend | Cursor | GitHub Copilot | UI-focused, visual feedback |
| Backend | Claude | ChatGPT | Complex AI/ML reasoning |
| DevOps | GitHub Copilot | Terminal tools | Infrastructure automation |

---
*Choose agent roles based on task complexity and your team's expertise*
