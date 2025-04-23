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

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

class QuizAgentOutput(BaseModel):
    quiz: List[QuizQuestion] = Field(..., description="List of MCQ questions.")

quiz_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=QuizAgentOutput,
    system_prompt=(
        "Given a skill and module title, generate 3 multiple-choice questions to test understanding. "
        "Each question must have 4 options and indicate the correct answer. "
        "Respond in this JSON format: {\"quiz\": [{\"question\": ..., \"options\": [...], \"correct_answer\": ...}, ...]}"
    ),
)

async def get_quiz(current_skill: str, module_title: str) -> QuizAgentOutput:
    # Try static pool first
    static_quiz = load_quiz(current_skill, module_title)
    if static_quiz:
        return QuizAgentOutput(quiz=[QuizQuestion(**q) for q in static_quiz])
    # Fallback to LLM
    result = await quiz_agent.run(current_skill=current_skill, module_title=module_title)
    return result.output

def validate_quiz_answers(quiz: List[QuizQuestion], answers: List[str]) -> Dict:
    correct = 0
    for q, a in zip(quiz, answers):
        if a == q.correct_answer.lower():
            correct += 1
    score = correct / max(1, len(quiz))
    return {"score": score, "correct": correct, "total": len(quiz)}

if __name__ == "__main__":
    # Example usage
    current_skill = "Python"
    module_title = "Intro to Python"
    quiz_output = asyncio.run(get_quiz(current_skill, module_title))
    print(quiz_output)
    answers = []
    for q in quiz_output.quiz:
        print(f"Q: {q.question}")
        print(f"Options: {', '.join(q.options)}")
        answers.append(str(input("Your answer: ")).lower()) 
    validated_output = validate_quiz_answers(quiz_output.quiz, answers)
    print(f"Score: {validated_output['score']}, Correct: {validated_output['correct']}/{validated_output['total']}")
    print("Success")
    
    
