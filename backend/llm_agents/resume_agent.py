"""
ResumeAgent: Extracts structured information from a user's resume text.
- Input: resume_text (str)
- Output: skills (List[str]), summary (str), experience_highlights (List[str]), learning_preferences (optional, str)

Example input:
resume_text = '''
Jane Doe\nSenior Data Analyst\nSkills: Python, SQL, Data Visualization\nExperience: Built dashboards, led analytics projects, mentored juniors. Prefers project-based learning.
'''

Example output:
{
  "skills": ["Python", "SQL", "Data Visualization"],
  "summary": "Senior Data Analyst with experience in dashboards and analytics projects.",
  "experience_highlights": ["Built dashboards", "Led analytics projects", "Mentored juniors"],
  "learning_preferences": "Prefers project-based learning."
}
"""
from pydantic import BaseModel, Field
from pydantic_ai import Agent
import os
from dotenv import load_dotenv

load_dotenv()

from typing import List, Optional
class ResumeAgentOutput(BaseModel):
    skills: List[str] = Field(..., description="List of extracted skills.")
    summary: str = Field(..., description="Short summary of the candidate.")
    experience_highlights: List[str] = Field(..., description="Key achievements or roles.")
    learning_preferences: Optional[str] = Field(None, description="Learning preferences if present.")

resume_agent = Agent(
    "openai:gpt-4o",
    output_type=ResumeAgentOutput,
    system_prompt=(
        "You are an expert career coach AI. Given a user's resume text, extract the following as structured JSON:\n"
        "- skills: List of technical and soft skills\n"
        "- summary: 1-2 sentence professional summary\n"
        "- experience_highlights: 2-5 bullet points of key achievements or roles\n"
        "- learning_preferences: If present, how the user prefers to learn (e.g., project-based, video, hands-on)\n"
        "Be robust to various resume formats and ignore irrelevant/noisy text.\n"
        "Output only valid JSON in this format: {\"skills\": [...], \"summary\": \"...\", \"experience_highlights\": [...], \"learning_preferences\": \"...\"}"
    ),
)

# Usage example (async):
# result = await resume_agent.run(resume_text="...your resume...")
# print(result.output)
