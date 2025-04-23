import pytest
from llm_agents.quiz_agent import quiz_agent, QuizAgentOutput
import asyncio

@pytest.mark.asyncio
async def test_quiz_agent_output_schema():
    # Minimal mock input
    skill = "Python"
    module = "Intro to Python"
    result = await quiz_agent.run(current_skill=skill, module_title=module)
    output = result.output
    # Validate output type
    assert isinstance(output, QuizAgentOutput)
    assert hasattr(output, "quiz")
    assert isinstance(output.quiz, list)
    for q in output.quiz:
        assert hasattr(q, "question")
        assert hasattr(q, "options")
        assert hasattr(q, "correct_answer")
        assert isinstance(q.options, list)
        assert q.correct_answer in q.options
