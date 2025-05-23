from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder
from haystack.components.preprocessors import DocumentSplitter
from haystack.utils import Secret
import os
from dotenv import load_dotenv

load_dotenv()

documents_dir = "documents/txt"
documents = []
for filename in os.listdir(documents_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(documents_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            documents.append(f.read())

splitter = DocumentSplitter(split_by="sentence", split_length=500, split_overlap=50)
splitter.warm_up()
docs = [Document(content=d, id=str(i)) for i, d in enumerate(documents)]
split_docs = []
for doc in docs:
    split_docs += splitter.run(documents=[doc])["documents"]

document_store = InMemoryDocumentStore()
document_store.write_documents(split_docs)

retriever = InMemoryBM25Retriever(document_store=document_store)

generator = OpenAIGenerator(
    api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
    model="gpt-4.1-nano",
    generation_kwargs={"temperature": 0.3, "max_tokens": 256},
)

prompt_builder = PromptBuilder(
    template="""
        You are an AI assistant tasked with answering questions using the provided context.
        Your response must be:
        - **Concise** and in your own words.
        - Based **only on the documents** below — **cite them** where relevant.
        - If the answer is not present, say **"I don't know"**.
        - If the question is unclear or too broad, ask for clarification.

        --- CONTEXT ---
        {% for doc in documents %}
        Document {{ loop.index }}:
        {{ doc.content }}

        {% endfor %}
        ----------------

        Question: {{ question }}

        Answer:
    """
)

rag = Pipeline()
rag.add_component("retriever", retriever)
rag.add_component("prompt_builder", prompt_builder)
rag.add_component("generator", generator)
rag.connect("retriever", "prompt_builder.documents")
rag.connect("prompt_builder", "generator")
