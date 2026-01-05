import os
import json
import faiss
import numpy as np

FAISS_DIR = "src/data/faiss"
INDEX_PATH = f"{FAISS_DIR}/index.faiss"
META_PATH = f"{FAISS_DIR}/metadata.json"
os.makedirs(FAISS_DIR, exist_ok=True)

def faiss_exists() -> bool:
    return os.path.exists(INDEX_PATH) and os.path.exists(META_PATH)

def save_faiss(vectors: np.ndarray, metadata: list):
    if len(vectors) == 0:
        raise ValueError("No vectors to save. Ingestion failed.")

    print("Saving FAISS index with", len(vectors))

    vectors = vectors.astype("float32")
    faiss.normalize_L2(vectors)

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w") as f:
        json.dump(metadata, f, indent=2)
    print("FAISS files written to:", FAISS_DIR)

def load_faiss():
    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH) as f:
        metadata = json.load(f)
    return index, metadata


def search_faiss(query_vector: np.ndarray, top_k=3):
    index, metadata = load_faiss()

    query_vector = query_vector.astype("float32").reshape(1, -1)
    faiss.normalize_L2(query_vector)

    _, idxs = index.search(query_vector, top_k)
    return [metadata[i] for i in idxs[0]]
