from components.dispatching import triage_agent
from agents import Runner
import pandas as pd
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
from components.rag import RAG
import os
from time import time

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPERIMENT_DIR = os.path.join(ROOT_DIR, "experiment")
DATASET_DIR = os.path.join(EXPERIMENT_DIR, "data")


async def evaluate_dispatching():
    dataset = pd.read_csv(os.path.join(DATASET_DIR, "dispatching.csv"))  # noqa: F841
    for prompt in dataset["prompt"]:
        start_time = time()
        dispatcher = await Runner.run(triage_agent, input=prompt)
        end_time = time()
        dataset["result"] = dispatcher.last_agent.name
        dataset["time"] = end_time - start_time
    correct = (dataset["result"] == dataset["expected"]).sum()
    print(f"{correct} correctly dispatched prompts out of {dataset.shape[0]}.")
    dataset.to_csv(os.path.join(DATASET_DIR, "dispatching.csv"), index=False)
    return dataset


async def evaluate_rag():
    """referencing: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/#retrieval-augmented-generation"""
    run_rag_on_dataset()
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


def run_rag_on_dataset():
    dataset = os.path.join(DATASET_DIR, "questions.jsonl")
    with open(dataset, "r") as f:
        lines = f.readlines()  # noqa: F841
    data = [json.loads(line) for line in lines]
    rag = RAG().get_pipeline()
    print(len(data))
    i = 1
    for item in data:
        print(f"Processing item {i}/{len(data)}")
        i += 1
        query = item["user_input"]
        print(f"{query[:4]}...")
        start_time = time()
        result = rag.run(
            data={
                "retriever": {"query": query},
                "ranker": {"query": query},
                "prompt_builder": {"question": query},
            },
        )
        end_time = time()
        item["retrieved_contexts"] = [
            str(doc.content) for doc in result["retriever"]["documents"]
        ]
        item["response"] = result["generator"]["replies"][0]
        item["time"] = end_time - start_time

    # Save the outputs
    with open(dataset, "w") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def evaluate_performance():
    pd.read_csv(os.path.join(DATASET_DIR, "dispatching.csv"))
    rag_evaluation = os.path.join(DATASET_DIR, "questions.jsonl")
    with open(rag_evaluation, "r") as f:
        f.readlines()


# TODO: possibly run real user experiments and get feedback
