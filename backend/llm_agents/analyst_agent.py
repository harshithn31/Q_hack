"""
AnalystAgent: Analyzes current vs. target skills, summarizes skill gap, and offers to create a custom course bundle.
- Input: skills (List[str]), goal_skills (List[str])
- Output: skills_gap (List[str]), gap_message (str), offer_custom_course_message (str)
"""
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List

class AnalystAgentOutput(BaseModel):
    skills_gap: List[str] = Field(..., description="List of missing skills needed to reach the goal.")
    gap_message: str = Field(..., description="Summary of the skill gap in friendly language.")
    offer_custom_course_message: str = Field(..., description="Prompt asking if the user wants a custom course bundle.")

analyst_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=AnalystAgentOutput,
    system_prompt=(
        "You are a friendly, growth-mindset career analyst. Given a user's current skills and their upskilling goal (desired skills), "
        "compare the two and list the missing skills (skill gap) as a JSON array. "
        "Then, write a short, highly supportive summary explaining which skills the user needs to learn to reach their goal, using positive, actionable language. "
        "Finally, ask the user if they would like a personalized course bundle to help fill these gaps, in an encouraging and motivating tone.\n"
        "Examples:\n"
        "Current skills: ['python', 'sql']\nGoal: ['cloud', 'data engineering']\n"
        "Output: {\"skills_gap\": [\"cloud\", \"data engineering\"], \"gap_message\": \"To achieve your goal, you only need to focus on cloud and data engineering skills. You're well on your way!\", \"offer_custom_course_message\": \"Would you like me to create a custom learning bundle to help you master these new skills?\"}\n"
        "Current skills: ['excel', 'statistics']\nGoal: ['machine learning', 'python']\n"
        "Output: {\"skills_gap\": [\"machine learning\", \"python\"], \"gap_message\": \"Great start! To reach your goal, learning machine learning and python will be valuable next steps.\", \"offer_custom_course_message\": \"Shall I recommend a course bundle to help you get there?\"}\n"
        "Always be concise, actionable, and supportive.\n"
        "Respond ONLY in this JSON format: {\"skills_gap\": [...], \"gap_message\": \"...\", \"offer_custom_course_message\": \"...\"}"
    ),
)

# Usage example (async):
# result = await analyst_agent.run(skills=[...], goal_skills=[...])
# print(result.output)
