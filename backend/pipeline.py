"""
LangGraph DAG orchestration for Personalized Learning Marketplace MVP.
- Wires ResumeAgent, ConversationAgent, CourseRetrievalAgent, PricingAgent.
- Includes a test DAG run with mock data.
"""
from .agents_resume import ResumeAgent, ResumeAgentInput
from .agents_conversation import ConversationAgent, ConversationAgentInput
from .agents_course_retrieval import CourseRetrievalAgent, CourseRetrievalAgentInput
from .agents_pricing import PricingAgent, PricingAgentInput

from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from typing import Any, Dict

# Define shared state for the DAG
def dict_merge(a: Dict, b: Dict) -> Dict:
    out = dict(a)
    out.update(b)
    return out

class PipelineState(BaseModel):
    resume_text: str = ""
    chat_transcript: str = ""
    skills: Any = None
    summary: Any = None
    target_role: Any = None
    goal_skills: Any = None
    budget_eur: Any = None
    skills_gap: Any = None
    recommended_courses: Any = None
    final_bundle: Any = None

# Node wrappers
def run_resume_agent(state: PipelineState) -> Dict:
    agent = ResumeAgent()
    output = agent.run(ResumeAgentInput(resume_text=state.resume_text))
    return {"skills": output.skills, "summary": output.summary}

def run_conversation_agent(state: PipelineState) -> Dict:
    agent = ConversationAgent()
    output = agent.run(ConversationAgentInput(chat_transcript=state.chat_transcript))
    return {"target_role": output.target_role, "goal_skills": output.goal_skills, "budget_eur": output.budget_eur}

def compute_skills_gap(state: PipelineState) -> Dict:
    # Reason: Compute missing skills for course recommendation
    skills = set(state.skills or [])
    goals = set(state.goal_skills or [])
    gap = list(goals - skills)
    return {"skills_gap": gap}

def run_course_retrieval_agent(state: PipelineState) -> Dict:
    agent = CourseRetrievalAgent()
    output = agent.run(CourseRetrievalAgentInput(skills_gap=state.skills_gap))
    return {"recommended_courses": output.recommended_courses}

def run_pricing_agent(state: PipelineState) -> Dict:
    agent = PricingAgent()
    output = agent.run(PricingAgentInput(
        recommended_courses=state.recommended_courses,
        budget_eur=state.budget_eur,
    ))
    return {"final_bundle": output.final_bundle}

# Build LangGraph DAG
graph = StateGraph(PipelineState)
graph.add_node("resume", run_resume_agent)
graph.add_node("conversation", run_conversation_agent)
graph.add_node("skills_gap", compute_skills_gap)
graph.add_node("course_retrieval", run_course_retrieval_agent)
graph.add_node("pricing", run_pricing_agent)

graph.set_entry_point("resume")
graph.add_edge("resume", "conversation")
graph.add_edge("conversation", "skills_gap")
graph.add_edge("skills_gap", "course_retrieval")
graph.add_edge("course_retrieval", "pricing")
graph.add_edge("pricing", END)

dag = graph.compile()

# Test DAG run with mock data
if __name__ == "__main__":
    mock_resume = """
    John Doe\nExperienced software developer skilled in Python, machine learning, and web development.\nProjects include cloud deployments and data science pipelines.\n"""
    mock_chat = """
    User: I want to become a data scientist and work in AI. My budget is 200 euros.\nAssistant: Great! What skills do you want to focus on?\nUser: Machine learning, Python, and cloud computing.\n"""
    state = PipelineState(resume_text=mock_resume, chat_transcript=mock_chat)
    result = dag.invoke(state)
    print("--- Pipeline Output ---")
    print("Summary:", result.summary)
    print("Skills:", result.skills)
    print("Target Role:", result.target_role)
    print("Goal Skills:", result.goal_skills)
    print("Skills Gap:", result.skills_gap)
    print("Recommended Courses:", result.recommended_courses)
    print("Final Bundle:", result.final_bundle)