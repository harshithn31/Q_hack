"""
FastAPI routes for Personalized Learning Marketplace backend.
Exposes pipeline as an async API endpoint.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from pydantic import BaseModel
from graph.langgraph_intent_dag import build_intent_graph

dag = build_intent_graph()
from llm_agents.quiz_agent import get_quiz, validate_quiz_answers, QuizQuestion
from embeddings.utils import extract_resume_text
from typing import List, Dict
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class PipelineStepRequest(BaseModel):
    state: dict
    user_input: str | None = None
    thread_id: str | None = None

@router.post("/pipeline-step")
async def pipeline_step(request: PipelineStepRequest):
    # --- ENFORCE thread_id presence ---
    if not request.thread_id:
        raise HTTPException(status_code=400, detail="Missing thread_id. All pipeline-step requests must include a thread_id.")
    thread_id = request.thread_id
    config = {"configurable": {"thread_id": thread_id}}

    # Prepare input for the graph
    graph_input = dict(request.state or {})
    if request.user_input is not None:
        graph_input['user_input'] = request.user_input

    # Run the intent-driven DAG
    try:
        result = await dag.ainvoke(graph_input, config=config)
        response = {
            "response": result.get("response"),
            "state": result,
            "thread_id": thread_id
        }
        return response
    except Exception as e:
        logger.error(f"Pipeline step error for thread {thread_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Pipeline execution error: {e}")


# Simple in-memory XP/badge store for demo (keyed by user_id)
USER_XP = {}
USER_BADGES = {}

import uuid

RESUME_STORE = {}

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    print(f"[UPLOAD] Received upload request: filename={file.filename}, content_type={file.content_type}")
    """
    Accepts a PDF or TXT resume, extracts text securely, greets the user, and returns a resume_id and extracted skills for later use.
    """
    try:
        text = extract_resume_text(await file.read(), file.filename)
        if not text.strip():
            print(f"[UPLOAD] Extraction failed: No extractable text found in {file.filename}")
            raise HTTPException(status_code=400, detail="No extractable text found in resume.")
        resume_id = str(uuid.uuid4())
        RESUME_STORE[resume_id] = text
        print(f"[UPLOAD] Successfully stored resume_id={resume_id} for {file.filename}")
        # Run resume extraction agent logic here (greet + extract skills)
        from llm_agents.resume_agent import extract_with_agent
        result = await extract_with_agent(text)
        return {
            "resume_id": resume_id,
            "skills": result.skills,
            "summary": result.summary,
            "encouragement_message": result.encouragement_message,
            "ask_goal_message": result.ask_goal_message
        }
    except ValueError as e:
        print(f"[UPLOAD] ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[UPLOAD] Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Resume extraction failed due to a server error.")

class StartConversationRequest(BaseModel):
    resume_id: str

class AnalyzeSkillGapRequest(BaseModel):
    resume_id: str
    goal_skills: list[str]

class RecommendBundleRequest(BaseModel):
    resume_id: str
    consent: bool = True
    budget_eur: float | None = None

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
    current_skill: str
    module_title: str

class QuizSubmitRequest(BaseModel):
    user_id: str
    quiz: List[Dict]
    answers: List[str]

@router.post("/start-conversation")
async def start_conversation(request: StartConversationRequest):
    """
    Starts the conversation: runs ResumeAgent and returns skills, summary, encouragement, and upskill prompt.
    """
    resume_text = RESUME_STORE.get(request.resume_id)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Invalid or expired resume_id.")
    from llm_agents.resume_agent import extract_with_agent
    result = await extract_with_agent(resume_text)
    return {
        "skills": result.skills,
        "summary": result.summary,
        "encouragement_message": result.encouragement_message,
        "ask_goal_message": result.ask_goal_message
    }

@router.post("/analyze-skill-gap")
async def analyze_skill_gap(request: AnalyzeSkillGapRequest):
    """
    Analyzes the skill gap between resume and user goal. Returns missing skills, gap message, and course offer prompt.
    """
    resume_text = RESUME_STORE.get(request.resume_id)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Invalid or expired resume_id.")
    from llm_agents.resume_agent import extract_with_agent
    from llm_agents.analyst_agent import analyst_agent
    resume_result = await extract_with_agent(resume_text)
    analyst_result = await analyst_agent.run(skills=resume_result.skills, goal_skills=request.goal_skills)
    return {
        "skills_gap": analyst_result.output.skills_gap,
        "gap_message": analyst_result.output.gap_message,
        "offer_custom_course_message": analyst_result.output.offer_custom_course_message
    }

@router.post("/recommend-bundle")
async def recommend_bundle(request: RecommendBundleRequest):
    """
    Runs the course retrieval and pricing pipeline after user consents. Returns recommended modules and pricing.
    """
    if not request.consent:
        return {"message": "User did not consent to course recommendation."}
    resume_text = RESUME_STORE.get(request.resume_id)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Invalid or expired resume_id.")
    from llm_agents.resume_agent import extract_with_agent
    from llm_agents.analyst_agent import analyst_agent
    from llm_agents.course_retrieval_agent import course_retrieval_agent
    from llm_agents.pricing_agent import pricing_agent
    # Extract skills
    resume_result = await extract_with_agent(resume_text)
    # Assume goal_skills were provided in previous step (for demo, use all skills_gap)
    analyst_result = await analyst_agent.run(skills=resume_result.skills, goal_skills=resume_result.skills)
    skills_gap = analyst_result.output.skills_gap
    # Retrieve courses
    from course_retriever import CourseRetriever
    retriever = CourseRetriever()
    candidate_courses = retriever.retrieve(skills_gap, top_k=5)
    course_result = await course_retrieval_agent.run(skills_gap=skills_gap, candidate_courses=candidate_courses)
    # Price bundle
    price_result = await pricing_agent.run(recommended_modules=course_result.output.recommended_modules, budget_eur=request.budget_eur)
    return {
        "recommended_modules": course_result.output.recommended_modules,
        "final_bundle": price_result.output.final_bundle,
        "pricing": getattr(price_result.output, "pricing", None)
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
