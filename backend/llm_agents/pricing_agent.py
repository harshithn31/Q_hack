"""
PricingAgent: Adjusts recommended module-level bundle to fit within user's budget.
- Input: recommended_modules (List[Module]), budget_eur (int)
- Output: final_bundle (List[Module] with final_price)
- Modern pydantic-ai Agent pattern, async-ready.
"""
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Optional

class Module(BaseModel):
    course_title: str
    module_title: str
    module_description: str
    selected_subtopics: List[str]
    why_selected: str
    price: int
    final_price: Optional[int] = None

class PricingAgentOutput(BaseModel):
    final_bundle: List[Module] = Field(..., description="Final bundle of modules with adjusted pricing.")

async def adjust_pricing(recommended_modules: List[Module], budget_eur: int) -> List[Module]:
    total = sum(m.price for m in recommended_modules)
    if total <= budget_eur:
        for m in recommended_modules:
            m.final_price = m.price
        return recommended_modules
    discount = budget_eur / total if total > 0 else 1.0
    bundle = []
    for m in recommended_modules:
        new_price = max(1, int(m.price * discount))
        bundle.append(Module(**m.dict(), final_price=new_price))
    # Drop modules if still over budget due to rounding
    while sum(m.final_price for m in bundle) > budget_eur and bundle:
        bundle.pop()
    return bundle

pricing_agent = Agent(
    "openai:gpt-4o-mini",
    output_type=PricingAgentOutput,
    system_prompt=(
        "Given a recommended module-level learning bundle and a budget in EUR, adjust the pricing so the bundle fits the budget. "
        "Each module has: course_title, module_title, module_description, selected_subtopics (list), why_selected, price. "
        "If needed, apply proportional discounts (to the price field) and drop modules if necessary. "
        "Respond in this JSON format: {\"final_bundle\": [{\"course_title\": ..., \"module_title\": ..., \"module_description\": ..., \"selected_subtopics\": [...], \"why_selected\": ..., \"price\": 0, \"final_price\": 0}, ...]}"
    ),
)

# Usage example (async):
# result = await pricing_agent.run(recommended_courses=[...], budget_eur=200)
# print(result.output)
