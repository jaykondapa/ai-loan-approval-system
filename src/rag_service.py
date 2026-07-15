import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_DIRECTORY = PROJECT_ROOT / "knowledge" / "index"

CHUNKS_PATH = INDEX_DIRECTORY / "policy_chunks.json"
EMBEDDINGS_PATH = INDEX_DIRECTORY / "policy_embeddings.npy"

DEFAULT_TOP_K = 3


class RAGServiceError(RuntimeError):
    """Raised when policy retrieval cannot be completed."""


class PolicyRetriever:
    def __init__(self) -> None:
        if not CHUNKS_PATH.exists():
            raise RAGServiceError(
                "Policy chunk metadata was not found. "
                "Run 'py -3.9 -m rag.build_index' first."
            )

        if not EMBEDDINGS_PATH.exists():
            raise RAGServiceError(
                "Policy embeddings were not found. "
                "Run 'py -3.9 -m rag.build_index' first."
            )

        with CHUNKS_PATH.open("r", encoding="utf-8") as file:
            metadata = json.load(file)

        self.chunks = metadata["chunks"]
        self.embedding_model_name = metadata["embedding_model"]

        self.embeddings = np.load(EMBEDDINGS_PATH)

        if len(self.chunks) != len(self.embeddings):
            raise RAGServiceError(
                "The number of policy chunks does not match "
                "the number of stored embeddings."
            )

        self.model = SentenceTransformer(
            self.embedding_model_name
        )

    def retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
    ) -> list[dict]:
        if not query or not query.strip():
            raise RAGServiceError(
                "The policy retrieval query cannot be empty."
            )

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
        )[0]

        # Embeddings were normalized while building the index,
        # so the dot product produces cosine similarity.
        similarity_scores = np.dot(
            self.embeddings,
            query_embedding,
        )

        number_to_return = min(top_k, len(self.chunks))

        top_indices = np.argsort(
            similarity_scores
        )[::-1][:number_to_return]

        results = []

        for index in top_indices:
            chunk = self.chunks[int(index)]

            results.append(
                {
                    "id": chunk["id"],
                    "source": chunk["source"],
                    "text": chunk["text"],
                    "score": round(
                        float(similarity_scores[index]),
                        4,
                    ),
                }
            )

        return results


POLICY_RETRIEVER = PolicyRetriever()


def build_policy_query(
    model_decision: str,
    loan_purpose: str,
) -> str:
    decision_description = (
        "favorable preliminary loan assessment"
        if model_decision == "Approved"
        else "unfavorable preliminary loan assessment"
    )

    return (
        "Customer communication requirements for a "
        f"{decision_description}. "
        f"The requested loan purpose is {loan_purpose}. "
        "Retrieve rules about preliminary decisions, "
        "customer wording, unsupported promises, technical "
        "disclosures, approved terms, document requests, "
        "and final decision language."
    )


def retrieve_communication_policies(
    model_decision: str,
    loan_purpose: str,
    top_k: int = DEFAULT_TOP_K,
) -> dict:
    query = build_policy_query(
        model_decision=model_decision,
        loan_purpose=loan_purpose,
    )

    policies = POLICY_RETRIEVER.retrieve(
        query=query,
        top_k=top_k,
    )

    return {
        "query": query,
        "policies": policies,
        "retrieved_count": len(policies),
        "total_indexed_chunks": len(POLICY_RETRIEVER.chunks),
        "embedding_model": POLICY_RETRIEVER.embedding_model_name,
    }


def format_retrieved_policies(
    retrieved_policies: list[dict],
) -> str:
    formatted_sections = []

    for position, policy in enumerate(
        retrieved_policies,
        start=1,
    ):
        formatted_sections.append(
            "\n".join(
                [
                    f"Policy {position}",
                    f"Source: {policy['source']}",
                    f"Relevance score: {policy['score']}",
                    policy["text"],
                ]
            )
        )

    return "\n\n".join(formatted_sections)