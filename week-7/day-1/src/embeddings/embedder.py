import json
import numpy as np
from sentence_transformers import SentenceTransformer

chunk_file = "src/data/chunks/chunks.json"
embedding_file = "src/embeddings/embeddings.npy"

model = SentenceTransformer('sentence-transformers/sentence-t5-base')

def load_chunks(file_path):
    with open(file_path, 'r') as f:
        chunks = json.load(f)
    return chunks

def embed_chunks(chunks, model):
    texts = [chunk['text'] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings

def save_embeddings(embeddings, file_path):
    np.save(file_path, embeddings)
if __name__ == "__main__":
    chunks = load_chunks(chunk_file)
    embeddings = embed_chunks(chunks, model)
    save_embeddings(embeddings, embedding_file)
    print(f"Saved embeddings to {embedding_file}")
