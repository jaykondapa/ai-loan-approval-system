import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
POLICY_DIRECTORY = PROJECT_ROOT / "knowledge" / "policies"
INDEX_DIRECTORY = PROJECT_ROOT / "knowledge" / "index"

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
CHUNK_SIZE_WORDS = 90
CHUNK_OVERLAP_WORDS = 20


def split_text(
    text: str,
    chunk_size: int = CHUNK_SIZE_WORDS,
    overlap: int = CHUNK_OVERLAP_WORDS,
) -> list[str]:
    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def load_policy_chunks() -> list[dict]:
    chunks = []

    for file_path in sorted(POLICY_DIRECTORY.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")

        for chunk_number, chunk_text in enumerate(split_text(text), start=1):
            chunks.append(
                {
                    "id": f"{file_path.stem}-{chunk_number}",
                    "source": file_path.name,
                    "text": chunk_text,
                }
            )

    if not chunks:
        raise RuntimeError(
            f"No policy documents were found in {POLICY_DIRECTORY}."
        )

    return chunks


def main() -> None:
    chunks = load_policy_chunks()

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    INDEX_DIRECTORY.mkdir(parents=True, exist_ok=True)

    np.save(
        INDEX_DIRECTORY / "policy_embeddings.npy",
        embeddings,
    )

    metadata = {
        "embedding_model": EMBEDDING_MODEL_NAME,
        "chunk_size_words": CHUNK_SIZE_WORDS,
        "chunk_overlap_words": CHUNK_OVERLAP_WORDS,
        "chunks": chunks,
    }

    with (INDEX_DIRECTORY / "policy_chunks.json").open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(metadata, file, indent=2)

    print(f"Indexed {len(chunks)} policy chunks.")
    print(f"Index saved to: {INDEX_DIRECTORY}")


if __name__ == "__main__":
    main()