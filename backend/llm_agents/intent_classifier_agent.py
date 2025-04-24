import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Dict
from pydantic_ai import Agent

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class IntentClassifierOutput(BaseModel):
    """
    Output schema for the intent classifier agent.
    - intent: Node name for DAG routing (analyst_node, course_node, pricing_node, fallback_node)
    - raw_intent: Fine-grained user intent (greet, goodbye, thank_you, small_talk, unrecognized, skill_gap_analysis, course_recommendation, pricing_query)
    """
    intent: str = Field(..., description="Routing node for the user's intent. One of: analyst_node, course_node, pricing_node, fallback_node.")
    raw_intent: str = Field(..., description="Fine-grained intent type. E.g., greet, goodbye, thank_you, small_talk, unrecognized, skill_gap_analysis, course_recommendation, pricing_query.")

intent_classifier_agent = Agent(
    "openai:gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    output_type=IntentClassifierOutput,
    system_prompt=(
        "You are an intent classifier for a personalized learning assistant. "
        "Given a user's message or the full conversation, classify it into one of the following routing nodes: "
        "- analyst_node (the user wants to upskill, learn, improve, asks about missing skills, skill gaps, or requests analysis of their resume/goals. This includes phrases like 'I want to upskill in cloud', 'I would like to learn AI', 'How can I improve in data science?', 'What am I missing for a cloud role?', 'What skills should I improve?') "
        "- course_node (the user asks about courses, learning resources, recommendations, or expresses interest in learning a specific topic or technology. This includes 'What courses are available for cloud?', 'Recommend a course for Python', 'Suggest learning resources for ML', 'Are there any courses for AWS?') "
        "- pricing_node (the user asks about price, cost, budget, or cheaper options. E.g., 'How much is this course?', 'Show me cheaper options', 'What is the price?', 'My budget is 100 EUR') "
        "- fallback_node (the user greets, says goodbye, thanks or the intent is unrecognized/unsupported. E.g., 'Hi', 'Thanks', 'Goodbye', 'Tell me a joke', 'Who are you?') "
        "Additionally, output a fine-grained 'raw_intent' field: one of greet, goodbye, thank_you, small_talk, unrecognized, skill_gap_analysis, course_recommendation, pricing_query. "
        "\n"
        "Here are some examples:\n"
        "User: I want to upskill in cloud\nIntent: analyst_node\n"
        "User: How can I improve my Python skills?\nIntent: analyst_node\n"
        "User: What skills am I missing for a data scientist role?\nIntent: analyst_node\n"
        "User: What courses are available for cloud?\nIntent: course_node\n"
        "User: Recommend a course for Python\nIntent: course_node\n"
        "User: How much is this course?\nIntent: pricing_node\n"
        "User: Show me cheaper options\nIntent: pricing_node\n"
        "User: Hi\nIntent: fallback_node\n"
        "User: Thanks\nIntent: fallback_node\n"
        "User: Tell me a joke\nIntent: fallback_node\n"
        "Respond ONLY with a valid JSON: {\"intent\": \"analyst_node|course_node|pricing_node|fallback_node\", \"raw_intent\": \"...\"}"
    ),
)

async def classify_intent(user_input: str = None, chat_transcript: list = None) -> Dict[str, str]:
    """
    Classifies user input and/or chat transcript according to the intent DAG. Returns a dict with 'intent' and 'raw_intent'.
    If input is empty, defaults to fallback_node/greet.
    If chat_transcript is provided, use it as context for classification.
    """
    if chat_transcript and isinstance(chat_transcript, list) and len(chat_transcript) > 0:
        # Build a conversation string for richer context
        transcript_text = "\n".join([f"{m['role']}: {m['content']}" for m in chat_transcript if m.get('role') and m.get('content')])
        prompt = f"Conversation so far:\n{transcript_text}\n\nGiven the above, classify the user's current intent."
        run_input = prompt
    else:
        run_input = user_input or ""
    if not run_input.strip():
        return {"intent": "fallback_node", "raw_intent": "no_input"}
    result = await intent_classifier_agent.run(user_input=run_input)
    return {"intent": result.output.intent, "raw_intent": result.output.raw_intent}
