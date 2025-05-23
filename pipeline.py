from dispatching import triage_agent, dreamplan_agent
from agents import ItemHelpers, Runner
from typing import List


async def pipeline(chat: List):
    triage = await Runner.run(
        triage_agent,
        input=str(chat[-1] if chat else ""),
        context=str(chat[:-1] if chat else ""),
    )
    print(chat)
    dreamplan_prompt = f"""
    Original user input: {triage.input}
    Last agent called: {triage.last_agent.name}
    Last agent output: {triage.final_output}
    """
    dreamplan = Runner.run_streamed(
        dreamplan_agent, input=dreamplan_prompt, context=str(chat)
    )
    print("=== Run starting ===")

    async for event in dreamplan.stream_events():
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
    return dreamplan.final_output
