import json

from src.explanation_mapping import build_readable_application

from src.rag_service import format_retrieved_policies


SYSTEM_PROMPT = """
You generate loan-assessment communication for two separate audiences:

1. A customer-facing message.
2. An internal loan-officer summary.

The machine-learning system provides only a preliminary credit-risk assessment.
It does not issue a final lending decision, approve a specific loan amount,
determine an interest rate, or establish repayment terms.

Rules:
1. Never change or contradict the supplied model decision.
2. Use only facts explicitly provided in the prompt.
3. Never invent income, salary, credit score, debt-to-income ratio,
   affordability, financial stability, or undocumented information.
4. Never claim that a specific applicant feature caused the decision.
5. Do not make discriminatory statements or infer protected characteristics.
6. Do not present the model result as a final lending decision.
7. Do not state that the requested amount, duration, interest rate, or loan
   terms have been approved.
8. Keep customer communication simple, respectful, and non-technical.
9. Keep internal communication concise, factual, and clearly structured.
10. Return valid JSON only.
"""


def build_decision_prompt(
    application: dict,
    prediction: dict,
    retrieved_policies: list[dict],
) -> str:
    readable_application = build_readable_application(application)
    policy_context = format_retrieved_policies(
    retrieved_policies
    )

    return f"""
Generate communication for the following preliminary credit-risk assessment.

APPLICATION DATA:
{json.dumps(readable_application, indent=2)}

INTERNAL MODEL RESULT:
Decision: {prediction["decision"]}
Approval probability: {prediction["approval_probability"]}
Risk probability: {prediction["risk_probability"]}
Risk level: {prediction["risk_level"]}
Confidence: {prediction["confidence"]}

RETRIEVED DEMONSTRATION POLICIES:
{policy_context}

POLICY USAGE RULES:
- Treat the retrieved policies as the source of truth for customer communication.
- Follow only policies relevant to the supplied preliminary assessment.
- Do not invent institutional policies that are absent from the retrieved context.
- If the prompt instructions and retrieved policies appear inconsistent,
  follow the stricter safety requirement.

CUSTOMER MESSAGE RULES:
- Write a professional customer-facing update of 3 to 5 sentences.
- Personalize the message using the requested loan purpose when it reads naturally.
- Keep the wording warm, clear, and non-technical.
- Vary the wording naturally across applications.

IF THE MODEL DECISION IS APPROVED:
- Clearly state that the application received a favorable preliminary assessment.
- You may use warm language such as "Congratulations" or "You're one step closer."
- Explain that submitted information may still be verified and supporting documents may be requested.
- Explain that a final decision and any applicable terms will be communicated after review.

IF THE MODEL DECISION IS REJECTED:
- Clearly state that the application did not receive a favorable preliminary assessment.
- Use respectful and neutral language.
- Do not use "Congratulations," "one step closer," "approved," or other positive-outcome wording.
- Do not suggest that submitting additional information or documents is likely to change the result.
- State only that further communication will follow if required or once the review process has concluded.

DO NOT:
- Contradict the supplied model decision.
- Say the requested amount or loan terms were approved.
- Say financing is guaranteed, finalized, or ready to be issued.
- Mention AI, machine learning, models, probabilities, confidence, or risk scores.
- Invent reasons for the result.
- Mention sensitive applicant characteristics.

Return valid JSON with exactly this field:

{{
  "customer_message": "A short, non-technical customer-facing message."
}}

The value must be a JSON string.

Do not return a loan-officer summary.
Do not include markdown, code fences, or additional fields.
"""