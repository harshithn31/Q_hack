import logging
import asyncio
from typing import List, Dict, Optional, TypedDict
from langgraph.graph import StateGraph, END

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Add project root to path for imports ---
# This ensures modules like llm_agents can be found when running the script directly
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Import Real Agents & Helpers ---
from llm_agents.intent_classifier_agent import classify_intent
from llm_agents.analyst_agent import analyst_agent, AnalystAgentOutput
from llm_agents.course_retrieval_agent import run_budget_aware_course_retrieval, ModuleRecommendation
from llm_agents.pricing_agent import adjust_pricing, Module as PricingModule # Rename to avoid conflict
from course_retriever import CourseRetriever # Assuming this is still used to get candidates

# --- Define State Schema ---
class AgentState(TypedDict):
    user_input: Optional[str]
    intent: Optional[str]
    resume_skills: Optional[List[str]] # Skills extracted from resume
    goal_skills: Optional[List[str]] # Skills user wants to learn (from goal setting/convo)
    skills_gap: Optional[List[str]] # Calculated gap
    budget_eur: Optional[float] # User's budget
    candidate_courses: Optional[List[Dict]] # Courses from retriever
    recommended_modules: Optional[List[ModuleRecommendation]] # Modules from course agent
    final_bundle: Optional[List[PricingModule]] # Priced bundle
    response: Optional[str] # The final message for the user for this turn
    error: Optional[str] # To capture any errors during execution

# --- Wrapper Nodes for Agents ---

async def intent_classifier_node(state: AgentState) -> AgentState:
    """Classifies user intent using full chat transcript for context."""
    logging.info("Running intent classifier...")
    user_input = state.get('user_input', '')
    chat_transcript = state.get('chat_transcript', [])
    if not user_input and not chat_transcript:
        return {"response": "Please provide some input.", "intent": "end"} # Handle empty input
    try:
        intent_result = await classify_intent(user_input=user_input, chat_transcript=chat_transcript)
        logging.info(f"Classified intent: {intent_result}")
        return {"intent": intent_result['intent'], "raw_intent": intent_result['raw_intent']}
    except Exception as e:
        logging.error(f"Intent classification failed: {e}")
        return {"error": f"Intent classification failed: {e}", "intent": "error"}

async def analyst_node(state: AgentState) -> AgentState:
    """Runs the skill gap analysis agent."""
    logging.info("Running analyst agent...")
    skills = state.get('resume_skills', [])
    goal_skills = state.get('goal_skills', []) # Needs to be populated earlier
    user_input = state.get('user_input', '')

    # If goal_skills is missing, just pass user_input as the goal (LLM will extract skills)
    if not goal_skills and user_input:
        goal_skills = [user_input.strip()]
        state['goal_skills'] = goal_skills

    if not skills or not goal_skills:
        logging.warning(f"Missing skills or goal_skills for analysis. skills: {skills}, goal_skills: {goal_skills}")
        return {"response": "I need both your current skills (from your resume) and your goal skills to analyze the gap. Could you tell me your goal?", "intent": "end"}

    try:
        result: AnalystAgentOutput = await analyst_agent.run(skills=skills, goal_skills=goal_skills)
        logging.info("Analyst agent finished.")
        return {
            "skills_gap": result.skills_gap,
            "response": f"{result.gap_message}\n{result.offer_custom_course_message}"
        }
    except Exception as e:
        logging.error(f"Analyst agent failed: {e}")
        return {"error": f"Analyst agent failed: {e}", "response": "Sorry, I couldn't analyze the skill gap right now."}

async def course_node(state: AgentState) -> AgentState:
    """Runs the course retrieval agent."""
    logging.info("Running course retrieval agent...")
    skills_gap = state.get('skills_gap')
    budget_eur = state.get('budget_eur') # Needs to be populated

    if not skills_gap:
        logging.warning("Skills gap not found in state for course agent.")
        return {"response": "I need to know your skill gap first. Would you like me to analyze it based on your goals?", "intent": "gap_analysis"} # Route back? Or end?

    try:
        # Retrieve candidate courses (assuming CourseRetriever works as before)
        retriever = CourseRetriever()
        candidate_courses = retriever.retrieve(skills_gap, top_k=5) # Or load from state if pre-retrieved
        logging.info(f"Retrieved {len(candidate_courses)} candidate courses.")

        # Run budget-aware retrieval
        result = await run_budget_aware_course_retrieval(
            skills_gap=skills_gap,
            candidate_courses=candidate_courses,
            budget_eur=budget_eur
        )
        logging.info("Course retrieval agent finished.")
        # Response will be generated by the pricing node which follows
        return {"recommended_modules": result.recommended_modules if result else []}
    except Exception as e:
        logging.error(f"Course retrieval agent failed: {e}")
        return {"error": f"Course retrieval agent failed: {e}", "response": "Sorry, I couldn't find courses right now."}

async def pricing_node(state: AgentState) -> AgentState:
    """Runs the pricing adjustment logic."""
    logging.info("Running pricing adjustment...")
    recommended_modules = state.get('recommended_modules', [])
    budget_eur = state.get('budget_eur')

    if not recommended_modules:
         logging.warning("No recommended modules found for pricing.")
         # If course_node failed or returned empty, this node shouldn't run ideally,
         # but handle gracefully if it does.
         return {"response": "It seems no suitable course modules were found. Would you like to refine your goals or budget?"}


    if budget_eur is None:
        logging.warning("Budget not found in state for pricing agent.")
        # Handle case where budget wasn't set - maybe ask user?
        # For now, proceed without adjustment or use a default? Let's assume required.
        return {"response": "I need your budget to finalize the course bundle price. How much are you looking to spend (in EUR)?", "intent": "set_budget"} # Need a way to handle this intent

    try:
        # Adapt recommended_modules structure for adjust_pricing if needed
        # Assuming ModuleRecommendation has price info or can be adapted
        # For simulation, let's assume ModuleRecommendation has a 'price' field
        pricing_input = [PricingModule(**m.dict()) for m in recommended_modules if hasattr(m, 'price')] # Adapt as needed

        final_bundle: List[PricingModule] = await adjust_pricing(
             recommended_modules=pricing_input,
             budget_eur=budget_eur
        )
        logging.info("Pricing adjustment finished.")

        # Format response
        if not final_bundle:
            response = "Unfortunately, I couldn't create a bundle within your budget with the recommended modules."
        else:
            bundle_details = "\n".join([f"- {m.module_title} ({m.course_title}): €{m.final_price}" for m in final_bundle])
            total_price = sum(m.final_price for m in final_bundle)
            response = f"Here's your personalized learning bundle fitting your budget (€{budget_eur}):\n{bundle_details}\n\nTotal: €{total_price}"

        return {"final_bundle": final_bundle, "response": response}
    except Exception as e:
        logging.error(f"Pricing agent failed: {e}")
        return {"error": f"Pricing agent failed: {e}", "response": "Sorry, I couldn't finalize the pricing right now."}

async def fallback_node(state: AgentState) -> AgentState:
    """Handles unrecognized intents or provides a default response."""
    logging.info("Running fallback node.")
    error = state.get("error")
    if error:
         return {"response": f"An error occurred: {error}"}
    return {"response": "I'm not sure how to help with that. Could you please rephrase or tell me about your learning goals?"}

# --- Routing Logic ---
def route_by_intent(state: AgentState):
    """
    Routes the user to the correct node based on intent classification results.
    Handles both dict and str intent outputs from the LLM.
    """
    intent = state.get('intent')
    raw_intent = state.get('raw_intent')
    logging.info(f"Routing based on intent: {intent}, raw_intent: {raw_intent}")

    # If intent is a dict (sometimes LLMs return JSON), extract the string
    if isinstance(intent, dict):
        intent_str = intent.get('intent')
    else:
        intent_str = intent

    # Route to analyst_node for skill gap/learning intents
    if intent_str == 'analyst_node' or raw_intent == 'skill_gap_analysis':
        return 'analyst_node'
    # Route to course_node for course recommendation intents
    elif intent_str == 'course_node' or raw_intent == 'course_recommendation':
        return 'course_node'
    # Route to pricing_node for pricing intents
    elif intent_str == 'pricing_node' or raw_intent == 'pricing_query':
        return 'pricing_node'
    # End on error
    elif intent_str == 'error':
        return END
    # Default to fallback for anything else
    else:
        return 'fallback_node'  # Reason: Unrecognized or unsupported intent


# --- Build LangGraph DAG ---
def build_intent_graph():
    graph_builder = StateGraph(AgentState)

    # Add nodes
    graph_builder.add_node('intent_classifier', intent_classifier_node)
    graph_builder.add_node('analyst_node', analyst_node)
    graph_builder.add_node('course_node', course_node)
    graph_builder.add_node('pricing_node', pricing_node)
    graph_builder.add_node('fallback_node', fallback_node)

    # Set entry point
    graph_builder.set_entry_point('intent_classifier')

    # Define edges
    graph_builder.add_conditional_edges(
        'intent_classifier',
        route_by_intent,
        {
            'analyst_node': 'analyst_node',
            'course_node': 'course_node',
            'fallback_node': 'fallback_node',
            END: END
        }
    )

    # Define standard end paths
    graph_builder.add_edge('analyst_node', END)
    graph_builder.add_edge('fallback_node', END)

    # Special sequence: course -> pricing -> END
    graph_builder.add_edge('course_node', 'pricing_node')
    graph_builder.add_edge('pricing_node', END)

    # Compile the graph
    graph = graph_builder.compile()
    logging.info("LangGraph compiled successfully.")
    return graph

# --- Simulation ---
async def run_simulation():
    dag = build_intent_graph()
    thread_id = "simulated_thread_1" # Simulate thread persistence

    # Initial state (e.g., after resume upload)
    current_state = AgentState(
        user_input=None,
        intent=None,
        resume_skills=["Python", "SQL", "Basic Statistics"],
        goal_skills=None, # Needs to be set by user
        skills_gap=None,
        budget_eur=None, # Needs to be set by user
        candidate_courses=None,
        recommended_modules=None,
        final_bundle=None,
        response=None,
        error=None
    )
    print(f"\n--- Initial State ({thread_id}) ---")
    print(current_state)

    # Turn 1: User sets goal
    user_message_1 = "I want to become a data scientist, focusing on machine learning and cloud platforms. My budget is around 150 EUR."
    print(f"\n--- Turn 1: User Input ---")
    print(user_message_1)
    current_state['user_input'] = user_message_1
    # Simulate API call - invoke graph
    result_state = await dag.ainvoke(current_state, config={"configurable": {"thread_id": thread_id}})
    # Update state (API would save/load this)
    current_state.update(result_state)
    print(f"\n--- Turn 1: AI Response ---")
    print(current_state.get('response'))
    print(f"\n--- Turn 1: Final State ---")
    print(current_state)
    # --- Manually update state based on intent/response (if needed for simulation) ---
    # For simulation, let's assume intent classifier correctly identified 'goal_setting'
    # and a separate process (or conversation agent) extracted these:
    current_state['goal_skills'] = ["Machine Learning", "Cloud Platforms (AWS/Azure/GCP)", "Advanced Statistics", "Data Visualization"]
    current_state['budget_eur'] = 150.0
    current_state['user_input'] = None # Clear input for next turn
    current_state['response'] = None # Clear response for next turn
    current_state['intent'] = None # Clear intent
    # ------------------------------------------------------------------------------------


    # Turn 2: User asks for gap analysis
    user_message_2 = "What skills am I missing for that goal?"
    print(f"\n--- Turn 2: User Input ---")
    print(user_message_2)
    current_state['user_input'] = user_message_2
    # Simulate API call
    result_state = await dag.ainvoke(current_state, config={"configurable": {"thread_id": thread_id}})
    current_state.update(result_state)
    print(f"\n--- Turn 2: AI Response ---")
    print(current_state.get('response'))
    print(f"\n--- Turn 2: Final State ---")
    print(current_state)
    # --- Manually update state ---
    current_state['user_input'] = None
    current_state['response'] = None
    current_state['intent'] = None
    # ---------------------------

    # Turn 3: User asks for courses
    user_message_3 = "Okay, show me a course bundle for those gaps."
    print(f"\n--- Turn 3: User Input ---")
    print(user_message_3)
    current_state['user_input'] = user_message_3
     # Simulate API call
    result_state = await dag.ainvoke(current_state, config={"configurable": {"thread_id": thread_id}})
    current_state.update(result_state)
    print(f"\n--- Turn 3: AI Response ---")
    print(current_state.get('response')) # Should be pricing info now
    print(f"\n--- Turn 3: Final State ---")
    print(current_state)
    # --- Manually update state ---
    current_state['user_input'] = None
    current_state['response'] = None
    current_state['intent'] = None
    # ---------------------------


if __name__ == '__main__':
    print("Starting LangGraph DAG simulation...")
    # Add dummy price to ModuleRecommendation for simulation if needed
    # This is hacky - ideally CourseRetriever/Agent provides price
    if not hasattr(ModuleRecommendation, 'price'):
         ModuleRecommendation.model_fields['price'] = (int, Field(default=50)) # Add dummy price field

    asyncio.run(run_simulation())
    print("\nSimulation finished.")
