# 🧠 PLANNING.md – Personalized Learning Marketplace (LangGraph + Pydantic AI)

## 🧭 Overview
Build an AI-powered assistant that:
- Parses resumes
- Chats with the user about goals and budget
- Suggests a course bundle tailored to the user’s skill gaps
- Prices the bundle according to budget constraints
- Adds micro-assessments (quizzes/tests) between modules to ensure understanding

Built using **Pydantic AI agents** and **LangGraph DAG orchestration**.

---

## 📐 Architecture

### 🔗 LangGraph DAG Flow:
```
Start ➜ ResumeAgent ➜ ConversationAgent ➜ CourseRetrievalAgent ➜ PricingAgent ➜ QuizAgent ➜ End
```

- **ResumeAgent** → Extract skills from parsed resume
- **ConversationAgent** → Capture goals and budget
- **CourseRetrievalAgent** → Find relevant courses from FAISS
- **PricingAgent** → Adjust bundle to fit budget
- **QuizAgent** → Generate or fetch tailored quizzes before allowing module progression

---

## 🔧 Core Modules

### 🧠 Pydantic AI Agents
Each agent lives in `/llm_agents/`:
- `ResumeAgent`
- `ConversationAgent`
- `CourseRetrievalAgent`
- `PricingAgent`
- `QuizAgent` (NEW)

### 🧩 Embedding Layer
- FAISS vector store
- Embedded items:
  - Course catalog (title + description)
  - Resume chunks (optional)
  - Quiz templates/questions (optional, mock for hackathon)

### 💬 Conversation Input
- UI + backend route to gather:
  - Resume
  - Role of interest
  - Budget
  - Preferred stack/domain (e.g., frontend, data, devops)

---

## 🧪 Quiz/Assessment Logic

### ✍️ QuizAgent Responsibilities
- Input: `current_skill: str`, `module_title: str`
- Output: `quiz: List[Dict]` – multiple choice questions + correct answers
- Sources:
  - GPT-4 generated questions via template (e.g., "Generate 3 MCQs to test understanding of X concept")
  - Optionally retrieved from pre-made quizzes stored in vector store
- Evaluation:
  - (Optional for hackathon) Accept mock answers, verify score, gate next module

---

## 🏗️ Stack & Tools

### Backend
- FastAPI
- LangGraph
- Pydantic AI
- FAISS
- OpenAI (GPT-4 for quiz generation + prompts)

### Frontend
- React
- Chakra UI / Tailwind CSS
- Axios

---

## 🧪 Testing Strategy

### Unit Tests
- Agent schema tests: QuizAgent input/output validation
- LangGraph: Add `QuizAgent` transitions in DAG test

### Integration Tests
- Resume → Skill → Goal → Bundle → Quiz
- Mock test score logic to show user "passed" to move forward

---

## 🗂️ Directory Structure

```
backend/
  ├── api/
  │   └── routes.py
  ├── llm_agents/
  │   ├── resume_agent.py
  │   ├── conversation_agent.py
  │   ├── course_retrieval_agent.py
  │   ├── pricing_agent.py
  │   └── quiz_agent.py         # <--- New!
  ├── graph/
  │   └── dag.py
  ├── embeddings/
  │   ├── loader.py
  │   └── quizzes.json          # (Optional for mock)
  └── tests/
      └── agents/
      └── graph/
      └── pricing/
      └── quiz/

frontend/
  ├── components/
  │   └── QuizView.jsx
  ├── pages/
  └── utils/
```

---

## 🧭 Future Extensions

- Add payment integration
- Persistent user sessions
- Pretrained classifier for course-level skill tags
- Gamify quiz success (XP, badges)
- Adaptive difficulty based on past quiz scores