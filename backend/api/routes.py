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
from llm_agents.module_description_agent import get_module_description
from llm_agents.update_module_description_agent import get_updated_module_description
from llm_agents.suggestion_agent import get_suggestion_agent_response

from backend.llm_agents.explanation_agent import get_explanation, ExplanationOutput, ExplanationRequest

router = APIRouter()

# Simple in-memory XP/badge store for demo (keyed by user_id)
USER_XP = {}
USER_BADGES = {}

import uuid

RESUME_STORE = {}

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    print(f"[UPLOAD] Received upload request: filename={file.filename}, content_type={file.content_type}")
    """
    Accepts a PDF or TXT resume, extracts text securely, and returns a resume_id for later use.
    """
    try:
        text = extract_resume_text(await file.read(), file.filename)
        if not text.strip():
            print(f"[UPLOAD] Extraction failed: No extractable text found in {file.filename}")
            raise HTTPException(status_code=400, detail="No extractable text found in resume.")
        resume_id = str(uuid.uuid4())
        RESUME_STORE[resume_id] = text
        print(f"[UPLOAD] Successfully stored resume_id={resume_id} for {file.filename}")
        return {"resume_id": resume_id}
    except ValueError as e:
        print(f"[UPLOAD] ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[UPLOAD] Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Resume extraction failed due to a server error.")

class PipelineRequest(BaseModel):
    resume_id: str
    chat_transcript: str

@router.get("/get-resume-text/{resume_id}")
async def get_resume_text(resume_id: str):
    text = RESUME_STORE.get(resume_id)
    if not text:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"text": text}



class QuizRequest(BaseModel):
    user_id: str
    course_title: str
    module_title: str
    module_topics: List[str] = []  # Optional list of topics to guide quiz generation

class QuizSubmitRequest(BaseModel):
    user_id: str
    quiz: List[Dict]
    answers: List[str]
    
class ContentRequest(BaseModel):
    course_title: str
    module_title: str
    module_topics: List[str] = []

class ContentRequestUpdate(BaseModel):
    course_title: str
    module_title: str
    module_topics: List[str] = []
    wrong_questions: List[str] = []  # Optional list of wrong questions to guide content update

class ContentSuggestion(BaseModel):
    course_title: str
    module_title: str
    module_topics: List[str] = []
    wrong_questions: List[str] = []  # Optional list of wrong questions to guide content suggestion
    



@router.post("/recommend-bundle")
async def recommend_bundle(request: PipelineRequest):
    """
    Runs the full pipeline and returns a module-level personalized learning bundle.
    Response includes summary, skills, skill gap, and recommended_modules (with course/module/subtopics/rationale).
    """
    resume_text = RESUME_STORE.get(request.resume_id)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Invalid or expired resume_id.")
    state = await run_full_pipeline(resume_text, request.chat_transcript)
    return {
        "summary": state.summary,
        "skills": state.skills,
        "target_role": state.target_role,
        "goal_skills": state.goal_skills,
        "skills_gap": state.skills_gap,
        "recommended_modules": state.recommended_modules or [],
        "final_bundle": state.final_bundle or [],
    }


@router.post("/content_generator")
async def content_generator(request: ContentRequest):
    """
    Generates a module description based on course title, module title, and optional topics.
    Returns a concise and engaging summary of the module's key concepts.
    """
    module_description = await get_module_description(request.course_title, request.module_title, request.module_topics)
    return {"description": module_description.description}

@router.post("/content_updater")
async def content_updater(request: ContentRequestUpdate):
    """
    Updates the module description based on course title, module title, and optional topics.
    Returns a concise and engaging summary of the module's key concepts.
    """
    # Placeholder for content update logic (e.g., updating a database)
    # In a real-world scenario, this would involve more complex operations.
    module_description = await get_module_description(request.course_title, request.module_title, request.module_topics, request.wrong_questions)
    return {"description": module_description.description}
    
@router.post("/suggestion")
async def suggestion(request: ContentSuggestion):
    """
    Generates a personalized learning suggestion based on course title, module title, and optional topics.
    Returns a concise and engaging summary of the module's key concepts.
    """
    suggestion = await get_suggestion_agent_response(request.course_title, request.module_title, request.module_topics, request.wrong_questions)
    return {"suggestion": suggestion.description}

@router.post(
    "/explanation",
    response_model=ExplanationOutput,
    summary="Explain or reinforce a piece of text based on user diagnostics."
)
async def get_explanation_endpoint(req: ExplanationRequest) -> ExplanationOutput:
    """
    - If the request has no scale/questions/answers, returns the raw text.
    - Otherwise, generates an enhanced explanation via LLM, targeting the user's weak points.
    """
    dicti = {}
    return await get_explanation(
        raw_text=req.raw_text,
        scale=req.scale,
        questions=req.questions,
        answers=req.answers,
        knowledge=dicti,
    )


class QuizRequest(BaseModel):
    user_id: str
    current_skill: str
    module_title: str

class QuizSubmitRequest(BaseModel):
    user_id: str
    quiz: List[Dict]
    answers: List[str]


@router.post("/quiz")
async def get_quiz_endpoint(request: QuizRequest):
    quiz_output = await get_quiz(request.course_title, request.module_title, request.module_topics)
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
