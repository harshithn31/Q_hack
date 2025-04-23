# Personalized Learning Marketplace (GenAI, Pydantic AI, LangGraph)

## Overview
A conversational GenAI platform that analyzes resumes and user goals, recommends personalized course bundles, and auto-prices them based on budget. Modular agents (Pydantic AI), orchestrated with LangGraph, power the backend. Frontend is React + Chakra UI.

---

## Features
- Resume parsing and skill extraction (GPT-4)
- Conversational goal and budget capture
- Skill gap analysis and course retrieval (FAISS, OpenAI embeddings)
- Dynamic, rule-based bundle pricing
- Modular, testable agents (Pydantic AI)
- Async LangGraph DAG orchestration
- FastAPI backend API
- React + Chakra UI frontend (scaffolded)

---

## Directory Structure
```
trendsetter/
  backend/
    api/
      routes.py
    llm_agents/
      resume_agent.py
      conversation_agent.py
      course_retrieval_agent.py
      pricing_agent.py
    graph/
      dag.py
    main.py
    requirements.txt
  frontend/
    components/
    pages/
    utils/
  PLANNING.md
  Task.md
  README.md
  .gitignore
```

---

## Setup & Usage

### Backend
1. `cd trendsetter/backend`
2. `pip install -r requirements.txt`
3. Add your OpenAI key to `.env`:  
   `OPENAI_API_KEY=sk-...`
4. `uvicorn main:app --reload`

### Frontend
1. `cd trendsetter/frontend`
2. `npm install`
3. `npm run dev`

---

## Backend Secrets Management (`.env`)
All backend secrets (such as API keys) must be provided via environment variables using a `.env` file in the `backend` directory. # Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
Never hardcode secrets in code.# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.


1. # Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
Setup:# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.

   - Copy `.env.example` to `.env` in the backend directory:
     ```sh
     cp backend/.env.example backend/.env
     ```
   - Fill in your actual OpenAI API key and any other required secrets.

2. # Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
Security:# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.

   - `.env` is already in `.gitignore` and must never be committed to version control.
   - # Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
Do not share your real API keys.# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.

   - If you rotate or update secrets, update your `.env` accordingly.

3. # Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
Required Variables:# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.

   - `OPENAI_API_KEY`: Your OpenAI API key for embeddings and quiz generation.

4. # Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
Usage:# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.
# Personalized Learning Marketplace Backend

## Overview
This backend powers a personalized learning platform that recommends modular learning bundles tailored to users' skill gaps and preferences. It leverages LLM agents (OpenAI GPT-4o), LangGraph orchestration, and FAISS for semantic search.

## Key Features
- **Resume Parsing Agent**: Extracts skills, summary, experience highlights, and learning preferences from free-text resumes.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat transcripts.
- **Course Retriever**: Uses embeddings and FAISS to retrieve the most relevant courses (with modules) for a user's skill gap.
- **Course Retrieval LLM Agent**: Selects and packages the most relevant modules and subtopics using GPT-4o, providing a rationale for each.
- **Pricing Agent**: Bundles modules/courses within a given budget.
- **Quiz Agent**: Generates quizzes for selected modules.
- **API**: `/recommend-bundle` endpoint returns a module-level personalized learning bundle.

## API Example
### `/recommend-bundle` (POST)
**Request:**
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
**Response:**
```json
{
  "summary": "...",
  "skills": ["..."],
  "target_role": "...",
  "goal_skills": ["..."],
  "skills_gap": ["..."],
  "recommended_modules": [
    {
      "course_title": "...",
      "module_title": "...",
      "module_description": "...",
      "selected_subtopics": ["..."],
      "why_selected": "..."
    }
  ],
  "final_bundle": [ ... ]
}
```

## Agents & Prompts
- **Resume Agent**: Extracts skills, summary, experience highlights, and learning preferences. Robust to noisy/unstructured input.
- **Conversation Agent**: Extracts target role, goal skills, budget, preferences, and context from chat. Handles informal, multi-turn dialogue.
- **Course Retrieval Agent**: Selects the most relevant modules/subtopics per skill gap, with rationale, maximizing diversity and relevance.

## Setup
1. `cp .env.example .env` and add your `OPENAI_API_KEY`.
2. `pip install -r requirements.txt` (Python 3.10+ recommended)
3. Run the backend: `uvicorn trendsetter.backend.api.main:app --reload`

## Security
- All secrets via `.env` (never hardcoded)
- All inputs validated with Pydantic
- Output sanitized and structured for frontend

## Testing
- Unit tests in `/tests/agents`, `/tests/langgraph`, `/tests/api`
- Run all tests: `pytest`

## Directory Structure
- `trendsetter/backend/llm_agents/` — All modular LLM agent logic
- `trendsetter/backend/embeddings/courses.json` — Course/module catalog
- `trendsetter/backend/graph/dag.py` — Orchestration pipeline
- `trendsetter/backend/api/routes.py` — API endpoints

## Contact & Contributions
Open an issue or PR for improvements, or reach out to the maintainers.

   - The backend loads secrets automatically using [python-dotenv](https://pypi.org/project/python-dotenv/).
   - If a required secret is missing, the backend will fail securely and log a clear error.

---

## API Example
POST `/recommend-bundle`
```json
{
  "resume_text": "...",
  "chat_transcript": "..."
}
```
Returns personalized bundle, pricing, and course recommendations.

---

## Testing
- Tests should be placed in `backend/tests/`
- Use `pytest` for backend tests

---

## Roadmap
- [x] Modular agent backend (Pydantic AI)
- [x] LangGraph DAG orchestration
- [x] FastAPI API
- [ ] Embedding pipeline & FAISS course retrieval
- [ ] Frontend UI polish
- [ ] Payment integration, persistent sessions

---

## Authors
- [Your Name]

## License
[MIT or your choice]
