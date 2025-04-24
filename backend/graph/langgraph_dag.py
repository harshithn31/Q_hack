print(">>> LANGGRAPH DAG LOADED (ensure this prints on every reload)")
import logging
logging.basicConfig(level=logging.INFO)
print(">>> Importing interrupt from langgraph.prebuilt")
from langgraph.prebuilt import interrupt

"""
LangGraph DAG orchestration for Personalized Learning Marketplace MVP (Human-in-the-Loop).
Nodes:
- resume       : Extract resume info, encouragement, ask goal
- wait_goal    : Pause for user to set goal_skills
- conversation : Parse user input to target_role, goal_skills, budget, etc.
- analyze_gap  : Compute skill gaps, summary, offer course
- wait_consent : Pause for user consent
- course_rec   : Retrieve and package recommended modules
- pricing      : Price bundle
- quiz         : Generate quiz for first module
"""
import asyncio
import sys
from pathlib import Path
from pydantic import BaseModel
from typing import Any, List, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import logging

# Ensure backend root directory is in sys.path for module resolution when running as script
sys.path.append(str(Path(__file__).resolve().parent.parent))

from llm_agents.resume_agent import extract_with_agent
from llm_agents.conversation_agent import conversation_agent
from llm_agents.analyst_agent import analyst_agent
from llm_agents.course_retrieval_agent import course_retrieval_agent
from llm_agents.pricing_agent import pricing_agent

from course_retriever import CourseRetriever

class PipelineState(BaseModel):
    # Inputs
    resume_text: str = ""
    chat_transcript: str = ""
    # ResumeAgent outputs
    skills: List[str] = []
    summary: str = ""
    encouragement_message: str = ""
    ask_goal_message: str = ""
    # ConversationAgent outputs
    target_role: Optional[str] = None
    goal_skills: Optional[List[str]] = None
    budget_eur: Optional[float] = None
    preferences: Optional[str] = None
    context: Optional[str] = None
    # AnalystAgent outputs
    skills_gap: List[str] = []
    gap_message: str = ""
    offer_custom_course_message: str = ""
    # CourseRetrievalAgent outputs
    recommended_modules: Any = None
    # PricingAgent outputs
    final_bundle: Any = None
    # Fields to store context for interruption
    current_prompt: Optional[str] = None
    expected_input_field: Optional[str] = None


# Node wrappers

async def run_resume_node(state: PipelineState) -> dict:
    logger = logging.getLogger(__name__)
    logger.info(f"--- [run_resume_node] --- STATE: {state}")
    logger.info("--- RUNNING RESUME AGENT ---")
    result = await extract_with_agent(state.resume_text)
    logger.info(f"--- RESUME AGENT COMPLETED --- Extracted Skills: {len(result.skills)}")
    return {
        "skills": result.skills,
        "summary": result.summary,
        "encouragement_message": result.encouragement_message,
        "ask_goal_message": result.ask_goal_message,
    }

def wait_for_goal(state: PipelineState):
    """Pauses the graph execution until the user provides their goal skills."""
    logger = logging.getLogger(__name__)
    logger.info("--- WAITING FOR GOAL ---")
    prompt = f"{state.encouragement_message}\n\n{state.ask_goal_message}".strip()
    logger.debug(f"Prompting user for goal: {prompt}")

    # Set state fields for interruption context BEFORE interrupting
    state.current_prompt = prompt
    state.expected_input_field = "goal_skills"

    # Return the interrupt object so LangGraph pauses and emits event
    return interrupt({
        "message": prompt,
        "expected_input_field": "goal_skills"
    })
    # logger.info("--- INTERRUPTED FOR GOAL --- Triggered. Node returns None.")

async def run_conversation_node(state: PipelineState) -> dict:
    logger = logging.getLogger(__name__)
    logger.info(f"--- [run_conversation_node] --- STATE: {state}")
    result = await conversation_agent.run(chat_transcript=state.chat_transcript)
    logger.info(f"--- [run_conversation_node] COMPLETED --- target_role: {result.output.target_role}")
    return {
        "target_role": result.output.target_role,
        "goal_skills": result.output.goal_skills,
        "budget_eur": result.output.budget_eur,
        "preferences": result.output.preferences,
        "context": result.output.context,
    }

def run_analyze_gap(state: PipelineState) -> dict:
    result = asyncio.run(analyst_agent.run(skills=state.skills, goal_skills=state.goal_skills or []))
    return {
        "skills_gap": result.output.skills_gap,
        "gap_message": result.output.gap_message,
        "offer_custom_course_message": result.output.offer_custom_course_message,
    }

def wait_for_consent(state: PipelineState):
    logger = logging.getLogger(__name__)
    logger.info(f"--- [wait_for_consent] --- STATE: {state}")
    logger.info("--- WAITING FOR CONSENT ---")
    prompt = state.offer_custom_course_message
    logger.debug(f"Prompting user for consent: {prompt}")
    state.current_prompt = prompt
    state.expected_input_field = "consent"
    logger.info("--- TRIGGERING CONSENT INTERRUPT ---")
    return interrupt({
        "message": prompt,
        "expected_input_field": "consent"
    })

async def run_course_rec(state: PipelineState) -> dict:
    retriever = CourseRetriever()
    candidate_courses = retriever.retrieve(state.skills_gap or [], top_k=5)
    result = await course_retrieval_agent.run(skills_gap=state.skills_gap or [], candidate_courses=candidate_courses)
    return {"recommended_modules": result.output.recommended_modules}

async def run_pricing_node(state: PipelineState) -> dict:
    logger = logging.getLogger(__name__)
    logger.info(f"--- [run_pricing_node] --- STATE: {state}")
    result = await pricing_agent.run(recommended_modules=state.recommended_modules, budget_eur=state.budget_eur)
    logger.info(f"--- [run_pricing_node] COMPLETED --- final_bundle: {result.output.final_bundle}")
    return {"final_bundle": result.output.final_bundle}


# Build LangGraph DAG
graph = StateGraph(PipelineState)
graph.add_node("resume", run_resume_node)
graph.add_node("wait_goal", wait_for_goal)
graph.add_node("conversation", run_conversation_node)
graph.add_node("analyze_gap", run_analyze_gap)
graph.add_node("wait_consent", wait_for_consent)
graph.add_node("course_rec", run_course_rec)
graph.add_node("pricing", run_pricing_node)

graph.set_entry_point("resume")
graph.add_edge("resume", "wait_goal")
graph.add_edge("wait_goal", "conversation")
graph.add_edge("conversation", "analyze_gap")
graph.add_edge("analyze_gap", "wait_consent")
graph.add_edge("wait_consent", "course_rec")
graph.add_edge("course_rec", "pricing")
graph.add_edge("pricing", END)

dag = graph.compile(checkpointer=MemorySaver())

# For offline testing only
import uuid

def run_full_mvp(resume_text: str, chat_transcript: str) -> PipelineState:
    state = PipelineState(resume_text=resume_text, chat_transcript=chat_transcript)
    # Always provide a thread_id for offline/test runs
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    # Use asyncio to run the async API, since nodes are async
    import asyncio
    return asyncio.run(dag.ainvoke(state, config=config))

if __name__ == "__main__":
    # Example
    state = run_full_mvp(
        resume_text="John Doe\nExperienced in Python and ML.",
        chat_transcript=""
    )
    try:
        # For Pydantic v2+
        print(state.model_dump_json(indent=2))
    except AttributeError:
        try:
            # For Pydantic v1
            import json
            print(json.dumps(state.model_dump(), indent=2))
        except Exception:
            print(str(state))
