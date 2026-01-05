import os
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from day_2.src.utils.document_loader import load_documents

def create_chunks(raw_dir=None, chunk_dir=None):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    raw_dir = raw_dir or os.path.join(BASE_DIR, "data/raw")
    chunk_dir = chunk_dir or os.path.join(BASE_DIR, "data/chunks")

    if not os.path.exists(raw_dir):
        os.makedirs(raw_dir, exist_ok=True)
        print(f"[WARN] Raw folder did not exist. Created: {raw_dir}")

    os.makedirs(chunk_dir, exist_ok=True)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    
    all_chunks = []
    
    for file in os.listdir(raw_dir):
        file_path = os.path.join(raw_dir, file)
        docs = load_documents(file_path)
        chunks = splitter.split_documents(docs)

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "text": chunk.page_content,
                "metadata": {
                    **chunk.metadata,
                    "source": file,
                    "chunk_index": i,
                }
            })
    chunks_file = os.path.join(chunk_dir, "chunks.json")
    with open(chunks_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Total chunks created: {len(all_chunks)} | Saved at: {chunks_file}")
    return all_chunks
