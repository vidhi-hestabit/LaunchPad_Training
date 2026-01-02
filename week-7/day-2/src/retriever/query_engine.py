import os
import sys
sys.path.append(os.path.abspath("."))

from src.pipelines.ingest import ingest
from src.retriever.hybrid_retriever import HybridRetriever
from src.retriever.reranker import Reranker
from src.utils.openai import get_openai_client


SYSTEM_PROMPT = """
You are a Retrieval-Augmented Generation (RAG) assistant.

Rules:
- Use ONLY the provided context
- Do NOT use external knowledge
- If the answer is not present, say:
  "I don't know based on the provided documents."
- Cite using [CHUNK X] and page number if available
- Provide the page number also [Page no.] from where you get the answer.
- Be concise and factual
"""

def build_prompt(question: str, context: str) -> str:
    return f""" Context: {context} Question: {question}

Answer using only the context above.
"""

class QueryEngine:
    def __init__(self):
        vector_db, embedder = ingest()
        self.retriever = HybridRetriever(vector_db, embedder)
        self.reranker = Reranker()
        self.client = get_openai_client()
        self.model = os.getenv("MODEL")

    def _build_context(self, docs):
        blocks = []
        for i, doc in enumerate(docs, start=1):
            meta = doc.get("metadata", {})
            page = meta.get("page", "unknown")

            blocks.append(
                f"""[CHUNK {i}]
Source: {meta.get("source", "unknown")}
Page: {page}
{doc["text"]}"""
            )

        return "\n\n".join(blocks)

    def ask(self, query: str, top_k: int = 5):
        candidates = self.retriever.retrieve(query, top_k=top_k*2)
        docs = self.reranker.rerank(query, candidates, top_k=top_k)
        context = self._build_context(docs)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_prompt(query, context)},
            ],
            temperature=0.1,
            max_tokens=300,
        )

        return response.choices[0].message.content.strip()

if __name__ == "__main__":
    engine = QueryEngine()
    print(engine.ask("Tell about Tom Nichols?"))
