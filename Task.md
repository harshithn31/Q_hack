# 🗂️ TASK.md – Personalized Learning Marketplace (LangGraph + Pydantic AI)

**MVP Status: All core backend and frontend steps for the quiz-enabled learning flow are complete. The prototype supports PDF upload, chat, bundle recommendation, quiz generation, validation, XP/badges, and a modern UI.**

---

## 🎯 Primary Goal
Design a conversational GenAI platform that:
1. Analyzes resumes and user goals via agents.
2. Recommends personalized course bundles.
3. Auto-prices bundles based on user-defined budgets.
4. Offers interactive micro-assessments (quizzes) before advancing modules.
5. Uses Pydantic AI for agent modularity, LangGraph for orchestration.

---

## 🔁 Phase 1: Agent & Graph Bootstrapping

### 🤖 Agent Definitions (in `/llm_agents`)
- [x] `ResumeAgent`: Parse resume and extract structured skill profile.
- [x] `ConversationAgent`: Capture goals, roles, preferences, budget from user chat.
- [x] `CourseRetrievalAgent`: Match skill gaps with embedded courses.
- [x] `PricingAgent`: Adjust bundle price to fit user's budget constraints.
- [x] `QuizAgent`: Generate quizzes to test understanding per module before unlocking the next.

### 🧩 LangGraph DAG Setup
- [x] Define flow: ResumeAgent → ConversationAgent → CourseRetrievalAgent → PricingAgent → QuizAgent
- [x] Structure LangGraph DAG using typed Pydantic nodes.
- [x] Add LangGraph test traces for each transition.

---

## 📚 Phase 2: Embeddings & Course Base

### 📂 Embedding Pipeline
- [ ] Ingest 10–20 sample course descriptions.
- [ ] Embed courses using OpenAI's `text-embedding-ada-002`.
- [ ] Store vectors in FAISS DB (`embeddings/faiss_index/`).
- [ ] Implement `retriever.py` for reusable vector search abstraction.

---

## 💬 Phase 3: Chat + Resume Ingestion Flow

### 🧾 Resume Parsing
- [x] Upload resume (PDF or text).
- [x] Extract → chunk → embed.
- [x] Route into `ResumeAgent`; log structured skill profile output.

### 🧠 Chatflow UX
- [x] Build chat frontend to capture:
  - Career goal
  - Preferred tech domain (e.g., frontend, data)
  - Budget
- [x] Connect to `ConversationAgent` backend API.

---

## 🧠 Phase 4: Course Bundle & Pricing

### 🎯 Course Bundle Logic
- [x] Compare user resume skills with goal skills.
- [x] Retrieve best-fit courses from FAISS.
- [x] Output as bundle cards (title, skills, time, price).

### 💸 Dynamic Pricing Logic
- [x] Compute scaled pricing using:
  ```python
  scaled_price = (budget / total_base_price) * base_price
  ```
- [ ] Reflect bundle changes live in UI with budget slider.

---

## 🧪 Phase 5: Quiz Agent Integration

### ✍️ Quiz Generation Flow
- [x] Build `QuizAgent` (Pydantic AI)
  - Input: `module_title`, `target_skill`
  - Output: 3–5 MCQs as JSON
- [x] Use GPT-4 to generate questions OR load from static quiz pool (for mock).
- [x] Show quiz in frontend before enabling next module.

### 🔐 Quiz Evaluation
- [x] Simple answer validation logic.
- [x] Gate progression based on score (optional toggle for demo).

---

## 💻 Phase 6: Frontend UI

### 🖥️ Components
- [x] Resume upload + status indicator.
- [x] Chat-based assistant UI (collects resume/goals/budget).
- [x] Bundle preview: Course cards with skill tags + pricing.
- [x] Budget slider (UI fully implemented, live course swapping: [TODO])
- [x] Quiz interface: MCQ with feedback + score (unlock logic optional).
- [x] Responsive, mobile-first UI (all screens, all breakpoints)
- [x] Light/dark mode toggle in NavBar
- [x] Modern, custom color palette (theme-aware)
- [x] Gamified dashboard: XP, badges, quiz history, progress

---

## 🧪 Testing & Validation

### ✅ Core Testing
- [x] Unit tests for all Pydantic agents (including `QuizAgent`).
- [x] Validate LangGraph transitions (happy path + edge).
- [x] Simulated full flow: resume → goals → bundle → pricing → quiz.

---

## 🔜 Optional Extensions (Post-hackathon or stretch goals)
- [ ] Add support for persistent user accounts & profiles.
- [x] Add XP/progress badges for quiz completion.
- [ ] Gamified dashboard (track learning over time).