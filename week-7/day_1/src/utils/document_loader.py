from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)


def load_documents(file_path: str):
    file_path = Path(file_path)
    ext = file_path.suffix.lower()

    loader_map = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".txt": TextLoader,
    }

    if ext not in loader_map:
        raise ValueError(f"Unsupported file format: {ext}")

    loader = loader_map[ext](str(file_path))
    return loader.load()
