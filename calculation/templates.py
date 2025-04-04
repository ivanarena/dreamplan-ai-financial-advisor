from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel


class EntityBase(BaseModel):
    id: str


class DateConvention(str, Enum):
    BeginningOf = "BeginningOf"
    EndOf = "EndOf"


class AccountType(str, Enum):
    Salary = "Salary"
    Dreams = "Dreams"
    CompanyEquityGross = "CompanyEquityGross"
    CompanyEquityNet = "CompanyEquityNet"
    CompanyDividendGross = "CompanyDividendGross"
    CompanyDividendNet = "CompanyDividendNet"
    CompanyTopTax = "CompanyTopTax"
    EmergencySavings = "EmergencySavings"
    EmergencySavingsDeposit = "EmergencySavingsDeposit"
    LiquidityAccount = "LiquidityAccount"
    HouseValue = "HouseValue"
    HouseEquity = "HouseEquity"
    LoanPrincipal = "LoanPrincipal"
    LoanInterest = "LoanInterest"
    LoanRepayment = "LoanRepayment"
    LoanFees = "LoanFees"
    LoanInstallmentGross = "LoanInstallmentGross"
    LoanInstallmentNet = "LoanInstallmentNet"
    PensionContributionGross = "PensionContributionGross"
    PensionContributionNet = "PensionContributionNet"
    PensionDepotGross = "PensionDepotGross"
    PensionDepotNet = "PensionDepotNet"
    PensionPayout = "PensionPayout"
    PensionPayoutAtDeath = "PensionPayoutAtDeath"
    PensionCost = "PensionCost"
    RiskCoverageContributionGross = "RiskCoverageContributionGross"
    RiskCoverageContributionNet = "RiskCoverageContributionNet"
    RiskCoveragePayout = "RiskCoveragePayout"
    RiskCoveragePayoutToChildren = "RiskCoveragePayoutToChildren"
    InsuranceSumTax = "InsuranceSumTax"
    TaxableIncome = "TaxableIncome"
    TopTaxTaxationBase = "TopTaxTaxationBase"
    TotalIncome = "TotalIncome"
    TotalTax = "TotalTax"
    DisposableIncome = "DisposableIncome"
    ChangeInSavingsNet = "ChangeInSavingsNet"
    UkBasicRateTax = "UkBasicRateTax"
    UkHigherRateTax = "UkHigherRateTax"
    UkAdditionalRateTax = "UkAdditionalRateTax"
    DkAmbTax = "DkAmbTax"
    DkBottomTax = "DkBottomTax"
    DkTopTax = "DkTopTax"
    DkMunicipalityTax = "DkMunicipalityTax"
    DkStatePensionPayout = "DkStatePensionPayout"


class AssetType(str, Enum):
    Cash = "Cash"
    Stocks = "Stocks"
    Bonds = "Bonds"


class CalculationCountry(str, Enum):
    Dk = "Dk"
    Uk = "Uk"
    DkInHouse = "DkInHouse"


class Owner(str, Enum):
    Primary = "Primary"
    Spouse = "Spouse"


class PaymentFrequency(str, Enum):
    Yearly = "Yearly"
    Monthly = "Monthly"


class PersonType(str, Enum):
    Primary = "Primary"
    Spouse = "Spouse"
    Shared = "Shared"


class Scenario(str, Enum):
    Baseline = "Baseline"
    Recommendation = "Recommendation"


class HealthStatus(str, Enum):
    Unhealthy = "Unhealthy"
    Degraded = "Degraded"
    Healthy = "Healthy"


class MessageCode(str, Enum):
    TargetCoverageRatioIsTooLowBasedOnBaselineCoverageRatio = (
        "TargetCoverageRatioIsTooLowBasedOnBaselineCoverageRatio"
    )
    TargetDisposableIncomeIsTooLowBasedOnBaselineDisposableIncome = (
        "TargetDisposableIncomeIsTooLowBasedOnBaselineDisposableIncome"
    )
    LiquiditySavingsDepotHasNegativePeriods = "LiquiditySavingsDepotHasNegativePeriods"
    LiquiditySavingsDepotIsNegativeAtRetirement = (
        "LiquiditySavingsDepotIsNegativeAtRetirement"
    )
    TargetResultsInAnAverageRetirementMuchHigherThanTheFirstYearDisposableIncome = (
        "TargetResultsInAnAverageRetirementMuchHigherThanTheFirstYearDisposableIncome"
    )


class AbsoluteMonth(BaseModel):
    year: int
    month: int = 12
    convention: "DateConvention" = "EndOf"


class EntryBase(BaseModel):
    entryDate: AbsoluteMonth


class PercentageEntry(EntryBase):
    percentage: float


class AmountEntry(EntryBase):
    amount: float


class Key(BaseModel):
    personType: PersonType
    accountType: AccountType
    inputId: Optional[str] = None


class Account(BaseModel):
    key: Optional[Key] = None
    entries: Optional[List[AmountEntry]] = []
    subAccountKeys: Optional[List[Key]] = []


class Statement(BaseModel):
    accounts: Optional[List[Account]] = []


class StatementResponse(BaseModel):
    baseline: Optional[Statement] = None
    recommendation: Optional[Statement] = None
    delta: Optional[Statement] = None


class PersonInput(BaseModel):
    birthYear: int
    pensionAge: int
    deathAge: int = 88


class PaymentBase(BaseModel):
    type: str
    amount: float
    to: Optional[AbsoluteMonth] = None
    paymentFrequency: "PaymentFrequency" = "Monthly"


class Payment(PaymentBase):
    pass


class Contribution(PaymentBase):
    isFromEmployer: bool = True
    isInclusiveAmb: Optional[bool] = False


class RiskCoverageContribution(Contribution):
    pass


class PensionContribution(Contribution):
    extraVoluntaryContribution: float = 0
    contributionToInsuranceFraction: float = 0


class PayOutType(BaseModel):
    type: str
    payOutDate: Optional[AbsoluteMonth] = None


class Annuity(PayOutType):
    payOutEndDate: Optional[AbsoluteMonth] = None


class LifeAnnuity(PayOutType):
    pass


class LumpSum(PayOutType):
    pass


class RiskCoverageInformation(BaseModel):
    type: str


class DkRiskCoverageType(str, Enum):
    AnnuityAtDeath = "AnnuityAtDeath"
    LumpSumAtDeathTaxCode2 = "LumpSumAtDeathTaxCode2"
    LumpSumAtDeathTaxCode5 = "LumpSumAtDeathTaxCode5"
    LumpSumAtDisabilityTaxCode2 = "LumpSumAtDisabilityTaxCode2"
    LumpSumAtDisabilityTaxCode5 = "LumpSumAtDisabilityTaxCode5"
    AnnuityAtDisability = "AnnuityAtDisability"
    CriticalIllness = "CriticalIllness"
    AccidentInsuranceAtDeath = "AccidentInsuranceAtDeath"
    LumpSumAtDeathToChildrenTaxCode5 = "LumpSumAtDeathToChildrenTaxCode5"


class DkRiskCoverageInformation(RiskCoverageInformation):
    coverageType: DkRiskCoverageType = DkRiskCoverageType.LumpSumAtDeathTaxCode5


class UkRiskCoverageType(str, Enum):
    LumpSumAtDeath = "LumpSumAtDeath"
    AnnuityAtDeath = "AnnuityAtDeath"
    LumpSumAtDisability = "LumpSumAtDisability"
    AnnuityAtDisability = "AnnuityAtDisability"
    CriticalIllness = "CriticalIllness"
    AccidentInsuranceAtDeath = "AccidentInsuranceAtDeath"


class UkRiskCoverageInformation(RiskCoverageInformation):
    coverageType: UkRiskCoverageType = UkRiskCoverageType.LumpSumAtDeath


class DkTaxCode(str, Enum):
    One = "One"
    Two = "Two"
    Three = "Three"
    Five = "Five"
    Seven = "Seven"
    Nine = "Nine"
    ThirtyThree = "ThirtyThree"


class PayoutReceiver(str, Enum):
    Self = "Self"
    Spouse = "Spouse"
    Children = "Children"
    Other = "Other"


class RiskCoveragePayOut(BaseModel):
    amount: float
    payoutReceiver: Optional[PayoutReceiver] = None


class Coverage(EntityBase):
    type: str
    owner: Owner


class RiskCoverage(Coverage):
    contribution: Optional[RiskCoverageContribution] = None
    payOut: Optional[RiskCoveragePayOut] = None
    riskCoverageInformation: Optional[
        Union[DkRiskCoverageInformation, UkRiskCoverageInformation]
    ] = None


class PensionCoverage(Coverage):
    contribution: Optional[PensionContribution] = None
    initialValue: Optional[float] = None
    payOutType: Optional[Union[Annuity, LifeAnnuity, LumpSum]] = None
    taxCode: DkTaxCode = DkTaxCode.One
    predefinedBenefits: Optional[List[AmountEntry]] = None
    expectedReturn: Optional[List[PercentageEntry]] = None
    assetUnderManagementFee: Optional[List[PercentageEntry]] = None


class Policy(EntityBase):
    owner: Owner
    coverages: Optional[List[Union[RiskCoverage, PensionCoverage]]] = None


class Income(EntityBase):
    owner: Owner
    payment: Payment
    expectedGrowth: Optional[List[PercentageEntry]] = None


class RedemptionDetails(BaseModel):
    redemptionFee: float
    bondPrice: Optional[float] = None


class LoanBase(EntityBase):
    type: str
    redemptionDetails: Optional[RedemptionDetails] = None


class AmortizedLoan(LoanBase):
    remainingPrincipal: float
    remainingTenure: int = 30
    remainingRepaymentFreeYears: int = 0
    interestRate: float = 0.03
    contributionFeeRate: float = 0


class HouseBase(EntityBase):
    type: str
    loans: Optional[List[AmortizedLoan]] = None


class HouseWithLoans(HouseBase):
    houseValue: float
    houseGrowth: Optional[List[PercentageEntry]] = None


class LiquidAsset(EntityBase):
    assetType: AssetType
    initialValue: float
    monthlyDeposit: Optional[Payment] = None
    expectedReturn: Optional[List[PercentageEntry]] = None
    recurringFees: Optional[List[PercentageEntry]] = None


class CompanyBase(EntityBase):
    type: str
    yearlyEbitda: float
    initialEquity: Optional[float] = None
    expectedReturn: Optional[List[PercentageEntry]] = None


class IncorporatedCompany(CompanyBase):
    dividends: float


class PersonalCompany(CompanyBase):
    pass


class Dream(BaseModel):
    date: Optional[AbsoluteMonth] = None
    cost: float = 0


class OutputConfiguration(BaseModel):
    includeStatementInOutput: bool = True
    roundingPrecision: int = 0
    accountTypesFilter: Optional[List[AccountType]] = None
    includeRecommendation: bool = True


class BaseRecommendation(BaseModel):
    type: str


class PensionRecommendationProduct(BaseModel):
    """Base class for pension recommendation products."""
    type: str
    minimumContribution: Optional[float] = None


class SinglePensionRecommendationProduct(PensionRecommendationProduct):
    """A recommendation product that modifies a single pension coverage."""
    type: str = "SinglePensionRecommendationProduct"
    idOfPensionToChange: Optional[str] = None


class PriceRule(BaseModel):
    """Base class for price rules."""
    type: str


class PriceStep(BaseModel):
    """A single price/benefit step for the PriceStepRule."""

    price: float
    benefit: float
    id: Optional[str] = None


class PriceRange(PriceRule):
    """Price rule based on a price per 1000 benefit calculation."""

    pricePer1000Benefit: float
    minimumContribution: float = 0
    maximumContribution: Optional[float] = None
    type: str = "PriceRange"


class PriceStepRule(PriceRule):
    """Price rule based on discrete steps of price and benefit."""

    steps: List[PriceStep]
    defaultPriceStepId: Optional[str] = None
    type: str = "PriceStepRule"


class RiskCoverageWithProductInformation(RiskCoverage):
    """Risk coverage with additional product information."""

    priceRule: Optional[Union[PriceRange, PriceStepRule]] = None
    isMandatory: bool = False  # If true, this coverage will always be created


class SpecifiedPolicyRecommendationProduct(PensionRecommendationProduct):
    """A specified policy is always assumed to be a new policy with no prior contributions."""

    type: str = "SpecifiedPolicyRecommendationProduct"
    recommendationCoverage: Optional[PensionCoverage] = None
    disabilityRecommendationCoverages: Optional[
        List[RiskCoverageWithProductInformation]
    ] = None
    deathRecommendationCoverages: Optional[List[RiskCoverageWithProductInformation]] = (
        None
    )
    fixedCoverages: Optional[
        List[Union[RiskCoverage, RiskCoverageWithProductInformation, PensionCoverage]]
    ] = None


class PensionCoverageRatioGoalSeek(BaseRecommendation):
    ratio: float = 0.75
    recommendationProduct: Optional[
        Union[SinglePensionRecommendationProduct, SpecifiedPolicyRecommendationProduct]
    ] = None


class AverageDisposableIncomeGoalSeek(BaseRecommendation):
    averageMonthlyDisposableIncome: float
    recommendationProduct: Optional[
        Union[SinglePensionRecommendationProduct, SpecifiedPolicyRecommendationProduct]
    ] = None


class SimpleSpecifiedPension(BaseRecommendation):
    pension: float
    recommendationProduct: Optional[
        Union[SinglePensionRecommendationProduct, SpecifiedPolicyRecommendationProduct]
    ] = None


class SpecifiedNetVoluntaryPayment(BaseRecommendation):
    payment: float
    recommendationProduct: Optional[
        Union[SinglePensionRecommendationProduct, SpecifiedPolicyRecommendationProduct]
    ] = None


class EstablishmentDetails(BaseModel):
    """Details related to the establishment of a loan."""

    foundationFee: float
    bondPrice: Optional[float] = (
        None  # Only relevant for bond based mortgages. Otherwise, the loan proceeds is deemed equal to the loan principal baring costs.
    )


# Loan recommendation types


class LoanToValueRatioGoalSeek(BaseRecommendation):
    ratio: float
    establishmentDetails: Optional[EstablishmentDetails] = None
    interestRate: Optional[float] = None
    contributionFeeRate: Optional[float] = None


class RestrictedLoanToValueRatioGoalSeek(BaseRecommendation):
    ratio: float
    establishmentDetails: Optional[EstablishmentDetails] = None
    interestRate: Optional[float] = None
    contributionFeeRate: Optional[float] = None


class SpecifiedAmortizationLoan(BaseRecommendation):
    remainingPrincipal: float
    remainingTenure: int
    interestRate: float
    contributionFeeRate: float


# Emergency saving recommendation types


class CashSavingsWithSpecifiedContribution(BaseRecommendation):
    cashSavings: float
    initialOneTimeContribution: float
    monthlyContribution: float


class CashToSalaryRatio(BaseRecommendation):
    ratio: float = 1.25


class DefinedCashSavings(BaseRecommendation):
    cashSavings: float


# Company recommendation types
class NoCompanyRecommendation(BaseRecommendation):
    pass


class SpecifiedDividends(BaseRecommendation):
    dividends: float


class TopTaxOptimizedDividends(BaseRecommendation):
    # These duplicate product types are already defined above
    # Removing duplicate definitions that conflict with the earlier ones
    foundationFee: float
    bondPrice: float


class RecommendationSettings(BaseModel):
    primaryPensionRecommendation: Optional[
        Union[
            AverageDisposableIncomeGoalSeek,
            PensionCoverageRatioGoalSeek,
            SimpleSpecifiedPension,
            SpecifiedNetVoluntaryPayment,
        ]
    ] = None
    spousePensionRecommendation: Optional[
        Union[
            AverageDisposableIncomeGoalSeek,
            PensionCoverageRatioGoalSeek,
            SimpleSpecifiedPension,
            SpecifiedNetVoluntaryPayment,
        ]
    ] = None
    loanRecommendation: Optional[
        Union[
            LoanToValueRatioGoalSeek,
            RestrictedLoanToValueRatioGoalSeek,
            SpecifiedAmortizationLoan,
        ]
    ] = None
    emergencySavingRecommendation: Optional[
        Union[
            CashSavingsWithSpecifiedContribution, CashToSalaryRatio, DefinedCashSavings
        ]
    ] = None
    companyRecommendation: Optional[
        Union[NoCompanyRecommendation, SpecifiedDividends, TopTaxOptimizedDividends]
    ] = None


class Message(BaseModel):
    messageCode: MessageCode
    scenario: Scenario
    description: Optional[str] = None
    outputConfiguration: Optional[OutputConfiguration] = None


class PensionPayOutOverview(BaseModel):
    """Overview of pension pay-outs. All the pay-outs are gross."""

    sumPayOut: Optional[float] = None
    monthlyAnnuityPayOut: Optional[float] = None
    monthlyLifeAnnuityPayOut: Optional[float] = None


class PensionPerson(BaseModel):
    coverageRatio: float
    netPensionDepotAtPension: float
    netMonthlyPayment: float  # First year
    grossMonthlyPayment: float  # First year. Ex. AMB.
    averageMonthlyDisposableIncomeDuringRetirement: float
    pensionPayOutOverview: Optional[PensionPayOutOverview] = None


class PensionPersonDelta(BaseModel):
    netPensionDepotAtRetirementDelta: float
    grossMonthlyPaymentDelta: float
    netMonthlyPaymentDelta: float
    averageMonthlyDisposableIncomeDuringRetirementDelta: float


class PensionHouseholdOutput(BaseModel):
    primary: Optional[PensionPerson] = None
    spouse: Optional[PensionPerson] = None
    householdCoverageRatio: Optional[float] = None
    averageMonthlyDisposableIncomeDuringRetirement: float = 0
    householdPensionDepotSum: float = 0
    householdNetMonthlyPayment: float = 0
    householdGrossMonthlyPayment: float = 0


class PensionHouseholdDelta(BaseModel):
    primaryDelta: Optional[PensionPersonDelta] = None
    spouseDelta: Optional[PensionPersonDelta] = None
    householdNetPensionDepotAtRetirementDelta: float = 0
    averageMonthlyDisposableIncomeDuringRetirementDelta: float = 0
    householdNetMonthlyPaymentDelta: float = 0
    householdGrossMonthlyPaymentDelta: float = 0


class PensionBaselineAndRecommendedOutput(BaseModel):
    baseline: Optional[PensionHouseholdOutput] = None
    recommendation: Optional[PensionHouseholdOutput] = None
    householdDelta: Optional[PensionHouseholdDelta] = None


class CompanyOutput(BaseModel):
    netEquityAtRetirement: float = 0


class CompanyBaselineAndRecommendedOutput(BaseModel):
    baseline: Optional[CompanyOutput] = None
    recommendation: Optional[CompanyOutput] = None
    netCompanyEquityAtRetirementDelta: float = 0


class SavingsOutput(BaseModel):
    depotAtPension: float = 0
    averageMonthlySavings: float = 0  # positive = savings, negative = withdrawals


class SavingsBaselineAndRecommendedOutput(BaseModel):
    baseline: Optional[SavingsOutput] = None
    recommendation: Optional[SavingsOutput] = None


class EmergencySavingsOutput(BaseModel):
    cashToGrossSalaryRatio: float = 0  # Emergency savings (cash) to gross salary ratio
    depotAtPension: float = 0
    averageMonthlySavingsUntilPension: float = (
        0  # Average monthly savings (positive) or withdrawals (negative)
    )


class EmergencySavingsBaselineAndRecommendedOutput(BaseModel):
    baseline: Optional[EmergencySavingsOutput] = None
    recommendation: Optional[EmergencySavingsOutput] = None
    emergencySavingsDelta: float = 0


class HousingHeating(str, Enum):
    DistrictHeating = "districtHeating"
    Oil = "oil"
    Electricity = "electricity"
    Gas = "gas"
    Other = "other"


class RefinancingDetails(BaseModel):
    """Details about loan refinancing process."""

    totalRefinancingFees: (
        float  # Sum of all fees and expenses related to the refinancing
    )
    redemptionAmount: float  # The final redemption amount. Accounts for bond price
    finalChangeInLoanPrincipal: float  # The final change in loan principal due to refinancing fees and bond price differences


class HousingOutput(BaseModel):
    loanToValueRatioAtPension: float
    houseEquityAtPension: float
    averageMonthlyInstallmentUntilPension: float
    netAverageMonthlyInstallmentUntilPension: float


class HousingOutputAggregate(BaseModel):
    """Represents aggregate housing output values for all houses combined."""

    loanToValueRatioAtPension: float
    houseEquityAtPension: float
    averageMonthlyInstallmentUntilPension: float
    netAverageMonthlyInstallmentUntilPension: float
    houseList: Optional[List[HousingOutput]] = None


class HousingOutputAggregateRecommendation(HousingOutputAggregate):
    """Represents aggregated housing output values for recommendation, including refinancing details."""

    refinancingDetailsAggregate: Optional[RefinancingDetails] = None
    refinancingDetailsList: Optional[List[RefinancingDetails]] = None


class HousingBaselineAndRecommendedOutput(BaseModel):
    baseline: Optional[
        Union[HousingOutputAggregate, HousingOutputAggregateRecommendation]
    ] = None
    recommendation: Optional[HousingOutputAggregateRecommendation] = None
    houseEquityAtPensionDelta: float = 0
    averageMonthlyInstallmentUntilPensionDelta: float = 0
    netAverageMonthlyInstallmentUntilPensionDelta: float = 0


class OverallResultOutput(BaseModel):
    """Represents overall result output with household wealth information."""

    householdWealthAtPension: float = 0


class OverallResultBaselineAndRecommendedOutput(BaseModel):
    """Compares baseline and recommendation overall results with deltas."""

    baseline: Optional[OverallResultOutput] = None
    recommendation: Optional[OverallResultOutput] = None
    householdWealthAtPensionDelta: float = 0
    averageChangeInSavingsPrMonth: float = 0


class CalculateRequest(BaseModel):
    primary: PersonInput
    spouse: Optional[PersonInput] = None
    housesWithLoans: Optional[List[HouseWithLoans]] = None
    incomes: Optional[List[Income]] = None
    liquidAssets: Optional[List[LiquidAsset]] = None
    companies: Optional[List[Union[IncorporatedCompany, PersonalCompany]]] = None
    policies: Optional[List[Policy]] = None
    recommendationSettings: Optional[RecommendationSettings] = None
    dreams: Optional[List[Dream]] = None
    municipalityId: Optional[str] = "165"  # Default municipality id for Danish city
    calculationStart: Optional[AbsoluteMonth] = None  # Default is "2025 BoY"
    calculationCountry: CalculationCountry = CalculationCountry.Dk
    outputConfiguration: Optional[OutputConfiguration] = None


class CalculateResponse(BaseModel):
    """The different outputs from the calculators can be null, if that calculation does not apply to the input data."""
    messages: Optional[List[Message]] = None
    statements: Optional[StatementResponse] = None
    houseAndMortgageOutput: Optional[HousingBaselineAndRecommendedOutput] = None
    emergencySavingsOutput: Optional[EmergencySavingsBaselineAndRecommendedOutput] = (
        None
    )
    pensionOutput: Optional[PensionBaselineAndRecommendedOutput] = None
    companyOutput: Optional[CompanyBaselineAndRecommendedOutput] = None
    liquidSavingsOutput: Optional[SavingsBaselineAndRecommendedOutput] = None
    overallResultOutput: Optional[OverallResultBaselineAndRecommendedOutput] = None
