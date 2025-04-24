"""
CourseRetrievalAgent: Selects and packages the most relevant modules/subtopics from candidate courses for a user's skill gap using an LLM.
- Input: skills_gap (List[str]), candidate_courses (List[Dict])
- Output: recommended_modules (List[Dict])
- Modern pydantic-ai Agent pattern, async-ready.
"""
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Dict

class ModuleRecommendation(BaseModel):
    course_title: str
    module_title: str
    module_description: str
    selected_subtopics: List[str]
    why_selected: str

class CourseRetrievalAgentOutput(BaseModel):
    recommended_modules: List[ModuleRecommendation] = Field(..., description="List of selected modules packaged for the user.")

# Example input:
# skills_gap = ["Data Visualization", "APIs"]
# candidate_courses = [ ... ]
#
# Example output:
# {"recommended_modules": [
#   {
#     "course_title": "Data Analysis with Pandas",
#     "module_title": "Visualization with Matplotlib",
#     "module_description": "Plotting and visualizing data.",
#     "selected_subtopics": ["Line & Bar Charts", "Histograms"],
#     "why_selected": "Directly addresses the user's need for Data Visualization."
#   },
#   ...
# ]}

course_retrieval_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=CourseRetrievalAgentOutput,
    system_prompt=(
        "You are an expert learning path designer for a personalized education platform. "
        "Given a user's skill gaps and a list of candidate courses (each with modules and subtopics), your job is to select and package the most relevant modules and subtopics to help close those gaps.\n"
        "Instructions:\n"
        "- For each skill gap, select the most relevant module(s) from any course.\n"
        "- Prefer diversity: avoid selecting multiple modules covering the same content unless necessary.\n"
        "- For each module, select only the subtopics that are most relevant to the skill gap(s).\n"
        "- For each recommended module, provide a short, clear rationale in 'why_selected'.\n"
        "- Do NOT include modules that do not directly help close the skill gaps.\n"
        "- Output a JSON object with a key 'recommended_modules', containing a list of objects with: course_title, module_title, module_description, selected_subtopics (list), why_selected.\n"
        "- Be concise and actionable.\n"
        "Example output:\n"
        '{"recommended_modules": [ {"course_title": "...", "module_title": "...", "module_description": "...", "selected_subtopics": ["..."], "why_selected": "..."}, ... ]}'
    ),
)

# Usage example (async):
# result = await course_retrieval_agent.run(skills_gap=[...], candidate_courses=[...])
# print(result.output)
