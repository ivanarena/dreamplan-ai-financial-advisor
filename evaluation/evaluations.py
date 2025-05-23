from dispatching import triage_agent
from agents import Runner
import pandas as pd
import pprint as pp
import json
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    ResponseRelevancy,
    LLMContextPrecisionWithoutReference,
    Faithfulness,
    ContextRelevance,
)
from ragas import evaluate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from ragas import EvaluationDataset
from rag import rag
import os

load_dotenv()

DATASET_DIR = "data"


async def evaluate_dispatching():
    dataset = pd.read_csv(os.path.join(DATASET_DIR, "dispatching.csv"))
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


async def evaluate_rag():
    """referencing: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/#retrieval-augmented-generation"""
    # Run the RAG pipeline on the dataset
    dataset = os.path.join(DATASET_DIR, "questions.jsonl")
    with open(dataset, "r") as f:
        lines = f.readlines()
    data = [json.loads(line) for line in lines]
    for item in data:
        query = item["user_input"]
        result = rag.run(
            data={"retriever": {"query": query}, "prompt_builder": {"question": query}},
            include_outputs_from={"retriever", "generator"},
        )
        item["retrieved_contexts"] = [
            str(doc.content) for doc in result["retriever"]["documents"]
        ]
        item["response"] = result["generator"]["replies"][0]

    # Save the outputs
    with open(dataset, "w") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    # Run evaluation
    evaluation_dataset = EvaluationDataset.from_jsonl(
        os.path.join(DATASET_DIR, "questions.jsonl")
    )
    print("Features in dataset:", evaluation_dataset.features())
    print("Total samples in dataset:", len(evaluation_dataset))
    evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4.1-nano"))
    result = evaluate(
        dataset=evaluation_dataset,
        metrics=[
            ResponseRelevancy(),
            LLMContextPrecisionWithoutReference(),
            Faithfulness(),
            ContextRelevance(),
        ],
        llm=evaluator_llm,
    )
    df = result.to_pandas()
    df.to_csv(os.path.join(DATASET_DIR, "rag_evaluation.csv"), index=False)
    return df
