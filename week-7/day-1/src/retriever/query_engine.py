import faiss
import sys
import os
sys.path.append(os.path.abspath("."))
import json
from sentence_transformers import SentenceTransformer
from src.utils.openai import get_openai_client

client = get_openai_client()

model = SentenceTransformer("sentence-transformers/sentence-t5-base")

index = faiss.read_index("src/vectorstore/index.faiss")
with open("src/vectorstore/metadata.json") as f:
    metadata = json.load(f)

def ask(query, k=5):
    q_emb = model.encode([query]).astype("float32")
    _, idxs = index.search(q_emb, k)
    chunks = [metadata[i] for i in idxs[0]]
    context = ""
    for c in chunks:
        text = c.get("text", "")
        meta = c.get("metadata", {})
        context += f"Source: {meta.get('source', 'unknown')}, Chunk: {meta.get('chunk_index', 'N/A')}\n{text}\n\n"
    
    prompt = f"""
You are an expert assistant. Using the context below, answer the question concisely.
Review the context and provide a detailed answer.
Read in detail the metadata associated with each chunk to provide accurate references.
No irrelevant or wrong information, if you don't know, just say you don't know.
Context: {context}
Question: {query}
Answer:
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert assistant who can reason over metadata and text chunks."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=300
    )
    answer = response.choices[0].message.content.strip()
    return answer, [c["metadata"] for c in chunks]

if __name__ == "__main__":
    query = "What topics do the document cover?"
    answer, meta = ask(query)
    print("Answer:\n \n", answer)
    print("Source metadata:", meta)
