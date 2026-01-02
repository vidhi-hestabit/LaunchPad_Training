from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
def load_documents(file_path: str):
    file_path = Path(file_path)
    loaders = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".txt": TextLoader,
    }

    if file_path.suffix.lower() not in loaders:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")
    
    return loaders[file_path.suffix.lower()](str(file_path)).load()