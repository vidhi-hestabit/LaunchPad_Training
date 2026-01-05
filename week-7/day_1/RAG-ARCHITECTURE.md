--- 
Day-1 RAG-ARCHITECTURE.md 
---

RAG (Retrieval Augumented Generator) :
- involves info retrieval with LLM generation.
- why needed ?
--- Hallucinations
--- No access to private/internal data
--- Knowledge cutoff
--- No source grounding


User query -> Query Encoder -> Retriever (Vectordb) -> Relevant context -> Prompt builder -> LLM Generator -> Result
---
```
Have created folders 
- day_1
    -- src
            --- data/chunks -- chunks.json generated
            --- data/raw/__raw_data(pdf)
            --- utils/document_loader.py
            --- pipelines/ingest.py
            --- embeddings/embedder.py
            --- vectorstore/index_faiss.py -- index.faiss and metadata.json generated
            --- retriever/query_engine.py
    -- requirements.txt
    -- .gitignore
---
```
-> Model used to generate Embeddings :
sentence-transformers/sentence-t5-base

-> LLM Model :
llama-3.1-8b-instant

-> FAISS normalization function :
faiss.normalize_L2 is a function in the Faiss library that performs L2 normalization on a set of vectors in-place. This means it modifies each vector so that its L2 norm (Euclidean length) equals one (a unit vector). 

