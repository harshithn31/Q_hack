from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field
from pydantic_ai import Agent
import asyncio

class ExplanationRequest(BaseModel):
    raw_text: str = Field(..., description="The original text to simplify or enhance.")
    scale: Optional[int] = Field(
        None,
        description="Self-reported understanding level (e.g. 1–5)."
    )
    questions: Optional[List[str]] = Field(
        None,
        description="List of questions the user got wrong."
    )
    knowledge: Optional[List[str]] = Field(
        None,
        description="List of knowledge."
    )
    answers: Optional[List[str]] = Field(
        None,
        description="User’s answers to those questions."
    )

class ExplanationOutput(BaseModel):
    simplified_text: str = Field(
        ...,
        description="Either the raw text (if no diagnostics) or the LLM-enhanced explanation."
    )
    analytics: str = Field(
        ...,
        description="The analytics."
    )

explanation_agent = Agent(
    model="openai:gpt-4o-mini",
    output_type=ExplanationOutput,
    system_prompt=(
        "You are an educational assistant.  "
        "Given the following inputs:\n"
        "  • raw_text: the source content to be explained\n"
        "  • scale: the user’s self-reported understanding (1–5)\n"
        "  • questions: questions the user got wrong\n"
        "  • knowledge: knowledge about the module\n"
        "  • answers: their answers\n\n"
        "Produce a JSON object:\n"
        "  {\"simplified_text\": \"<an explanation that reinforces the material, "
        "addresses their weak points, and makes the raw text clearer>\"}\n"
        "Be concise but thorough, and explicitly revisit any concepts tied to the questions."
    )
)

async def get_explanation(
    raw_text: str,
    scale: Optional[int] = None,
    questions: Optional[List[str]] = None,
    knowledge: Optional[Dict[str]] = None,
    answers: Optional[List[str]] = None
) -> ExplanationOutput:
    # If no diagnostics provided, skip the LLM and just return the raw text
    if scale is None and not questions and not answers:
        return ExplanationOutput(simplified_text=raw_text)

    # Otherwise, call the agent with everything packed into a dict
    payload: Dict[str, Any] = {
        "raw_text": raw_text,
        "scale": scale or 0,
        "questions": questions or [],
        "knowledge": knowledge or {},
        "answers": answers or [],
    }
    result = await explanation_agent.run(**payload)
    return result.output

if __name__ == "__main__":
    # --- Sample inputs for demonstration ---
    sample_raw_text = (
        "In Python, a list comprehension is a concise way to create lists. "
        "You can use an expression followed by a for-clause, "
        "then zero or more for- or if-clauses."
    )
    sample_scale = 2
    sample_questions = [
        "What keyword introduces the iteration in a list comprehension?",
        "How do you filter items in a list comprehension?"
    ]
    sample_knowledge = [
        "Basic for-loops in Python",
        "Conditional expressions"
    ]
    sample_answers = ["list", "using if"]  # intentional mistakes

    # --- Run the explanation generator ---
    explanation_output = asyncio.run(
        get_explanation(
            raw_text=sample_raw_text,
            scale=sample_scale,
            questions=sample_questions,
            knowledge=sample_knowledge,
            answers=sample_answers,
        )
    )

    # --- Print results ---
    print("=== Simplified Explanation ===")
    print(explanation_output.simplified_text)
    print("\n=== Analytics ===")
    print(explanation_output.analytics)