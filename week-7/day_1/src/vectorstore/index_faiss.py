import faiss
import numpy as np
import json
chunk_file = "src/data/chunks/chunks.json"
embedding_file = "src/embeddings/embeddings.npy"
faiss_index_file = "src/vectorstore/index.faiss"
metadata_file = "src/vectorstore/metadata.json"

embeddings = np.load(embedding_file).astype("float32")

with open(chunk_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

assert len(embeddings) == len(chunks), (
    f"Embeddings ({len(embeddings)}) != Chunks ({len(chunks)})"
)
faiss.normalize_L2(embeddings)

dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

faiss.write_index(index, faiss_index_file)
metadata = [
    {
        "source": chunk["metadata"].get("source"),
        "page": chunk["metadata"].get("page"),
        "chunk_index": chunk["metadata"].get("chunk_index"),
    }
    for chunk in chunks
]

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print(f"Number of vectors in index: {index.ntotal}")
