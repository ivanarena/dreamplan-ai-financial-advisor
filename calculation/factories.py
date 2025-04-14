from calculation.templates import PersonInput, Income, PensionCoverage
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
                },
                "id": str(uuid.uuid4()),
            }
        )
    return incomes


def build_policies(
    contribution: float,
    initial_value: float,
    spouse_contribution: float,
    spouse_initial_value: float,
) -> List[PensionCoverage]:
    policies = [
        {
            "type": "PensionPolicy",
            "owner": "Primary",
            "coverages": [
                {
                    "type": "PensionCoverage",
                    "owner": "Primary",
                    "contribution": {
                        "type": "PensionContribution",
                        "amount": contribution,
                    },
                    "initialValue": initial_value,
                    "id": str(uuid.uuid4()),
                },
            ],
            "id": str(uuid.uuid4()),
        }
    ]
    if spouse_contribution:
        policies.append(
            {
                "type": "PensionPolicy",
                "owner": "Spouse",
                "coverages": [
                    {
                        "type": "PensionCoverage",
                        "owner": "Spouse",
                        "contribution": {
                            "type": "PensionContribution",
                            "amount": spouse_contribution,
                        },
                        "initialValue": spouse_initial_value,
                        "id": str(uuid.uuid4()),
                    },
                ],
                "id": str(uuid.uuid4()),
            }
        )
    return policies
