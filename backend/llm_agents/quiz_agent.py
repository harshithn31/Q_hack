"""
QuizAgent: Generates or retrieves MCQ quizzes for a given skill/module.
- Input: current_skill (str), module_title (str)
- Output: quiz (List[Dict])
- Modern pydantic-ai Agent pattern, async-ready.
"""
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Dict
from embeddings.loader import load_quiz
import asyncio
import os

from dotenv import load_dotenv
from pydantic_ai import Agent


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: {api_key}")  # Debugging line to check if the key is loaded

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    
class QuizAgentOutput(BaseModel):
    quiz: List[QuizQuestion] = Field(..., description="List of MCQ questions.")

class ValidationAgentInput(BaseModel):
    correct_answers: List[str]
    user_answers: List[str]

class ValidationAgentOutput(BaseModel):
    correct_answers: List[str] = Field(..., description="List of correct answers.")
    user_answers: List[str] = Field(..., description="List of user answers.")
    scale: float = Field(..., description="Score in range of 0-10, 0 lowest and 10 highest.")
    description: str = Field(..., description="Explain why the answers are correct or not.")

    
quiz_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=QuizAgentOutput,
    system_prompt=(
         "You are a quiz generator. Given the module title, generate a quiz with 10 multiple-choice questions. "
        "These questions should focus on the specific subject of the module and test knowledge on its key concepts. "
        "For example, if the module title is 'Effective Communication in Business', the questions should revolve around topics like business communication techniques, verbal and non-verbal communication, feedback, listening skills, cultural communication, and so on. "
        "Each question should have 4 options, and the correct answer should be clearly indicated. "
        "The goal is to test key concepts and practical applications of the module. "
        "Ensure the questions are diverse and cover different aspects of the topic. "
        "If this is a repeated request for the same skill/module, generate a different set of questions than previously returned. "
        "Respond in this JSON format: "
        "{\"quiz\": [{\"question\": ..., \"options\": [...], \"correct_answer\": ...}, ...]}"
    ),
)

validate_agent = Agent(
    model="openai:gpt-4o-mini",
    input_type=ValidationAgentInput,
    output_type=ValidationAgentOutput,
    temperature=0.8,
    system_prompt=(
        "You are a quiz evaluator. Given two lists: correct_answers and user_answers (both of same length), "
        "compare each answer and generate a score out of 10. Provide a short explanation "
        "highlighting what was answered correctly or incorrectly. Respond in this JSON format: "
        "{\"correct_answers\": [...], \"user_answers\": [...], \"scale\": ..., \"description\": ...}"
    )
)

async def get_quiz(course_title: str, module_title: str, topics: List[str]) -> QuizAgentOutput:
    
    dynamic_system_prompt = f"""
    You are a quiz generator. Given the module title "{module_title}", course title : {course_title}, topics: {topics} generate a quiz with 10 multiple-choice questions. 
    These questions should focus on the specific subject of the module and test knowledge on its key concepts.
    Each question should have 4 options, and the correct answer should be clearly indicated.
    The goal is to test key concepts and practical applications of the module.
    Ensure the questions are diverse and cover different aspects of the topic.
    If this is a repeated request for the same skill/module, generate a different set of questions than previously returned.
    Respond in this JSON format:
    {{ "quiz": [{{"question": ..., "options": [...], "correct_answer": ...}}, ...] }}
    """

    result = await quiz_agent.run(dynamic_system_prompt)
    return result.output

async def validate_quiz_answers(quiz: List[QuizQuestion], answers: List[str]) -> Dict:
    

    correct = []
    incorrect = []
    for q, a in zip(quiz, answers):
        if a.strip().lower() == q.correct_answer.strip().lower():
            correct += 1
        else:
            incorrect.append(a.strip().lower())
            correct.append(q.correct_answer.strip().lower())
            
    dynamic_system_prompt = f"""
        You are a quiz evaluator. Your task is to analyze the performance of a quiz taker by comparing their answers to the correct answers. generate 5 questions with 3 options each.

        Given:
        - correct_answers: {correct}
        - user_answers: {incorrect}

        1. Calculate a score between 0 and 10 based on the number of correct answers.
        2. Provide a short summary of how the user performed. Be friendly and constructive — emojis are welcome 😄📘❗.
        3. Identify key areas or topics the user should improve on, based on the questions they got wrong. Present this as a bulleted list titled '📌 Areas of Improvement'.
        4. Keep it concise but informative, helpful, and encouraging.

        Output your response in the following JSON format:
        {{
        "correct_answers": [...], 
        "user_answers": [...], 
        "score": ..., 
        "description": "...", 
        "areas_of_improvement": [
            "Area 1",
            "Area 2",
            "Area 3" ....
        ]
        }}
        """
    
    result = await validate_agent.run(dynamic_system_prompt)
    
    return result
    
async def take_quiz():
    # Example usage
    course_title = "Python"
    module_title = "basic of python"
    topics = ["Python Basics", "Data Types", "Control Structures", "Functions"]
    quiz_output = await get_quiz(course_title, module_title, topics)
    print(quiz_output)
    answers = []
    for q in quiz_output.quiz:
        print(f"Q: {q.question}")
        print(f"Options: {', '.join(q.options)}")
        answers.append(str(input("Your answer: "))) 
        
    validated_output = await validate_quiz_answers(quiz_output.quiz, answers)
    
    print(f"Validation Result: {validated_output}")
    
            

if __name__ == "__main__":
    asyncio.run(take_quiz())
