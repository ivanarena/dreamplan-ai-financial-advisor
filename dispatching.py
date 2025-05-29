from agents import Agent, set_default_openai_key  # , enable_verbose_stdout_logging
from data.prompts import (
    calculation_agent_instructions,
    dreamplan_agent_instructions,
    finance_agent_instructions,
    triage_agent_instructions,
)
import os
from dotenv import load_dotenv
from tools import call_calculation_api, call_rag

load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))
# enable_verbose_stdout_logging()  # uncomment for debug


calculation_agent = Agent(
    name="Calculation Agent",
    handoff_description="Specialist agent for interacting with the Calculation API",
    instructions=calculation_agent_instructions,
    tools=[call_calculation_api],
)

dreamplan_agent = Agent(
    name="Dreamplan Agent",
    handoff_description="Specialist agent for interpreting the Calculation API responses and answering questions about Dreamplan",
    instructions=dreamplan_agent_instructions,
)

finance_agent = Agent(
    name="Finance Agent",
    handoff_description="Specialist agent for answering finance-related questions with the aid of RAG",
    instructions=finance_agent_instructions,
    tools=[call_rag],
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=triage_agent_instructions,
    handoffs=[calculation_agent, dreamplan_agent, finance_agent],
)
