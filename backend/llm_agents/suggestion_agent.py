"""
SuggestionAgent: Suggest better teaching methods based on questions students got wrong.
- Input: module_title (str), wrong_answers_question (List[str])
- Output: suggestions (str)
"""

import asyncio
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {api_key}")  # Debugging line to check if the key is loaded

class SuggestionInput(BaseModel):
    course_title: str = Field(..., module_title="Title of the course to which the module belongs.")
    module_title: str = Field(..., module_title="Title of the module to describe.")
    module_topics: List[str] = Field(..., module_title="List of topics covered in the module.")
    wrong_question: List[str]

class TeachingSuggestionsOutput(BaseModel):
    suggestions: str = Field(..., description="Practical teaching tips to address misunderstood topics.")

suggestion_agent = Agent(
    model="openai:gpt-4o-mini",
    input_type=SuggestionInput,
    output_type=TeachingSuggestionsOutput,
    temperature=0.8,
    system_prompt=(
        "You are a teaching assistant focused on instructional design. Given a module title and a list of frequently misunderstood questions, "
        "generate actionable suggestions for improving how this module is taught. Recommend better ways to present or explain the material, "
        "possible use of examples, analogies, visual aids, or interactive methods. Structure your suggestions clearly and constructively for instructors."
    )
)

async def get_teaching_suggestions(module_title: str, wrong_answers_question: List[str]) -> str:
    """
    Generate teaching suggestions using the suggestion_agent.
    """
    dynamic_system_prompt = f"""
    You are a teaching assistant focused on instructional design. Given the module title "{module_title}" and a list of frequently misunderstood questions {wrong_answers_question}, 
    generate actionable suggestions for improving how this module is taught. Recommend better ways to present or explain the material, possible use of examples, analogies, visual aids, or interactive methods. 
    Structure your suggestions clearly and constructively for instructors.
    Respond in this JSON format:
    {{ "suggestions": ... }}
    """
    
    result = await suggestion_agent.run(dynamic_system_prompt)
    return result

if __name__ == "__main__":
    # Example usage
    module_title = "Effective Communication in Business"
    wrong_answers_question = ["What is the importance of non-verbal communication?", "How does active listening improve communication?"]
    suggestions = asyncio.run(get_teaching_suggestions(module_title, wrong_answers_question))
    print(f"Module Title: {module_title}")
    print(f"Suggestions: {suggestions}")