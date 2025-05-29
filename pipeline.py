from dispatching import triage_agent
from agents import ItemHelpers, Runner
from typing import List
from agents import InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered


def format_chat(chat: List[dict]) -> str:
    return "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat])


async def pipeline(chat: List):
    # TODO write about dynamic context injection strategy
    try:
        triage = Runner.run_streamed(
            triage_agent,
            input=format_chat(chat) if chat else "",
        )
        print(chat)
        print("=== Run starting ===")
        async for event in triage.stream_events():
            # We'll ignore the raw responses event deltas
            if event.type == "raw_response_event":
                continue
            # When the agent updates, print that
            elif event.type == "agent_updated_stream_event":
                print(f"Agent updated: {event.new_agent.name}")
                continue
            # When items are generated, print them
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    print("-- Tool was called")
                elif event.item.type == "tool_call_output_item":
                    print(f"-- Tool output: {event.item.output}")
                elif event.item.type == "message_output_item":
                    print(
                        f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}"
                    )
                else:
                    pass  # Ignore other event types

        print("=== Run complete ===")
        return triage.final_output
    except InputGuardrailTripwireTriggered:
        print("Input guardrail was triggered, please rephrase your question.")
        return {
            "error": "Input guardrail was triggered, please rephrase your question."
        }
    except OutputGuardrailTripwireTriggered:
        print("Output guardrail was triggered, please check the output.")
        return {"error": "Output guardrail was triggered, please check the output."}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
