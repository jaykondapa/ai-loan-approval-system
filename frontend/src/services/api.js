const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function handleResponse(response, fallbackMessage) {
  if (!response.ok) {
    let errorMessage = fallbackMessage;

    try {
      const errorData = await response.json();

      if (errorData.detail) {
        errorMessage =
          typeof errorData.detail === "string"
            ? errorData.detail
            : JSON.stringify(errorData.detail);
      }
    } catch {
      // Keep the fallback message when the response is not JSON.
    }

    throw new Error(errorMessage);
  }

  return response.json();
}

export async function predictLoan(application) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(application),
  });

  return handleResponse(response, "Unable to complete the prediction.");
}

export async function getModelInfo() {
  const response = await fetch(`${API_BASE_URL}/model-info`);

  return handleResponse(response, "Unable to load model information.");
}

export async function predictLoanWithExplanation(application) {
  const response = await fetch(
    `${API_BASE_URL}/predict-with-explanation`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(application),
    }
  );

  return handleResponse(
    response,
    "Unable to generate the loan assessment."
  );
}