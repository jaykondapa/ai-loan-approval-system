from typing import Optional

from pydantic import BaseModel, Field


class LoanApplication(BaseModel):
    checking_account: int = Field(3, ge=1, le=4)
    loan_duration_months: int = Field(
    default=24,
    ge=4,
    le=72,
    description="Loan duration supported by the model: 4–72 months",
    ) #to match the trained data range
    credit_history: int = Field(3, ge=0, le=4)
    loan_purpose: int = Field(2, ge=0, le=10)
    loan_amount: int = Field(
    default=5000,
    ge=250,
    le=18424,
    description="Loan amount supported by the model: 250–18,424 DM",
    ) #to match the trained data range
    savings_account: int = Field(3, ge=1, le=5)
    employment_years: int = Field(3, ge=1, le=5)
    installment_rate_percent: int = Field(3, ge=1, le=4)
    personal_status: int = Field(3, ge=1, le=4)
    guarantors: int = Field(1, ge=1, le=3)
    years_at_residence: int = Field(3, ge=1, le=4)
    property_assets: int = Field(4, ge=1, le=4)
    age: int = Field(35, ge=18, le=100)
    other_installment_plans: int = Field(3, ge=1, le=3)
    housing_type: int = Field(3, ge=1, le=3)
    existing_credit_count: int = Field(1, ge=1, le=4)
    job: int = Field(3, ge=1, le=4)
    dependents: int = Field(2, ge=1, le=2)
    telephone_available: int = Field(2, ge=1, le=2)
    foreign_worker: int = Field(1, ge=1, le=2)

class LoanOfficerSummary(BaseModel):
    model_decision: str
    approval_probability: float
    risk_probability: float
    risk_level: str
    confidence: str

    requested_loan_amount: int
    requested_duration_months: int

    loan_purpose: str
    checking_account: str
    savings_account: str
    credit_history: str
    employment_duration: str
    existing_credits: str
    housing: str
    property: str
    job: str


class AIExplanation(BaseModel):
    customer_message: str
    loan_officer_summary: LoanOfficerSummary


class PredictionResponse(BaseModel):
    prediction: int
    decision: str
    approval_probability: float
    risk_probability: float
    risk_level: str
    confidence: str

    model_name: str
    prediction_time_ms: float

    ai_explanation: Optional[AIExplanation] = None
