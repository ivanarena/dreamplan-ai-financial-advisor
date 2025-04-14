from agents import Agent, Runner, set_default_openai_key, enable_verbose_stdout_logging
from datasets.prompts import (
    calculation_agent_instructions,
    dreamplan_agent_instructions,
    finance_agent_instructions,
    triage_agent_instructions,
)
import os
import dotenv
from tools import call_calculation_api

dotenv.load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))
enable_verbose_stdout_logging()


calculation_agent = Agent(
    name="Calculation Agent",
    handoff_description="Specialist agent for interacting with the Calculation API",
    instructions=calculation_agent_instructions,
    tools=[call_calculation_api],
)

dreamplan_agent = Agent(
    name="Dreamplan Agent",
    handoff_description="Specialist agent for answering questions about Dreamplan",
    instructions=dreamplan_agent_instructions,
)

finance_agent = Agent(
    name="Finance Agent",
    handoff_description="Specialist agent for answering finance-related questions",
    instructions=finance_agent_instructions,
)

triage_agent = Agent(
    name="triage Agent",
    instructions=triage_agent_instructions,
    handoffs=[calculation_agent, dreamplan_agent, finance_agent],
)


async def main():
    result = await Runner.run(
        triage_agent,
        """
        I need to calculate target prices, I'm 43 and my spouse is 42,
        I earn 40000 per month and my wife 52000. We both have pension policies: my contribution is 
        10000 with an initial value of 100000 and she contributes 4000, already having 200000. 
        """,
    )
    # pp.pprint(result)
    print(result.final_output)
