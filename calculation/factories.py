from calculation.templates import PersonInput, Income
import uuid
from typing import List


def build_person(age: int) -> PersonInput:
    return {"birthYear": 2025 - age, "pensionAge": 68, "deathAge": 88}


def build_incomes(salary: float, spouse_salary: float) -> List[Income]:
    incomes = [
        {
            "owner": "Primary",
            "payment": {
                "type": "Payment",
                "amount": salary,
                "paymentFrequency": "Monthly",
            },
            "id": str(uuid.uuid4()),
        }
    ]
    if spouse_salary:
        incomes.append(
            {
                "owner": "Spouse",
                "payment": {
                    "type": "Payment",
                    "amount": spouse_salary,
                    "paymentFrequency": "Monthly",
                },
                "id": str(uuid.uuid4()),
            }
        )
    return incomes
