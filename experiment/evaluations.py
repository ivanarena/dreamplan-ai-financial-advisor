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
from components.rag import reranker_rag, baseline_rag, dense_rag
import os
from time import time
from agents import (
    Agent,
    set_default_openai_key,
)

load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))

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


async def evaluate_reranker_rag():
    """referencing: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/#retrieval-augmented-generation"""
    # run_reranker_rag_on_dataset() # Uncomment this line to run RAG on the dataset first
    evaluation_dataset = EvaluationDataset.from_jsonl(
        os.path.join(DATASET_DIR, "questions_reranker_Rag.jsonl")
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
    df.to_csv(os.path.join(DATASET_DIR, "evaluation_reranker_rag.csv"), index=False)
    return df


async def evaluate_baseline_rag():
    """referencing: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/#retrieval-augmented-generation"""
    run_baseline_rag_on_dataset()  # Uncomment this line to run Simple RAG on the dataset first
    evaluation_dataset = EvaluationDataset.from_jsonl(
        os.path.join(DATASET_DIR, "questions_baseline_rag.jsonl")
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
    df.to_csv(os.path.join(DATASET_DIR, "baseline_rag_evaluation.csv"), index=False)
    return df


async def evaluate_dense_rag():
    """referencing: https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/#retrieval-augmented-generation"""
    run_dense_rag_on_dataset()  # Uncomment this line to run Dense RAG on the dataset first
    evaluation_dataset = EvaluationDataset.from_jsonl(
        os.path.join(DATASET_DIR, "questions_dense_rag.jsonl")
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
    df.to_csv(os.path.join(DATASET_DIR, "evaluation_dense_rag.csv"), index=False)
    return df


def run_dense_rag_on_dataset():
    dataset = os.path.join(DATASET_DIR, "questions_dense_rag.jsonl")
    with open(dataset, "r") as f:
        lines = f.readlines()  # noqa: F841
    data = [json.loads(line) for line in lines]
    pipeline = dense_rag.get_pipeline()
    print(len(data))
    i = 1
    for item in data:
        print(f"Processing item {i}/{len(data)}")
        i += 1
        query = item["user_input"]
        print(f"{query[:4]}...")
        start_time = time()
        result = pipeline.run(
            data={
                "text_embedder": {"text": query},
                "ranker": {"query": query},
                "prompt_builder": {"question": query},
            },
            include_outputs_from={"retriever", "generator"},
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


def run_reranker_rag_on_dataset():
    dataset = os.path.join(DATASET_DIR, "questions_reranker_rag.jsonl")
    with open(dataset, "r") as f:
        lines = f.readlines()  # noqa: F841
    data = [json.loads(line) for line in lines]
    pipeline = reranker_rag.get_pipeline()
    print(len(data))
    i = 1
    for item in data:
        print(f"Processing item {i}/{len(data)}")
        i += 1
        query = item["user_input"]
        print(f"{query[:4]}...")
        start_time = time()
        result = pipeline.run(
            data={
                "retriever": {"query": query},
                "ranker": {"query": query},
                "prompt_builder": {"question": query},
            },
            include_outputs_from={"retriever", "generator"},
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


def run_baseline_rag_on_dataset():
    dataset = os.path.join(DATASET_DIR, "questions_baseline_rag.jsonl")
    with open(dataset, "r") as f:
        lines = f.readlines()  # noqa: F841
    data = [json.loads(line) for line in lines]
    pipeline = baseline_rag.get_pipeline()
    print(len(data))
    i = 1
    for item in data:
        print(f"Processing item {i}/{len(data)}")
        i += 1
        query = item["user_input"]
        print(f"{query[:4]}...")
        start_time = time()
        result = pipeline.run(
            data={
                "retriever": {"query": query},
                "prompt_builder": {"question": query},
            },
            include_outputs_from={"retriever", "generator"},
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


# def evaluate_performance():
#     pd.read_csv(os.path.join(DATASET_DIR, "dispatching.csv"))
#     rag_evaluation = os.path.join(DATASET_DIR, "questions.jsonl")
#     with open(rag_evaluation, "r") as f:
#         f.readlines()


async def run_llm_only_on_dataset():
    agent = Agent(
        name="Finance Agent",
        instructions="""
        You are a specialist agent for answering finance-related questions. The response should be in English but referring to Denmark and Danish financial context.
        
        Your role is to:
            1. Receive general financial questions from the user (e.g., about savings, investment strategies, retirement planning, etc.).
            2. Provide an accurate and trustworthy answer based on your knowledge.
        
        If the information cannot be confidently answered using the available context, respond with: This information is not in my knowledge, sorry.
        """,
        model="gpt-4.1-nano",
    )
    dataset = os.path.join(DATASET_DIR, "questions_llm_only.jsonl")
    with open(dataset, "r") as f:
        lines = f.readlines()  # noqa: F841
    data = [json.loads(line) for line in lines]
    i = 1
    for item in data:
        print(f"Processing item {i}/{len(data)}")
        i += 1
        query = item["user_input"]
        print(f"{query[:4]}...")
        start_time = time()
        runner = await Runner.run(
            agent,
            input=query,
        )
        end_time = time()
        item["retrieved_contexts"] = []  # No contexts for LLM only
        item["response"] = runner.final_output
        item["time"] = end_time - start_time

    # Save the outputs
    with open(dataset, "w") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


async def evaluate_llm_only():
    """Evaluate LLM only on the dataset."""
    await run_llm_only_on_dataset()  # Run the LLM on the dataset first
    evaluation_dataset = EvaluationDataset.from_jsonl(
        os.path.join(DATASET_DIR, "questions_llm_only.jsonl")
    )
    print("Features in dataset:", evaluation_dataset.features())
    print("Total samples in dataset:", len(evaluation_dataset))
    evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4.1-nano"))
    result = evaluate(
        dataset=evaluation_dataset,
        metrics=[
            ResponseRelevancy(),
        ],
        llm=evaluator_llm,
    )
    df = result.to_pandas()
    df.to_csv(os.path.join(DATASET_DIR, "evaluation_llm_only.csv"), index=False)
    return df
