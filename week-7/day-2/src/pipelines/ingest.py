import os
import sys
sys.path.append(os.path.abspath("."))
from src.embeddings.embedder import GeminiEmbedder
from src.utils.chunker import create_chunks
from src.vectorstore.index_faiss import FaissVectorDB

def ingest(force_rebuild=False):
    embedder = GeminiEmbedder()

    if os.path.exists("src/vectorstore/index.faiss") and not force_rebuild:
        print("Using existing FAISS index")
        db = FaissVectorDB(load_existing=True)
        return db, embedder
    chunks = create_chunks()
    embeddings = embedder.embed([c["text"] for c in chunks])

    db = FaissVectorDB(
        load_existing=False,
        dim=embeddings.shape[1]
    )
    db.add(embeddings, chunks)
    return db, embedder
