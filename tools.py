from calculation.client import client
from agents import function_tool
from calculation.factories import build_person, build_incomes, build_policies
from pydantic import BaseModel
from typing import Optional


class UserData(BaseModel):
    age: int
    salary: float
    pension_contribution: Optional[float] = None
    pension_initial_value: Optional[float] = None
    spouse_age: Optional[int] = None
    spouse_salary: Optional[float] = None
    spouse_pension_contribution: Optional[float] = None
    spouse_pension_initial_value: Optional[float] = None


@function_tool
async def call_calculation_api(user_data: UserData) -> str:
    """Call Calculate Target Prices endpoint of Calculation API with given user data."""
    try:
        print("\n====== USER DATA ======\n", user_data)

        payload = {
            "primary": build_person(user_data.age),
            "spouse": build_person(user_data.spouse_age)
            if user_data.spouse_age is not None
            else None,
            "incomes": build_incomes(
                user_data.salary,
                user_data.spouse_salary
                if user_data.spouse_salary is not None
                else None,
            ),
            "policies": build_policies(
                user_data.pension_contribution,
                user_data.pension_initial_value,
                user_data.spouse_pension_contribution
                if user_data.spouse_pension_contribution
                else 0,
                user_data.spouse_pension_initial_value
                if user_data.spouse_pension_initial_value
                else 0,
            ),
        }

        print("\n====== PAYLOAD ======\n", payload)

        return client.calculate_target_prices(payload)

    except Exception as e:
        print("Error during calculation API call:", str(e))
        return f"An error occurred while processing your request: {e}"
