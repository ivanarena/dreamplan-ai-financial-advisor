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
from rag import rag


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


@function_tool
async def call_calculation_api(household: HouseholdData) -> str:
    """Call Calculate Target Prices endpoint of Calculation API with given user data."""
    try:
        payload = {
            "primary": build_person(household.age),
            "spouse": build_person(household.spouse_age)
            if household.spouse_age is not None
            else None,
            "incomes": build_incomes(
                household.salary,
                household.spouse_salary
                if household.spouse_salary is not None
                else None,
            ),
            "policies": build_policies(
                household.pension_contribution,
                household.pension_initial_value,
                household.spouse_pension_contribution
                if household.spouse_pension_contribution
                else 0,
                household.spouse_pension_initial_value
                if household.spouse_pension_initial_value
                else 0,
            ),
            "houses": build_houses(household.houses),
            "liquidAssets": build_liquid_assets(household.savings),
        }
        return client.calculate_target_prices(payload)

    except Exception as e:
        print("Error during calculation API call:", str(e))
        return f"An error occurred while processing your request: {e}"


@function_tool
async def call_rag(query: str) -> str:
    result = rag.run(
        data={"retriever": {"query": query}, "prompt_builder": {"question": query}}
    )
    return result["generator"]["replies"][0]
