from components.dispatching import triage_agent
from agents import Runner
from typing import List
from agents import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered


def format_messages(messages: List[dict]) -> str:
    return "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in messages]
    )


async def chat(messages: List):
    # TODO write about dynamic context injection strategy
    try:
        triage = await Runner.run(
            triage_agent,
            input=format_messages(messages) if messages else "",
        )
        print("LAST AGENT: ", triage.last_agent.name)
        return triage.final_output
    except InputGuardrailTripwireTriggered:
        print("Input guardrail was triggered, please rephrase your question.")
        return "Your question is not pertinent to the current context. Please rephrase your question."
    except OutputGuardrailTripwireTriggered:
        print("Output guardrail was triggered, please check the output.")
        return "There was an issue with the output. Please try again later."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An unexpected error occurred. Please try again later."
