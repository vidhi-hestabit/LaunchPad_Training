# Image RAG (Retrieval-Augmented Generation) System

## Key Components

### 1. Image Embeddings (CLIP)

* Uses **OpenAI CLIP (openai/clip-vit-base-patch32)** to convert images into dense vector embeddings.
* Supports GPU acceleration if CUDA is available.
* Ensures that both query images and stored images lie in the same embedding space.

### 2. Image Ingestion Pipeline

* Reads images and PDFs from `src/data/raw`.
* Converts PDFs into images.
* For each image:


  * Generates a CLIP embedding
  * Extracts OCR text using Tesseract
  * Generates a caption using BLIP
  - Image Captioner - using model="Salesforce/blip-image-captioning-base"

* Stores embeddings in FAISS and metadata in `metadata.json`.

### 3. Vector Store (FAISS)

* Uses **FAISS IndexFlatIP** with cosine similarity.
* Normalizes vectors before indexing and querying.
* Enables fast similarity search over image embeddings.

### 4. Image Retrieval

* Accepts a query image.
* Computes its CLIP embedding.
* Retrieves top-k most similar images from FAISS.
* Returns captions, OCR text, and image references as context.

### 5. Image Question Answering (Image RAG)

* Builds a structured context from retrieved images.
* Passes the context and user question to an LLM.
* The LLM answers strictly based on retrieved image information.

![alt text](<Screenshot from 2026-01-02 18-32-20.png>)

---

## Folder Structure

```
src/
├── data/
│   ├── raw/            # Input images and PDFs
│   └── faiss/          # FAISS index and metadata
├── embeddings/         # CLIP embedder
│   ├── clip_embedder.py
├── utils/              # OCR, captioning, PDF utilities
│   ├── caption.py
│   ├── ocr.py
│   ├── pdf_utils.py            
├── vectorstore/        # FAISS storage and search
│   ├── faiss_store.py       
└── retriever/          # Image search and RAG logic
│   ├── image_search.py          
```

---

## Supported Capabilities

* Image similarity search
* OCR-based text understanding
* Image caption grounding
* PDF image ingestion
* Context-aware image question answering

---
