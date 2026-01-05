import os
import sys
import json
import faiss
sys.path.append(os.path.abspath("."))
import numpy as np
from sentence_transformers import SentenceTransformer
from generator.llm_client import get_openai_client

client = get_openai_client()

EMBEDDING_MODEL = "sentence-transformers/sentence-t5-base"
LLM_MODEL = "llama-3.1-8b-instant"

model = SentenceTransformer(EMBEDDING_MODEL)

index = faiss.read_index("src/vectorstore/index.faiss")

with open("src/vectorstore/metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

with open("src/data/chunks/chunks.json", "r", encoding="utf-8") as f:
    chunks_data = json.load(f)

assert index.ntotal == len(metadata) == len(chunks_data), (
    "FAISS index, metadata, and chunks are not aligned"
)

SYSTEM_PROMPT = """
You are a Retrieval-Augmented Generation (RAG) assistant.

Strict rules:
- Use ONLY the provided context.
- Do NOT use external knowledge.
- If the answer is not present, say:
- "I don't know based on the provided documents."
- Cite answers using chunk numbers like [CHUNK 1].
- Be concise, factual, and accurate.
"""

def build_user_prompt(question: str, context: str) -> str:
    return f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}

Answer format:
- Start with a direct answer.
- List key supporting points.
- End with citations in square brackets.
"""

def build_context(retrieved_chunks):
    blocks = []
    for i, c in enumerate(retrieved_chunks, start=1):
        meta = c["metadata"]
        blocks.append(
            f"""
[CHUNK {i}]
Page: {meta.get("page", "N/A")}
{c["text"]}
""".strip()
        )
    return "\n\n".join(blocks)

def ask(query: str, k: int = 5):
    # Encode + normalize query (cosine similarity)
    q_emb = model.encode([query]).astype("float32")
    faiss.normalize_L2(q_emb)

    # FAISS search
    _, idxs = index.search(q_emb, k)

    retrieved_chunks = [chunks_data[i] for i in idxs[0]]

    context = build_context(retrieved_chunks)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(query, context)}
        ],
        temperature=0.1,
        max_tokens=300
    )

    answer = response.choices[0].message.content.strip()
    sources = [c["metadata"] for c in retrieved_chunks]

    return answer, sources

if __name__ == "__main__":
    query = "what does it mean by micro-business?"
    answer, source_metadata = ask(query)

    print("\nAnswer:\n")
    print(answer)
    # print("\nSource Metadata:\n")
    # for meta in source_metadata:
    #     print(meta)
