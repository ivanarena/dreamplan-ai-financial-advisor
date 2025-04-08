import pytest
from calculation.client import CalculationApiClient
import os
import dotenv
dotenv.load_dotenv()

@pytest.fixture
def api():
    """Fixture to create a test client with a mock base URL"""
    return CalculationApiClient(base_url=os.getenv("CALCULATION_API_URL"))


@pytest.fixture
def payload():
    """Fixture to provide a valid calculation payload"""
    return {
    "primary": {"birthYear": 1967, "pensionAge": 68, "deathAge": 88},
    "spouse": {"birthYear": 1969, "pensionAge": 68, "deathAge": 88},
    "housesWithLoans": [
        {
            "type": "HouseWithLoans",
            "houseValue": 3500000,
            "houseGrowth": [
                {
                    "percentage": 0.048,
                    "entryDate": {
                        "year": 2023,
                        "month": 1,
                        "convention": "BeginningOf",
                    },
                },
                {
                    "percentage": 0.045,
                    "entryDate": {
                        "year": 2028,
                        "month": 1,
                        "convention": "BeginningOf",
                    },
                },
                {
                    "percentage": 0.046,
                    "entryDate": {
                        "year": 2033,
                        "month": 1,
                        "convention": "BeginningOf",
                    },
                },
            ],
            "loans": [
                {
                    "type": "AmortizedLoan",
                    "remainingPrincipal": 2500000,
                    "remainingTenure": 25,
                    "remainingRepaymentFreeYears": 0,
                    "interestRate": 0.01,
                    "contributionFeeRate": 0.005,
                    "redemptionDetails": {"redemptionFee": 30000, "bondPrice": 70},
                    "id": "ltvccqj81olcrejm",
                }
            ],
            "id": "lk0yhlz86hz9kik5",
        }
    ],
    "incomes": [
        {
            "owner": "Primary",
            "payment": {
                "type": "Payment",
                "amount": 48000,
                "to": None,
                "paymentFrequency": "Monthly",
            },
            "expectedGrowth": None,
            "id": "wgpc47kdl6lcyfkv",
        },
        {
            "owner": "Spouse",
            "payment": {
                "type": "Payment",
                "amount": 33583.3333333333,
                "to": None,
                "paymentFrequency": "Monthly",
            },
            "expectedGrowth": None,
            "id": "urwhbye3e9juecz3",
        },
    ],
    "liquidAssets": [
        {
            "assetType": "Cash",
            "initialValue": 50000,
            "monthlyDeposit": {
                "type": "Payment",
                "amount": 1000,
                "to": None,
                "paymentFrequency": "Monthly",
            },
            "recurringFees": None,
            "expectedReturn": None,
            "id": "kefnmlv9oud6q29l",
        },
        {
            "assetType": "Stocks",
            "initialValue": 50000,
            "monthlyDeposit": {
                "type": "Payment",
                "amount": 5000,
                "to": None,
                "paymentFrequency": "Monthly",
            },
            "recurringFees": None,
            "expectedReturn": [
                {
                    "percentage": 0.05,
                    "entryDate": {
                        "year": 2023,
                        "month": 1,
                        "convention": "BeginningOf",
                    },
                },
                {
                    "percentage": 0.045,
                    "entryDate": {
                        "year": 2028,
                        "month": 1,
                        "convention": "BeginningOf",
                    },
                },
                {
                    "percentage": 0.047,
                    "entryDate": {
                        "year": 2033,
                        "month": 1,
                        "convention": "BeginningOf",
                    },
                },
            ],
            "id": "b10jb2odt99tru5f",
        },
    ],
    "companies": [
        {
            "type": "IncorporatedCompany",
            "dividends": 30000,
            "yearlyEbitda": 100000,
            "initialEquity": 100000,
            "expectedReturn": [
                {
                    "percentage": 0.05,
                    "entryDate": {
                        "year": 2023,
                        "month": 1,
                        "convention": "BeginningOf",
                    },
                },
                {
                    "percentage": 0.045,
                    "entryDate": {
                        "year": 2028,
                        "month": 1,
                        "convention": "BeginningOf",
                    },
                },
                {
                    "percentage": 0.047,
                    "entryDate": {
                        "year": 2033,
                        "month": 1,
                        "convention": "BeginningOf",
                    },
                },
            ],
            "id": "jjybqf0np7f2igbe",
        }
    ],
    "policies": [
        {
            "owner": "Primary",
            "coverages": [
                {
                    "type": "PensionCoverage",
                    "contribution": {
                        "type": "PensionContribution",
                        "extraVoluntaryContribution": 0,
                        "contributionToInsuranceFraction": 0,
                        "isFromEmployer": True,
                        "isInclusiveAmb": False,
                        "amount": 4800,
                        "to": None,
                        "paymentFrequency": "Monthly",
                    },
                    "initialValue": 652000,
                    "payOutType": {
                        "type": "Annuity",
                        "payOutEndDate": None,
                        "payOutDate": None,
                    },
                    "taxCode": "Two",
                    "predefinedBenefits": None,
                    "expectedReturn": [
                        {
                            "percentage": 0.05,
                            "entryDate": {
                                "year": 2023,
                                "month": 1,
                                "convention": "BeginningOf",
                            },
                        },
                        {
                            "percentage": 0.045,
                            "entryDate": {
                                "year": 2028,
                                "month": 1,
                                "convention": "BeginningOf",
                            },
                        },
                        {
                            "percentage": 0.047,
                            "entryDate": {
                                "year": 2033,
                                "month": 1,
                                "convention": "BeginningOf",
                            },
                        },
                    ],
                    "assetUnderManagementFee": [
                        {
                            "percentage": 0.01,
                            "entryDate": {
                                "year": 2024,
                                "month": 1,
                                "convention": "BeginningOf",
                            },
                        }
                    ],
                    "owner": "Primary",
                    "id": "xd0oo4gia92934sa",
                },
                {
                    "type": "RiskCoverage",
                    "contribution": {
                        "type": "RiskCoverageContribution",
                        "isFromEmployer": True,
                        "isInclusiveAmb": False,
                        "amount": 300,
                        "to": None,
                        "paymentFrequency": "Monthly",
                    },
                    "payOut": {"amount": 500000, "payoutReceiver": None},
                    "riskCoverageInformation": {
                        "type": "UkRiskCoverageInformation",
                        "coverageType": "LumpSumAtDeath",
                    },
                    "owner": "Primary",
                    "id": "ggxwz9iigfrvezue",
                },
            ],
            "id": "fxhf79vgfh1btru0",
        },
        {
            "owner": "Spouse",
            "coverages": [
                {
                    "type": "PensionCoverage",
                    "contribution": {
                        "type": "PensionContribution",
                        "extraVoluntaryContribution": 0,
                        "contributionToInsuranceFraction": 0,
                        "isFromEmployer": True,
                        "isInclusiveAmb": False,
                        "amount": 4030,
                        "to": None,
                        "paymentFrequency": "Monthly",
                    },
                    "initialValue": 693000,
                    "payOutType": {"type": "LifeAnnuity", "payOutDate": None},
                    "taxCode": "One",
                    "predefinedBenefits": [
                        {
                            "amount": 70000,
                            "entryDate": {
                                "year": 2038,
                                "month": 1,
                                "convention": "BeginningOf",
                            },
                        }
                    ],
                    "expectedReturn": None,
                    "assetUnderManagementFee": None,
                    "owner": "Spouse",
                    "id": "t536p1ximuxw8ylb",
                }
            ],
            "id": "vl61t5ov3e6h03tc",
        },
    ],
    "recommendationSettings": {
        "primaryPensionRecommendation": {
            "type": "PensionCoverageRatioGoalSeek",
            "ratio": 0.75,
            "recommendationProduct": {
                "type": "SpecifiedPolicyRecommendationProduct",
                "recommendationCoverage": {
                    "type": "PensionCoverage",
                    "contribution": {
                        "type": "PensionContribution",
                        "extraVoluntaryContribution": 0,
                        "contributionToInsuranceFraction": 0,
                        "isFromEmployer": True,
                        "isInclusiveAmb": False,
                        "amount": 2000,
                        "to": None,
                        "paymentFrequency": "Monthly",
                    },
                    "initialValue": 0,
                    "payOutType": {"type": "LifeAnnuity", "payOutDate": None},
                    "taxCode": "One",
                    "predefinedBenefits": None,
                    "expectedReturn": [
                        {
                            "percentage": 0.06,
                            "entryDate": {
                                "year": 2023,
                                "month": 1,
                                "convention": "BeginningOf",
                            },
                        }
                    ],
                    "assetUnderManagementFee": [
                        {
                            "percentage": 0.01,
                            "entryDate": {
                                "year": 2024,
                                "month": 1,
                                "convention": "BeginningOf",
                            },
                        }
                    ],
                    "owner": "Primary",
                    "id": "jbnqhl0cw0q4m3dq",
                },
                "disabilityRecommendationCoverages": None,
                "deathRecommendationCoverages": None,
                "fixedCoverages": [
                    {
                        "type": "RiskCoverage",
                        "contribution": {
                            "type": "RiskCoverageContribution",
                            "isFromEmployer": True,
                            "isInclusiveAmb": False,
                            "amount": 500,
                            "to": None,
                            "paymentFrequency": "Monthly",
                        },
                        "payOut": {"amount": 500000, "payoutReceiver": None},
                        "riskCoverageInformation": {
                            "type": "UkRiskCoverageInformation",
                            "coverageType": "LumpSumAtDeath",
                        },
                        "owner": "Primary",
                        "id": "dz1s10mdfg834v18",
                    }
                ],
                "minimumContribution": 700,
            },
        },
        "spousePensionRecommendation": {
            "type": "AverageDisposableIncomeGoalSeek",
            "averageMonthlyDisposableIncome": 30000,
            "recommendationProduct": {
                "type": "SinglePensionRecommendationProduct",
                "idOfPensionToChange": None,
                "minimumContribution": None,
            },
        },
        "loanRecommendation": {
            "type": "RestrictedLoanToValueRatioGoalSeek",
            "ratio": 0.5,
            "establishmentDetails": {"foundationFee": 20000, "bondPrice": 95},
            "interestRate": 0.03,
            "contributionFeeRate": 0.02,
        },
        "emergencySavingRecommendation": {
            "type": "CashSavingsWithSpecifiedContribution",
            "cashSavings": 150000,
            "initialOneTimeContribution": 50000,
            "monthlyContribution": 1000,
            "recommendationProduct": None,
        },
        "companyRecommendation": {"type": "NoCompanyRecommendation"},
    },
    "dreams": [
        {"date": {"year": 2024, "month": 12, "convention": "EndOf"}, "cost": 1000}
    ],
    "municipalityId": "165",
    "calculationStart": {"year": 2025, "month": 1, "convention": "BeginningOf"},
    "calculationCountry": "Uk",
    "outputConfiguration": {
        "includeStatementInOutput": True,
        "roundingPrecision": 2,
        "accountTypesFilter": [],
        "includeRecommendation": True,
    },
}
