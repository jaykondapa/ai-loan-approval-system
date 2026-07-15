import json

import requests

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from src.prompt_templates import SYSTEM_PROMPT, build_decision_prompt

from src.explanation_mapping import build_readable_application
from src.rag_service import (
    RAGServiceError,
    retrieve_communication_policies,
)


class LLMServiceError(RuntimeError):
    """Raised when the local LLM service cannot generate a valid response."""


def generate_decision_content(
    application: dict,
    prediction: dict,
) -> dict:
    readable_application = build_readable_application(
    application
    )

    try:
        retrieval_result = retrieve_communication_policies(
            model_decision=prediction["decision"],
            loan_purpose=readable_application["loan_purpose"],
            top_k=3,
        )
        retrieved_policies = retrieval_result["policies"]
    except RAGServiceError as exc:
        raise LLMServiceError(
            "Unable to retrieve customer communication policies."
        ) from exc

    prompt = build_decision_prompt(
    application=application,
    prediction=prediction,
    retrieved_policies=retrieved_policies,
    )

    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "format": "json",
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "options": {
            "temperature": 0.2,
        },
    }

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise LLMServiceError(
            "Unable to connect to the local Ollama service."
        ) from exc

    response_data = response.json()
    raw_content = response_data["message"]["content"]

    try:
        generated_content = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise LLMServiceError(
            "The LLM returned invalid JSON."
        ) from exc

    required_fields = {
        "customer_message",
    }

    missing_fields = required_fields - generated_content.keys()

    if missing_fields:
        raise LLMServiceError(
            f"The LLM response is missing fields: {sorted(missing_fields)}"
        )

    if not isinstance(generated_content["customer_message"], str):
        raise LLMServiceError(
            "The LLM returned an invalid customer message."
        )
    return {
        "customer_message": generated_content["customer_message"],
        "rag_metadata": {
            "query": retrieval_result["query"],
            "retrieved_count": retrieval_result["retrieved_count"],
            "total_indexed_chunks": retrieval_result[
                "total_indexed_chunks"
            ],
            "embedding_model": retrieval_result["embedding_model"],
            "policies": retrieved_policies,
        },
    }