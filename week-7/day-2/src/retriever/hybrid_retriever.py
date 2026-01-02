class HybridRetriever:
    def __init__(self, vector_db, embedder):
        self.vector_db = vector_db
        self.embedder = embedder

    def retrieve(self, query, top_k=10):
        query_emb = self.embedder.embed([query])[0]
        return self.vector_db.search(query_emb, top_k)
