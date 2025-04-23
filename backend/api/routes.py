"""
FastAPI routes for Personalized Learning Marketplace backend.
Exposes pipeline as an async API endpoint.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from graph.dag import run_full_pipeline
from llm_agents.quiz_agent import get_quiz, validate_quiz_answers, QuizQuestion
from embeddings.utils import extract_resume_text
from typing import List, Dict

router = APIRouter()

# Simple in-memory XP/badge store for demo (keyed by user_id)
USER_XP = {}
USER_BADGES = {}

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """
    Accepts a PDF or TXT resume, extracts text securely, and returns it.
    """
    try:
        text = extract_resume_text(await file.read(), file.filename)
        if not text.strip():
            raise HTTPException(status_code=400, detail="No extractable text found in resume.")
        return {"text": text}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Resume extraction failed due to a server error.")

class PipelineRequest(BaseModel):
    resume_text: str
    chat_transcript: str

class QuizRequest(BaseModel):
    user_id: str
    current_skill: str
    module_title: str

class QuizSubmitRequest(BaseModel):
    user_id: str
    quiz: List[Dict]
    answers: List[str]

@router.post("/recommend-bundle")
async def recommend_bundle(request: PipelineRequest):
    """
    Runs the full pipeline and returns a module-level personalized learning bundle.
    Response includes summary, skills, skill gap, and recommended_modules (with course/module/subtopics/rationale).
    """
    state = await run_full_pipeline(request.resume_text, request.chat_transcript)
    return {
        "summary": state.summary,
        "skills": state.skills,
        "target_role": state.target_role,
        "goal_skills": state.goal_skills,
        "skills_gap": state.skills_gap,
        "recommended_modules": state.recommended_modules or [],
        "final_bundle": state.final_bundle or [],
    }

@router.post("/quiz")
async def get_quiz_endpoint(request: QuizRequest):
    quiz_output = await get_quiz(request.current_skill, request.module_title)
    return {"quiz": [q.dict() for q in quiz_output.quiz]}

@router.post("/quiz/submit")
async def submit_quiz(request: QuizSubmitRequest):
    # Validate answers
    quiz_objs = [QuizQuestion(**q) for q in request.quiz]
    result = validate_quiz_answers(quiz_objs, request.answers)
    # XP/badge logic (simple): +10 XP per correct, badge if perfect
    user_id = request.user_id
    USER_XP[user_id] = USER_XP.get(user_id, 0) + int(result["correct"]) * 10
    if result["score"] == 1.0:
        USER_BADGES.setdefault(user_id, set()).add("Quiz Master")
    return {"score": result["score"], "correct": result["correct"], "total": result["total"], "xp": USER_XP[user_id], "badges": list(USER_BADGES.get(user_id, []))}

@router.get("/xp/{user_id}")
async def get_xp(user_id: str):
    return {"xp": USER_XP.get(user_id, 0), "badges": list(USER_BADGES.get(user_id, []))}
