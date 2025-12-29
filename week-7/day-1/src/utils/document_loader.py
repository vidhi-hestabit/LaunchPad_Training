import os
from pypdf import PdfReader
from docx import Document

def load_documents(file_path):
    documents = []
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".pdf":
        reader = PdfReader(file_path)
        for pgNo, pg in enumerate(reader.pages):
            text = pg.extract_text()
            if text is None:
                text = ""
            documents.append({"text": text, "metadata": {"source": f"{file_path}_page_{pgNo + 1}"}
            })
    elif extension == ".docx":
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        documents.append({"text": text, "metadata": {"source": file_path}
        })
    elif extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        documents.append({"text": text, "metadata": {"source": file_path}
        })
    else:
        raise ValueError(f"Unsupported file format: {extension}")
    return documents
