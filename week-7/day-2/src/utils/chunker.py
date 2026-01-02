import os, json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.document_loader import load_documents

def create_chunks(
    raw_dir="src/data/raw/",
    chunk_dir="src/data/chunks/",
):
    os.makedirs(chunk_dir, exist_ok=True)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    
    all_chunks = []
    for file in os.listdir(raw_dir):
        docs = load_documents(os.path.join(raw_dir, file))
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

    with open(f"{chunk_dir}/chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    return all_chunks
