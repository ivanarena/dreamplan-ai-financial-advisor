from calculation.client import client
from agents import function_tool
from calculation.factories import (
    build_person,
    build_incomes,
    build_policies,
    build_houses,
    build_liquid_assets,
)
from pydantic import BaseModel
from typing import Optional, List, Literal
from components.rag import rag
import json


class SavingsData(BaseModel):
    type: Literal["Cash", "Stocks"]
    initial_value: float
    monthly_deposit: float


class HouseData(BaseModel):
    value: float
    debt: float
    remaining_tenure: int


class HouseholdData(BaseModel):
    age: int
    salary: float
    pension_contribution: Optional[float] = None
    pension_initial_value: Optional[float] = None
    spouse_age: Optional[int] = None
    spouse_salary: Optional[float] = None
    spouse_pension_contribution: Optional[float] = None
    spouse_pension_initial_value: Optional[float] = None
    houses: Optional[List[HouseData]] = None
    savings: Optional[List[SavingsData]] = None


def _build_spouse(household: HouseholdData):
    if household.spouse_age:
        return build_person(household.spouse_age)
    return None


def _build_incomes(household: HouseholdData):
    spouse_salary = household.spouse_salary if household.spouse_salary else None
    return build_incomes(household.salary, spouse_salary)


def _build_policies(household: HouseholdData):
    if not household.pension_contribution:
        return None
    spouse_contrib = household.spouse_pension_contribution or 0
    spouse_init = household.spouse_pension_initial_value or 0
    return build_policies(
        household.pension_contribution,
        household.pension_initial_value,
        spouse_contrib,
        spouse_init,
    )


def _build_houses(household: HouseholdData):
    return build_houses(household.houses) if household.houses else None


def _build_liquid_assets(household: HouseholdData):
    return build_liquid_assets(household.savings) if household.savings else None


@function_tool
async def call_calculation_api(household: HouseholdData) -> str:
    """Call Calculate Target Prices endpoint of Calculation API with given user data."""
    try:
        payload = {
            "primary": build_person(household.age),
            "spouse": _build_spouse(household),
            "incomes": _build_incomes(household),
            "policies": _build_policies(household),
            "houses": _build_houses(household),
            "liquidAssets": _build_liquid_assets(household),
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        print("Payload for Calculation API:", json.dumps(payload, indent=2))
        return client.calculate_target_prices(payload)
    except Exception as e:
        print("Error during calculation API call:", str(e))
        return f"An error occurred while processing your request: {e}"


@function_tool
async def call_rag(query: str) -> str:
    pipeline = rag.get_pipeline()
    result = pipeline.run(
        data={
            "retriever": {"query": query},
            "ranker": {"query": query},
            "prompt_builder": {"question": query},
        },
        include_outputs_from={"retriever", "generator"},
    )
    print("rag result:", result["generator"]["replies"][0])
    return result["generator"]["replies"][0]
