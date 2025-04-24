# 🌟 Gen Wagon - Personalized Learning Marketplace

**Gen Wagon** is a modern GenAI-powered learning platform that delivers personalized, modular course bundles based on users’ skills, goals, and preferences. It analyzes resumes and chats, retrieves targeted content via embeddings and FAISS, and orchestrates intelligent agents using LangGraph.

Built with:
- 🔧 **FastAPI + Pydantic AI** for structured backend logic  
- 🧠 **LangGraph + GPT-4o** for LLM-powered decision making  
- 🔍 **FAISS** for fast semantic course matching  
- ⚛️ **React + Chakra UI** for a seamless frontend experience  

---

## 🚀 Quickstart (Local Development)

### 🧰 Prerequisites
- Python ≥ 3.10
- Node.js ≥ 18
- npm ≥ 9

---

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv/Scripts/activate on Windows
pip install -r requirements.txt
cp .env.example .env
```

> ✏️ Edit `.env` and set your API keys:
```
OPENAI_API_KEY=sk-...
```

Start the server:
```bash
uvicorn main:app --reload
```

📚 API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)  
📡 Default Port: `8000`

---

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

🎨 Dev Server: [http://localhost:5173](http://localhost:5173)

---

## 🧠 Key Features

- **Resume Agent**: Extracts skills, experience, preferences from free-text resumes  
- **Conversation Agent**: Understands user goals, budget, preferences from chat  
- **Course Retriever**: Embedding + FAISS-powered semantic search  
- **Module Selector Agent**: Picks relevant subtopics using GPT-4o with rationale  
- **Pricing Agent**: Optimizes bundles within budget  
- **Quiz Agent**: Generates assessments from selected modules  
- **API**: `/recommend-bundle` — Returns a complete personalized learning plan

---

## 📦 API Reference

### `POST /recommend-bundle`

**Request:**
```json
{
  "resume_text": "Experienced data scientist with Python and SQL...",
  "chat_transcript": "I want to transition into ML engineering on a budget of €500..."
}
```

**Response:**
```json
{
  "summary": "...",
  "skills": ["Python", "SQL"],
  "target_role": "ML Engineer",
  "goal_skills": ["MLOps", "Deep Learning"],
  "skills_gap": ["MLOps", "Model Deployment"],
  "recommended_modules": [
    {
      "course_title": "Advanced ML Engineering",
      "module_title": "MLOps Fundamentals",
      "selected_subtopics": ["CI/CD", "Model Monitoring"],
      "why_selected": "Covers core deployment strategies for ML workflows."
    }
  ],
  "final_bundle": [...]
}
```

---

## 🧩 Project Structure

```
│
├── backend/
│   ├── api/              # FastAPI routes
│   ├── llm_agents/       # Modular LLM agents
│   ├── embeddings/       # Course catalog + FAISS logic
│   ├── graph/            # LangGraph DAG orchestration
│   ├── main.py           # Entry point
│   └── .env              # Your secrets (not committed)
│
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable UI elements
│   │   ├── pages/        # React pages
│   │   └── theme.js      # Chakra UI customization
└──   └── package.json
```

---

## 🔒 Security Best Practices

- ✅ Secrets managed via `.env` (auto-loaded with `python-dotenv`)
- ✅ Inputs validated with **Pydantic**
- ✅ No hardcoded credentials
- ✅ Responses are sanitized & structured

---

## 🛠 Troubleshooting

| Issue                  | Fix                                                                 |
|------------------------|----------------------------------------------------------------------|
| Backend not starting   | Check Python version, `.env` file, and `pip install -r requirements.txt` |
| Frontend error         | Run `npm install` after deleting `node_modules`                     |
| CORS issues            | Ensure both frontend and backend are running on correct ports       |

---

## 📍 Roadmap

- [x] Modular agent design (Pydantic AI)
- [x] LangGraph DAG orchestration
- [x] Resume & Chat understanding
- [x] FAISS + Embeddings
- [ ] Frontend polish & dashboard UX
- [ ] Session persistence
- [ ] Payment integration (Stripe, PayPal)

---

## 👨‍💻 Contributing

We welcome pull requests and ideas!

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Submit a PR with context
4. Tag us if it's urgent ✉️

---

## ✨ Authors & Maintainers

- **Harshith Naganna, Revan Kumar Dhanasekaran, Paul Gaikwad, Philipp Peter, Edilbert Christhuraj** — Lead Developer  
- **Community Contributors** — You!

---

## 📜 License

[MIT License](LICENSE)

> © 2025 Gen Wagon. All rights reserved.
