from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.embedders import OpenAITextEmbedder, OpenAIDocumentEmbedder
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.rankers import SentenceTransformersDiversityRanker
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder
from haystack.components.preprocessors import DocumentSplitter
from haystack.utils import Secret
import os
from dotenv import load_dotenv

load_dotenv()


class RAG:
    def __init__(self, documents_dir=os.path.join("documents", "txt")):
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.documents_dir = os.path.join(root_dir, documents_dir)
        self.documents = self._load_documents()

    def _load_documents(self):
        documents = []
        for filename in os.listdir(self.documents_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.documents_dir, filename)
                source = filename[:-4].replace("_", "/")
                with open(file_path, "r", encoding="utf-8") as f:
                    documents.append({"source": source, "content": f.read()})
        return documents

    def _init_splitter(self):
        splitter = DocumentSplitter(
            split_by="sentence", split_length=500, split_overlap=50, language="en"
        )
        splitter.warm_up()
        return splitter

    def _create_documents(self):
        return [
            Document(content=d["content"], id=str(i), meta={"source": d["source"]})
            for i, d in enumerate(self.documents)
        ]

    def _split_documents(self):
        split_docs = []
        for doc in self.docs:
            split_docs += self.splitter.run(documents=[doc])["documents"]
        return split_docs

    def _init_document_store(self):
        document_store = InMemoryDocumentStore()
        document_store.write_documents(self.split_docs)
        return document_store

    def _init_retriever(self):
        return InMemoryBM25Retriever(document_store=self.document_store, top_k=6)

    def _init_generator(self):
        return OpenAIGenerator(
            api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
            model="gpt-4.1-nano",
            generation_kwargs={"temperature": 0.3, "max_tokens": 256},
        )

    def _init_prompt_builder(self):
        return PromptBuilder(
            template="""
            You are an AI assistant tasked with answering questions using the provided context.
            Your response must be:
            - **Concise** and in your own words.
            - Based **only on the documents** below — **cite them** where relevant by providing the URL in parentheses (e.g., (Source: https://example.com)).
            - If the question is unclear or too broad, ask for clarification.

            --- CONTEXT ---
            {% for doc in documents %}
            Document {{ loop.index }} (Source: https://{{ doc.meta.source }}):
            {{ doc.content }}

            {% endfor %}
            ----------------

            Question: {{ question }}

            Answer:
            """,
            required_variables=["documents", "question"],
        )

    def _build_pipeline(self):
        rag = Pipeline()
        rag.add_component("retriever", self.retriever)
        rag.add_component("prompt_builder", self.prompt_builder)
        rag.add_component("generator", self.generator)
        rag.connect("retriever.documents", "prompt_builder.documents")
        rag.connect("prompt_builder", "generator")
        return rag

    def get_pipeline(self):
        return self.pipeline


class BaselineRAG(RAG):
    def __init__(self, documents_dir=os.path.join("documents", "txt")):
        super().__init__(documents_dir)
        self.splitter = self._init_splitter()
        self.docs = self._create_documents()
        self.split_docs = self._split_documents()
        self.document_store = self._init_document_store()
        self.retriever = self._init_retriever()
        self.generator = self._init_generator()
        self.prompt_builder = self._init_prompt_builder()
        self.pipeline = self._build_pipeline()


class RerankerRAG(RAG):
    def __init__(self, documents_dir=os.path.join("documents", "txt")):
        super().__init__(documents_dir)
        self.splitter = self._init_splitter()
        self.docs = self._create_documents()
        self.split_docs = self._split_documents()
        self.document_store = self._init_document_store()
        self.retriever = self._init_retriever()
        self.ranker = self._init_ranker()
        self.generator = self._init_generator()
        self.prompt_builder = self._init_prompt_builder()
        self.pipeline = self._build_pipeline()

    def _init_ranker(self):
        ranker = SentenceTransformersDiversityRanker(
            model="sentence-transformers/all-MiniLM-L6-v2", similarity="cosine", top_k=4
        )
        ranker.warm_up()
        return ranker

    def _build_pipeline(self):
        rag = Pipeline()
        rag.add_component("retriever", self.retriever)
        rag.add_component("ranker", self.ranker)
        rag.add_component("prompt_builder", self.prompt_builder)
        rag.add_component("generator", self.generator)
        rag.connect("retriever.documents", "ranker.documents")
        rag.connect("ranker.documents", "prompt_builder.documents")
        rag.connect("prompt_builder", "generator")
        return rag


class DenseRAG(RAG):
    def __init__(self, documents_dir=os.path.join("documents", "txt")):
        super().__init__(documents_dir)
        self.text_embedder = self._init_text_embedder()
        self.splitter = self._init_splitter()
        self.docs = self._create_documents()
        self.split_docs = self._split_documents()
        self.embeddings = self._embed_documents()
        self.document_store = self._init_document_store()
        self.retriever = self._init_retriever()
        self.generator = self._init_generator()
        self.prompt_builder = self._init_prompt_builder()
        self.pipeline = self._build_pipeline()

    def _init_text_embedder(self):
        return OpenAITextEmbedder(
            api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
        )

    def _init_splitter(self):
        splitter = DocumentSplitter(
            split_by="sentence", split_length=100, split_overlap=25, language="en"
        )
        splitter.warm_up()
        return splitter

    def _split_documents(self):
        split_docs = []
        for doc in self.docs:
            split_docs += self.splitter.run(documents=[doc])["documents"]
        return split_docs

    def _embed_documents(self):
        document_embedder = OpenAIDocumentEmbedder(
            api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
        )
        embeddings = document_embedder.run(documents=self.split_docs)["documents"]
        return embeddings

    def _init_document_store(self):
        document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")
        document_store.write_documents(self.embeddings)
        return document_store

    def _init_retriever(self):
        return InMemoryEmbeddingRetriever(document_store=self.document_store, top_k=10)

    def _build_pipeline(self):
        rag = Pipeline()
        rag.add_component("text_embedder", self.text_embedder)
        rag.add_component("retriever", self.retriever)
        rag.add_component("prompt_builder", self.prompt_builder)
        rag.add_component("generator", self.generator)
        rag.connect("text_embedder.embedding", "retriever.query_embedding")
        rag.connect("retriever.documents", "prompt_builder.documents")
        rag.connect("prompt_builder", "generator")
        return rag


class DenseRerankerRAG(RAG):
    def __init__(self, documents_dir=os.path.join("documents", "txt")):
        super().__init__(documents_dir)
        self.text_embedder = self._init_text_embedder()
        self.splitter = self._init_splitter()
        self.docs = self._create_documents()
        self.split_docs = self._split_documents()
        self.embeddings = self._embed_documents()
        self.document_store = self._init_document_store()
        self.retriever = self._init_retriever()
        self.ranker = self._init_ranker()
        self.generator = self._init_generator()
        self.prompt_builder = self._init_prompt_builder()
        self.pipeline = self._build_pipeline()

    def _init_text_embedder(self):
        return OpenAITextEmbedder(
            api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
        )

    def _init_splitter(self):
        splitter = DocumentSplitter(
            split_by="sentence", split_length=100, split_overlap=25, language="en"
        )
        splitter.warm_up()
        return splitter

    def _split_documents(self):
        split_docs = []
        for doc in self.docs:
            split_docs += self.splitter.run(documents=[doc])["documents"]
        return split_docs

    def _embed_documents(self):
        document_embedder = OpenAIDocumentEmbedder(
            api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
        )
        embeddings = document_embedder.run(documents=self.split_docs)["documents"]
        return embeddings

    def _init_document_store(self):
        document_store = InMemoryDocumentStore(embedding_similarity_function="cosine")
        document_store.write_documents(self.embeddings)
        return document_store

    def _init_retriever(self):
        return InMemoryEmbeddingRetriever(document_store=self.document_store, top_k=10)

    def _init_ranker(self):
        ranker = SentenceTransformersDiversityRanker(
            model="sentence-transformers/all-MiniLM-L6-v2", similarity="cosine", top_k=4
        )
        ranker.warm_up()
        return ranker

    def _build_pipeline(self):
        rag = Pipeline()
        rag.add_component("text_embedder", self.text_embedder)
        rag.add_component("retriever", self.retriever)
        rag.add_component("ranker", self.ranker)
        rag.add_component("prompt_builder", self.prompt_builder)
        rag.add_component("generator", self.generator)
        rag.connect("text_embedder.embedding", "retriever.query_embedding")
        rag.connect("retriever.documents", "ranker.documents")
        rag.connect("ranker.documents", "prompt_builder.documents")
        rag.connect("prompt_builder", "generator")
        return rag


baseline_rag = BaselineRAG()
# reranker_rag = RerankerRAG()
# dense_rag = DenseRAG()
# dense_reranker_rag = DenseRerankerRAG()
