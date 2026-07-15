from src.explanation_mapping import build_readable_application


def build_loan_officer_summary(
    application: dict,
    prediction: dict,
) -> dict:
    readable = build_readable_application(application)

    return {
        "model_decision": prediction["decision"],
        "approval_probability": prediction["approval_probability"],
        "risk_probability": prediction["risk_probability"],
        "risk_level": prediction["risk_level"],
        "confidence": prediction["confidence"],
        "requested_loan_amount": application["loan_amount"],
        "requested_duration_months": application["loan_duration_months"],
        "loan_purpose": readable["loan_purpose"],
        "checking_account": readable["checking_account"],
        "savings_account": readable["savings_account"],
        "credit_history": readable["credit_history"],
        "employment_duration": readable["employment_duration"],
        "existing_credits": readable["existing_credits"],
        "housing": readable["housing"],
        "property": readable["property"],
        "job": readable["job"],
    }