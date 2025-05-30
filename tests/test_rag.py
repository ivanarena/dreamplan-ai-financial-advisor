def test_rag(rag_pipeline):
    query = "What are the different types of Danish tax cards?"
    result = rag_pipeline.run(
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
