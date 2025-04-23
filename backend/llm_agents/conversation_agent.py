from pydantic import BaseModel, Field
from pydantic_ai import Agent
import os
from dotenv import load_dotenv

load_dotenv()

from typing import List, Optional

class ConversationAgentOutput(BaseModel):
    target_role: str = Field(..., description="Target job role or learning goal.")
    goal_skills: List[str] = Field(..., description="List of skills the user wants to acquire.")
    budget_eur: Optional[float] = Field(None, description="User's budget in EUR.")
    preferences: Optional[str] = Field(None, description="Learning preferences if present.")
    context: Optional[str] = Field(None, description="Other relevant context if present.")

    preferences: Optional[str] = Field(None, description="Learning preferences if present.")
    context: Optional[str] = Field(None, description="Other relevant context if present.")

conversation_agent = Agent(
    "openai:gpt-4o",
    output_type=ConversationAgentOutput,
    system_prompt=(
        "You are an expert learning advisor AI. Given a user's chat transcript, extract the following as structured JSON:\n"
        "- target_role: The user's desired job or learning outcome\n"
        "- goal_skills: List of skills the user wants to acquire\n"
        "- budget_eur: If mentioned, the user's budget in euros\n"
        "- preferences: Any learning preferences (e.g., hands-on, video, project-based)\n"
        "- context: Any other relevant info (e.g., prior knowledge, constraints)\n"
        "Be robust to informal chat, multi-turn dialogue, and noisy input.\n"
        "Output only valid JSON in this format: {\"target_role\": \"...\", \"goal_skills\": [...], \"budget_eur\": 0, \"preferences\": \"...\", \"context\": \"...\"}"
    ),
)

# Usage example (async):
# result = await conversation_agent.run(chat_transcript="...your chat...")
# print(result.output)
