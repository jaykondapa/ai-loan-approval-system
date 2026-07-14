import json
import time
import joblib
import pandas as pd

from src.config import MODEL_PATH


MODEL = joblib.load(MODEL_PATH)


def load_model_metadata():
    with open("models/model_metadata.json", "r") as file:
        return json.load(file)


def get_risk_level(risk_probability: float):
    if risk_probability < 0.3:
        return "Low"
    elif risk_probability < 0.6:
        return "Medium"
    return "High"


def get_confidence(approval_probability: float, risk_probability: float):
    highest_probability = max(approval_probability, risk_probability)

    if highest_probability >= 0.8:
        return "High"
    elif highest_probability >= 0.6:
        return "Medium"
    return "Low"


def predict_loan(application_data: dict):
    start_time = time.time()

    input_df = pd.DataFrame([application_data])

    prediction = int(MODEL.predict(input_df)[0])
    probabilities = MODEL.predict_proba(input_df)[0]

    risk_probability = round(float(probabilities[0]), 4)
    approval_probability = round(float(probabilities[1]), 4)

    decision = "Approved" if prediction == 1 else "Rejected"

    metadata = load_model_metadata()
    prediction_time_ms = round((time.time() - start_time) * 1000, 2)

    return {
        "prediction": prediction,
        "decision": decision,
        "approval_probability": approval_probability,
        "risk_probability": risk_probability,
        "risk_level": get_risk_level(risk_probability),
        "confidence": get_confidence(approval_probability, risk_probability),
        "model_name": metadata["model_name"],
        "prediction_time_ms": prediction_time_ms,
    }