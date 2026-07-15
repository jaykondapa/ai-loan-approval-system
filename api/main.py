from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.llm_service import LLMServiceError, generate_decision_content

from src.schemas import LoanApplication, PredictionResponse
from src.predictor import predict_loan, load_model_metadata

from src.loan_officer_summary import build_loan_officer_summary



app = FastAPI(
    title="AI Loan Approval API",
    description="FastAPI backend for loan approval risk prediction using a tuned Gradient Boosting model.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "AI Loan Approval API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/model-info")
def model_info():
    return load_model_metadata()


@app.post("/predict", response_model=PredictionResponse)
def predict(application: LoanApplication):
    application_data = application.model_dump()
    return predict_loan(application_data)

@app.post( "/predict-with-explanation", response_model=PredictionResponse)
def predict_with_explanation(application: LoanApplication):
    application_data = application.model_dump()

    prediction = predict_loan(application_data)

    try:
        generated_content = generate_decision_content(
            application=application_data,
            prediction=prediction,
        )
    except LLMServiceError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    loan_officer_summary = build_loan_officer_summary(
        application=application_data,
        prediction=prediction,
    )

    return {
        **prediction,
        "ai_explanation": {
            "customer_message": generated_content["customer_message"],
            "loan_officer_summary": loan_officer_summary,
        },
    }