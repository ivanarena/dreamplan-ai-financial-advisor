from agents import (
    Agent,
    TResponseInputItem,
    GuardrailFunctionOutput,
    RunContextWrapper,
    input_guardrail,
    Runner,
    output_guardrail,
    set_default_openai_key,
    # enable_verbose_stdout_logging
)
from components.prompts import (
    calculation_agent_instructions,
    dreamplan_agent_instructions,
    finance_agent_instructions,
    triage_agent_instructions,
    input_guardrail_instructions,
    output_guardrail_instructions,
)
import os
from dotenv import load_dotenv
from components.tools import call_calculation_api, call_rag
from pydantic import BaseModel

load_dotenv()
set_default_openai_key(os.getenv("OPENAI_API_KEY"))
# enable_verbose_stdout_logging()  # uncomment for debug


class ValidInput(BaseModel):
    is_input_valid: bool


class ValidOutput(BaseModel):
    is_output_valid: bool


input_guardrail_agent = Agent(
    name="Input Guardrail",
    instructions=input_guardrail_instructions,
    model="gpt-4.1-nano",
    output_type=ValidInput,
)

output_guardrail_agent = Agent(
    name="Output Guardrail",
    instructions=output_guardrail_instructions,
    model="gpt-4.1-nano",
    output_type=ValidOutput,
)


@input_guardrail
async def call_input_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(input_guardrail_agent, input)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_input_valid,
    )


@output_guardrail
async def call_output_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent, input)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_output_valid,
    )


calculation_agent = Agent(
    name="Calculation Agent",
    handoff_description="Specialist agent for interacting with the Calculation API",
    instructions=calculation_agent_instructions,
    model="gpt-4.1-nano",
    tools=[call_calculation_api],
)

dreamplan_agent = Agent(
    name="Dreamplan Agent",
    handoff_description="Specialist agent for interpreting the Calculation API responses and answering questions about Dreamplan",
    instructions=dreamplan_agent_instructions,
    model="gpt-4.1-nano",
)

finance_agent = Agent(
    name="Finance Agent",
    handoff_description="Specialist agent for answering finance-related questions with the aid of RAG",
    instructions=finance_agent_instructions,
    tools=[call_rag],
    model="gpt-4.1-nano",
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=triage_agent_instructions,
    handoffs=[calculation_agent, dreamplan_agent, finance_agent],
    input_guardrails=[call_input_guardrail],
    output_guardrails=[call_output_guardrail],
    model="gpt-4.1-mini",
)

# TODO choose specific models
