# generates embedding.

import json
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

def generate_embeddings():
    print("Loading documents...")
    with open("data/documents.json", "r", encoding="utf-8") as f:
        documents = json.load(f)

    texts = [doc["text"] for doc in documents]

    print("Loading SentenceTransformer model...")
    model = SentenceTransformer("all-MiniLM-L6-v2", device='cpu')

    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    np.save("data/embeddings.npy", embeddings)

    print(f"Total saved embeddings: {len(embeddings)}")


if __name__ == "__main__":
    generate_embeddings()
