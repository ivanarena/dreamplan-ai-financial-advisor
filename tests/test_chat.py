from agents import Runner
import pytest


@pytest.mark.asyncio
async def test_chat(triage):
    chat = "What is the best way to save for retirement?"
    run = await Runner.run(
        triage,
        input=chat,
    )
    result = run.final_output
    assert isinstance(result, str), "Result should be a string"
    assert len(result) > 0, "Result should not be empty"
