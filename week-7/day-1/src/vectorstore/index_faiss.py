import faiss
import numpy as np
import json
import os

chunk_file = "src/data/chunks/chunks.json"
embedding_file = "src/embeddings/embeddings.npy"
faiss_index_file = "src/vectorstore/index.faiss"
metadata_file = "src/vectorstore/metadata.json"

embeddings = np.load(embedding_file).astype('float32')

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, faiss_index_file)

with open(chunk_file, "r") as f:
    chunks = json.load(f)

with open(metadata_file, "w") as f:
    json.dump(chunks, f, indent=2)

print(f"Number of vectors in index: {index.ntotal}")
