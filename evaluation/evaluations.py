from dispatching import triage_agent
from agents import Runner
import pandas as pd
import pprint as pp
import json


async def evaluate_dispatching():
    dataset = pd.read_csv("datasets/dispatching.csv")
    for prompt in dataset["prompt"]:
        dispatcher = await Runner.run(triage_agent, prompt)
        dispatcher_output = {}
        try:
            dispatcher_output = json.loads(
                dispatcher.final_output.strip("```json\n").strip("```")
            )
            pp.pprint(dispatcher_output)
        except json.JSONDecodeError:
            print("The output is not a valid JSON string:")
            print(dispatcher.final_output)

        assert "agent_name" in dispatcher_output
        assert "agent_response" in dispatcher_output

        dataset["result"] = dispatcher_output["agent_name"]
        dataset.to_csv("datasets/dispatching.csv", index=False)
    correct = (dataset["result"] == dataset["expected"]).sum()
    print(f"{correct} correctly dispatched prompts out of {dataset.shape[0]}.")
