import faiss
import json
import os
import numpy as np

class FaissVectorDB:
    def __init__(
        self,
        index_path="src/vectorstore/index.faiss",
        meta_path="src/vectorstore/metadata.json",
        load_existing=True,
        dim=None,
    ):
        self.index_path = index_path
        self.meta_path = meta_path

        if load_existing and os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            self.dim = self.index.d 
            with open(meta_path, "r") as f:
                self.metadata = json.load(f)
        else:
            if dim is None:
                raise ValueError("provide dim when creating a new FAISS index")
            self.dim = dim
            self.index = faiss.IndexFlatL2(dim)
            self.metadata = []

    def add(self, embeddings: np.ndarray, chunks: list[dict]):
        assert embeddings.shape[1] == self.dim
        self.index.add(embeddings)
        self.metadata.extend(chunks)

        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)

        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

    def search(self, query_emb, top_k=5):
        assert query_emb.shape[0] == self.dim
        _, idxs = self.index.search(query_emb.reshape(1, -1), top_k)
        return [self.metadata[i] for i in idxs[0]]
