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
    filePath = os.path.join(raw_dir, file)
    docs = load_documents(filePath)
    for doc in docs:
        chunks = text_splitter.split_text(doc["text"])
        for i, chunk in enumerate(chunks):
            chunk_metadata = {"source": doc["metadata"]["source"], "chunk_index": i}
            all_chunks.append({"text": chunk, "metadata": chunk_metadata})

with open(f"{chunk_dir}/chunks.json", "w") as f:
    json.dump(all_chunks, f, indent=2)

print(f"Created {len(all_chunks)} chunks")
