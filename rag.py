# rag_tool.py
from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder
from haystack.utils import Secret
import os
from dotenv import load_dotenv

load_dotenv()

# Setup only once at import
EXAMPLE_DOCS = [
    "An emergency fund is a savings account used to cover unexpected expenses such as medical bills or car repairs. Financial advisors typically recommend saving at least 3 to 6 months’ worth of living expenses.",
    "Index funds are mutual funds or ETFs that track a market index like the S&P 500. They offer broad market exposure, low fees, and are considered a good option for passive investing.",
    "Compound interest is the process by which interest is added to the principal, so that from that moment on, the interest that has been added also earns interest. This leads to exponential growth over time.",
    "A 401(k) is a retirement savings plan sponsored by an employer. It lets workers save and invest a portion of their paycheck before taxes are taken out, and employers often match contributions up to a certain limit.",
    "A credit score is a numerical representation of a person’s creditworthiness, ranging from 300 to 850. It's based on credit history, including payment history, amounts owed, length of credit history, and new credit.",
    "Diversification involves spreading investments across different asset classes to reduce risk. A diversified portfolio might include stocks, bonds, real estate, and commodities.",
    "The debt-to-income (DTI) ratio is calculated by dividing total monthly debt payments by gross monthly income. Lenders use this metric to assess a borrower's ability to manage monthly payments and repay debts.",
    "Robo-advisors are digital platforms that provide automated, algorithm-driven financial planning services with little to no human supervision. They are useful for beginners seeking low-cost portfolio management.",
    "Capital gains tax is a tax on the profit made from selling a non-inventory asset like stocks, bonds, or real estate. The rate depends on how long the asset was held and the taxpayer's income bracket.",
    "Inflation erodes purchasing power over time. If the inflation rate is 2% per year, something that costs $100 today will cost $102 in a year. Investments must beat inflation to generate real returns.",
]

document_store = InMemoryDocumentStore()
document_store.write_documents(
    [Document(content=d, id=str(i)) for i, d in enumerate(EXAMPLE_DOCS)]
)

retriever = InMemoryBM25Retriever(document_store=document_store)

generator = OpenAIGenerator(
    api_key=Secret.from_token(os.getenv("OPENAI_API_KEY")),
    model="gpt-3.5-turbo",
    generation_kwargs={"temperature": 0.3, "max_tokens": 256},
)

prompt_builder = PromptBuilder(
    template="""
Answer the question using the provided context. Your answer should be concise and in your own words.

Context:
{% for doc in documents %}
{{ doc.content }}
{% endfor %}

Question: {{question}}
Answer:
"""
)

# Build pipeline
rag = Pipeline()
rag.add_component("retriever", retriever)
rag.add_component("prompt_builder", prompt_builder)
rag.add_component("generator", generator)

# Connect components
rag.connect("retriever", "prompt_builder.documents")
rag.connect("prompt_builder", "generator")
