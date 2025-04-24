"""
UpdateModuleDescriptionAgent: Update the module description based on common wrong answers.
- Input: module_title (str), wrong_answers_question (List[str])
- Output: description (str)
"""

from pydantic import BaseModel, Field
from typing import List
from pydantic_ai import Agent
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {api_key}")  

class UpdateModuleInput(BaseModel):
    module_title: str = Field(..., module_title="Title of the module to update.")
    course_title: str = Field(..., module_title="Title of the course to which the module belongs.")
    module_topics: List[str] = Field(..., module_title="List of topics covered in the module.")
    wrong_questions: List[str] = Field(..., module_title="List of questions where users often provide wrong answers.")

class UpdatedDescriptionOutput(BaseModel):
    description: str = Field(..., description="An improved module description that fills identified knowledge gaps.")

update_module_description_agent = Agent(
    model="openai:gpt-4o-mini",
    input_type=UpdateModuleInput,
    output_type=UpdatedDescriptionOutput,
    temperature=0.7,
    system_prompt=(
        "You are a curriculum improvement assistant. Based on the module title and a list of questions "
        "where users often provide wrong answers, enhance the original module description to better address knowledge gaps. "
        "Keep the description short (3-5 sentences), insightful, and more targeted. Use natural language and make sure the updated "
        "description is inclusive of the misunderstood concepts."
    )
)

async def get_updated_module_description(module_title: str, wrong_answers_question: List[str]) -> str:
    """
    Generate an updated module description using the update_module_description_agent.
    """
    dynamic_system_prompt = f"""
    You are a curriculum improvement assistant. Based on the module title "{module_title}", wrong_answers_question: {wrong_answers_question} and a list of questions
    where users often provide wrong answers, enhance the original module description to better address knowledge gaps.
    Keep the description short (3-5 sentences), insightful, and more targeted. Use natural language and make sure the updated
    description is inclusive of the misunderstood concepts.
    Respond in this JSON format:
    {{ "description": ... }}"""
    
    result = await update_module_description_agent.run(dynamic_system_prompt)
    return result

if __name__ == "__main__":
    # Example usage
    module_title = "Effective Communication in Business"
    wrong_answers_question = ["What is the most effective way to communicate in a business setting?",
                              "How does non-verbal communication impact business interactions?"]
    updated_description = asyncio.run(get_updated_module_description(module_title, wrong_answers_question))
    print(f"Module Title: {module_title}")
    print(f"Updated Description: {updated_description}")