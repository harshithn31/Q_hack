"""
Async LangGraph DAG orchestration for Personalized Learning Marketplace.
Wires resume_agent, conversation_agent, course_retrieval_agent, pricing_agent.
"""
from pydantic import BaseModel
from typing import Any, List
from llm_agents.resume_agent import resume_agent, ResumeAgentOutput
from llm_agents.conversation_agent import conversation_agent, ConversationAgentOutput
from llm_agents.course_retrieval_agent import course_retrieval_agent, CourseRetrievalAgentOutput
from llm_agents.pricing_agent import pricing_agent, PricingAgentOutput
from llm_agents.quiz_agent import quiz_agent, QuizAgentOutput

class PipelineState(BaseModel):
    resume_text: str = ""
    chat_transcript: str = ""
    
    # Only fields used by conversation_agent
    target_role: Any = None
    goal_skills: Any = None
    budget_eur: Any = None

    # Commented out since not used in this step
    skills: Any = None
    # summary: Any = None
    skills_gap: Any = None
    recommended_modules: Any = None
    # final_bundle: Any = None
    # quiz: Any = None
    # quiz_score: Any = None

async def run_resume_agent(state: PipelineState) -> dict:
    result = await resume_agent.run(state.resume_text)
    return {"skills": result.output.skills, "summary": result.output.summary}

async def run_conversation_agent(state: PipelineState) -> dict:
    result = await conversation_agent.run(state.chat_transcript)
    return {"target_role": result.output.target_role, "goal_skills": result.output.goal_skills, "budget_eur": result.output.budget_eur}

async def compute_skills_gap(state: PipelineState) -> dict:
    skills = set(state.skills or [])
    goals = set(state.goal_skills or [])
    gap = list(goals - skills)
    return {"skills_gap": gap}

from course_retriever import CourseRetriever

async def run_course_retrieval_agent(state: PipelineState) -> dict:
    """
    Retrieves top-N relevant courses (with modules), then uses LLM to select and package the most relevant modules/subtopics for the user's skill gap.
    Returns: {"recommended_modules": ...}
    """
    retriever = CourseRetriever()
    candidate_courses = retriever.retrieve(state.skills_gap, top_k=5)
    # Use LLM to select/package modules
    result = await course_retrieval_agent.run(skills_gap=state.skills_gap, candidate_courses=candidate_courses)
    return {"recommended_modules": result.output.recommended_modules}

async def run_pricing_agent(state: PipelineState) -> dict:
    result = await pricing_agent.run(recommended_modules=state.recommended_modules, budget_eur=state.budget_eur)
    return {"final_bundle": result.output.final_bundle}

async def run_quiz_agent(state: PipelineState) -> dict:
    # Use first missing skill and first course as quiz context
    skill = (state.skills_gap or ["skill"])[0]
    module = state.recommended_modules[0].module_title if state.recommended_modules else "Module"
    result = await quiz_agent.run(current_skill=skill, module_title=module)
    return {"quiz": result.output.quiz}

# Orchestration function (async, linear for MVP)
async def run_full_pipeline(resume_text: str, chat_transcript: str) -> PipelineState:
    state = PipelineState(resume_text=resume_text, chat_transcript=chat_transcript)
#    state_dict = await run_resume_agent(state)
#    state = state.copy(update=state_dict)
    state_dict = await run_conversation_agent(state)
    state = state.copy(update=state_dict)
    state_dict = await compute_skills_gap(state)
    state = state.copy(update=state_dict)
    state_dict = await run_course_retrieval_agent(state)
    state = state.copy(update=state_dict)
#    state_dict = await run_pricing_agent(state)
#    state = state.copy(update=state_dict)
#    state_dict = await run_quiz_agent(state)
#    state = state.copy(update=state_dict)
    return state

# Usage example (async):
# result_state = await run_full_pipeline(resume_text, chat_transcript)
# print(result_state.final_bundle)
