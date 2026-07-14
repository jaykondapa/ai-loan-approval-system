from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.schemas import LoanApplication, PredictionResponse
from src.predictor import predict_loan, load_model_metadata



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