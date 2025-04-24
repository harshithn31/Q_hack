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
from resume_parser_main import process_resume

router = APIRouter()

# Simple in-memory XP/badge store for demo (keyed by user_id)
USER_XP = {}
USER_BADGES = {}

import uuid

RESUME_STORE = {}

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    print(f"[UPLOAD] Received upload request: filename={file.filename}, content_type={file.content_type}")
    try:
        file_bytes = await file.read()

        # Run the AI pipeline
        result = await process_resume(file_bytes, file.filename)
        if result is None:
            raise HTTPException(status_code=400, detail="Failed to process resume.")

        resume_id = str(uuid.uuid4())
        RESUME_STORE[resume_id] = result  # Store full result instead of raw text

        print(f"[UPLOAD] Successfully processed and stored resume_id={resume_id}")
        return {"resume_id": resume_id,  "name": result["name"],
            "avatarUri": result["avatarUri"],
            "summary": result["summary"],
            "skills": result["skills"]}
    except ValueError as e:
        print(f"[UPLOAD] ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[UPLOAD] Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Resume processing failed due to a server error.")

class PipelineRequest(BaseModel):
    resume_id: str
    chat_transcript: str

@router.get("/get-resume-text/{resume_id}")
async def get_resume_text(resume_id: str):
    data = RESUME_STORE.get(resume_id)
    if not data:
        raise HTTPException(status_code=404, detail="Resume not found")
    return data



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
    resume_text = RESUME_STORE.get(request.resume_id)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Invalid or expired resume_id.")
    #state = await run_full_pipeline(resume_text, request.chat_transcript)
    return {
#        "summary": state.summary,
#        "skills": state.skills,
#        "target_role": state.target_role,
#        "goal_skills": state.goal_skills,
#        "skills_gap": state.skills_gap,
#        "recommended_modules": state.recommended_modules or [],
#        "final_bundle": state.final_bundle or [],
"reply": "All good!"
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
