"""
ModuleDescriptionAgent: Provides a short, clear description for a given module title.
- Input: module_title (str)
- Output: description (str)
"""

from pydantic import BaseModel, Field
from pydantic_ai import Agent
import asyncio
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {api_key}")  

class ModuleDescriptionInput(BaseModel):
    course_title: str = Field(..., module_title="Title of the course to which the module belongs.")
    module_title: str = Field(..., module_title="Title of the module to describe.")
    module_topics: List[str] = Field(..., module_title="List of topics covered in the module.")
    wrong_questions: List[str] = Field(..., module_title="List of questions where users often provide wrong answers.")
     
class ModuleDescriptionOutput(BaseModel):
    description: str = Field(..., description="A concise and engaging summary of the module's key concepts.")

module_description_agent = Agent(
    model="openai:gpt-4o-mini",
    input_type=ModuleDescriptionInput,
    output_type=ModuleDescriptionOutput,
    temperature=0.7,
    system_prompt=(
        "You are a course module explainer. Given a module title, write a concise and engaging description "
        "that introduces the topic and outlines its importance, core concepts, and applications. "
        "Keep it short (3-4 sentences), friendly, and informative. Avoid listing topics; instead, provide a natural summary. "
        "For example, if the module is 'Effective Communication in Business', describe how mastering communication "
        "skills contributes to workplace success, covers both verbal and non-verbal aspects, and is essential for teamwork and leadership."
    )
)

async def get_module_description(course_title: str, module_title: str, module_topics: List[str]) -> str:
    """
    Generate a module description using the module_description_agent.
    """
    dynamic_system_prompt = f"""
    You are a course module explainer. Given the module title "{module_title}", {course_title} {module_topics} write a concise and engaging description
    that introduces the topic and outlines its importance, core concepts, and applications and industrial relevance.
    Keep it short (3-4 sentences), friendly, and informative. Avoid listing topics; instead, provide a natural summary.
    Respond in this JSON format:
    {{ "quiz": [{{"module_description": ...}}] }}"""
    
    result = await module_description_agent.run(dynamic_system_prompt)
    return result

if __name__ == "__main__":
    # Example usage
    module_title = "Effective Communication in Business"
    description = asyncio.run(get_module_description(module_title))
    print(f"Module Title: {module_title}")
    print(f"Description: {description}")