DATA_PATH = "data/loan_data.csv"

MODEL_PATH = "models/tuned_gradient_boosting.pkl"
FEATURE_IMPORTANCE_PATH = "models/feature_importance.csv"
ROC_CURVE_PATH = "models/roc_curve.png"
FEATURE_IMPORTANCE_PLOT_PATH = "models/feature_importance.png"

TARGET_COLUMN = "loan_status"

COLUMN_RENAME_MAP = {
    "laufkont": "checking_account",
    "laufzeit": "loan_duration_months",
    "moral": "credit_history",
    "verw": "loan_purpose",
    "hoehe": "loan_amount",
    "sparkont": "savings_account",
    "beszeit": "employment_years",
    "rate": "installment_rate_percent",
    "famges": "personal_status",
    "buerge": "guarantors",
    "wohnzeit": "years_at_residence",
    "verm": "property_assets",
    "alter": "age",
    "weitkred": "other_installment_plans",
    "wohn": "housing_type",
    "bishkred": "existing_credit_count",
    "beruf": "job",
    "pers": "dependents",
    "telef": "telephone_available",
    "gastarb": "foreign_worker",
    "kredit": "loan_status",
}

DISPLAY_NAME_MAP = {
    "checking_account": "Checking Account Status",
    "loan_duration_months": "Loan Duration",
    "credit_history": "Credit History",
    "loan_purpose": "Loan Purpose",
    "loan_amount": "Loan Amount",
    "savings_account": "Savings Account",
    "employment_years": "Employment Duration",
    "installment_rate_percent": "Installment Rate",
    "personal_status": "Personal Status",
    "guarantors": "Guarantor Status",
    "years_at_residence": "Years at Residence",
    "property_assets": "Property / Assets",
    "age": "Age",
    "other_installment_plans": "Other Installment Plans",
    "housing_type": "Housing Type",
    "existing_credit_count": "Existing Credit Count",
    "job": "Job Type",
    "dependents": "Dependents",
    "telephone_available": "Telephone Available",
    "foreign_worker": "Foreign Worker",
}

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "gemma3"