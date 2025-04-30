from dispatching import triage_agent
from agents import Runner
import json


async def pipeline(prompt: str):
    triage = await Runner.run(
        triage_agent,
        prompt,
    )
    import pprint as pp

    print("\n\n====== TRIAGE FINAL OUTPUT =======\n")
    triage_output = {}
    try:
        triage_output = json.loads(triage.final_output.strip("```json\n").strip("```"))
        pp.pprint(triage_output)
    except json.JSONDecodeError:
        print("The output is not a valid JSON string:")
        print(triage.final_output)

    assert "agent_name" in triage_output
    assert "agent_response" in triage_output

    # dreamplan = await Runner.run(
    #     dreamplan_agent,
    #     triage.final_output,
    # )
    # judge = await Runner.run(
    #     judge_agent,
    #     dreamplan.final_output,
    # )
    # pp.pprint(result)
    print("\n\n======DREAMPLAN FINAL OUTPUT=======\n")
    # print(dreamplan.final_output)
