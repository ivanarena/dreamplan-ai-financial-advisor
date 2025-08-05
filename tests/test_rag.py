def test_baseline_rag(baseline_rag_pipeline):
    query = "What are the different types of Danish tax cards?"
    result = baseline_rag_pipeline.run(
        data={
            "retriever": {"query": query},
            "prompt_builder": {"question": query},
        },
        include_outputs_from={"retriever", "generator"},
    )

    assert "retriever" in result, "Missing retriever output"
    assert "documents" in result["retriever"], "Missing retriever documents"
    assert isinstance(result["retriever"]["documents"], list), (
        "Retriever documents should be a list"
    )
    assert len(result["retriever"]["documents"]) > 0, "No documents retrieved"

    assert "generator" in result, "Missing generator output"
    assert "replies" in result["generator"], "Missing generator replies"
    assert isinstance(result["generator"]["replies"], list), (
        "Generator replies should be a list"
    )
    assert len(result["generator"]["replies"]) > 0, "No replies generated"
    assert isinstance(result["generator"]["replies"][0], str), (
        "Generator reply should be a string"
    )


def test_reranker_rag(reranker_rag_pipeline):
    query = "What are the different types of Danish tax cards?"
    result = reranker_rag_pipeline.run(
        data={
            "retriever": {"query": query},
            "ranker": {"query": query},
            "prompt_builder": {"question": query},
        },
        include_outputs_from={"retriever", "generator"},
    )

    assert "retriever" in result, "Missing retriever output"
    assert "documents" in result["retriever"], "Missing retriever documents"
    assert isinstance(result["retriever"]["documents"], list), (
        "Retriever documents should be a list"
    )
    assert len(result["retriever"]["documents"]) > 0, "No documents retrieved"

    assert "generator" in result, "Missing generator output"
    assert "replies" in result["generator"], "Missing generator replies"
    assert isinstance(result["generator"]["replies"], list), (
        "Generator replies should be a list"
    )
    assert len(result["generator"]["replies"]) > 0, "No replies generated"
    assert isinstance(result["generator"]["replies"][0], str), (
        "Generator reply should be a string"
    )


def test_dense_rag(dense_rag_pipeline):
    query = "What are the different types of Danish tax cards?"
    result = dense_rag_pipeline.run(
        data={
            "text_embedder": {"text": query},
            "prompt_builder": {"question": query},
        },
        include_outputs_from={"retriever", "generator"},
    )

    assert "retriever" in result, "Missing retriever output"
    assert "documents" in result["retriever"], "Missing retriever documents"
    assert isinstance(result["retriever"]["documents"], list), (
        "Retriever documents should be a list"
    )
    assert len(result["retriever"]["documents"]) > 0, "No documents retrieved"

    assert "generator" in result, "Missing generator output"
    assert "replies" in result["generator"], "Missing generator replies"
    assert isinstance(result["generator"]["replies"], list), (
        "Generator replies should be a list"
    )
    assert len(result["generator"]["replies"]) > 0, "No replies generated"
    assert isinstance(result["generator"]["replies"][0], str), (
        "Generator reply should be a string"
    )


def test_dense_reranker_rag(dense_reranker_rag_pipeline):
    query = "What are the different types of Danish tax cards?"
    result = dense_reranker_rag_pipeline.run(
        data={
            "text_embedder": {"text": query},
            "ranker": {"query": query},
            "prompt_builder": {"question": query},
        },
        include_outputs_from={"retriever", "generator"},
    )

    assert "retriever" in result, "Missing retriever output"
    assert "documents" in result["retriever"], "Missing retriever documents"
    assert isinstance(result["retriever"]["documents"], list), (
        "Retriever documents should be a list"
    )
    assert len(result["retriever"]["documents"]) > 0, "No documents retrieved"

    assert "generator" in result, "Missing generator output"
    assert "replies" in result["generator"], "Missing generator replies"
    assert isinstance(result["generator"]["replies"], list), (
        "Generator replies should be a list"
    )
    assert len(result["generator"]["replies"]) > 0, "No replies generated"
    assert isinstance(result["generator"]["replies"][0], str), (
        "Generator reply should be a string"
    )
