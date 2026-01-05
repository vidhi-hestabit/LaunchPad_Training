import os
import json
import sys
sys.path.append(os.path.abspath("."))
from src.utils.document_loader import load_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter

raw_dir = "src/data/raw/"
chunk_dir = "src/data/chunks/"

os.makedirs(chunk_dir, exist_ok=True)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
)

all_chunks = []
for file in os.listdir(raw_dir):
    file_path = os.path.join(raw_dir, file)
    docs = load_documents(file_path)
    chunks = text_splitter.split_documents(docs)

    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "text": chunk.page_content,
            "metadata": {
                **chunk.metadata,
                "chunk_index": i
            }
        })

with open(os.path.join(chunk_dir, "chunks.json"), "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=2, ensure_ascii=False)

print(f"Created {len(all_chunks)} chunks")
