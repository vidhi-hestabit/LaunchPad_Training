import os
import sys
sys.path.append(os.path.abspath(".."))
import uuid
import numpy as np
from PIL import Image
from tqdm import tqdm
from day_3.src.embeddings.clip_embedder import CLIPEmbedder
from day_3.src.utils.ocr import extract_ocr_text
from day_3.src.utils.caption import ImageCaptioner
from day_3.src.utils.pdf_utils import pdf_to_images
from day_3.src.vectorstore.faiss_store import faiss_exists, save_faiss

RAW_DIR = "src/data/raw"
def ingest_images():
    if faiss_exists():
        print("FAISS already exists. Skipping ingestion.")
        return
    embedder = CLIPEmbedder()
    captioner = ImageCaptioner()
    vectors = []
    metadata = []
    files = os.listdir(RAW_DIR)
    if not files:
        raise RuntimeError("src/data/raw is empty")

    for file in tqdm(files, desc="Ingesting images"):
        path = os.path.join(RAW_DIR, file)
        images = (
            pdf_to_images(path)
            if file.lower().endswith(".pdf")
            else [Image.open(path).convert("RGB")]
        )
        for img in images:
            embedding = embedder.embed_image(img)
            vectors.append(embedding)
            metadata.append({
                "id": str(uuid.uuid4()),
                "file_name": file,
                "caption": captioner.generate_caption(img),
                "ocr_text": extract_ocr_text(img)
            })

    vectors = np.array(vectors)
    if len(vectors) == 0:
        raise RuntimeError("No embeddings generated")
    save_faiss(vectors, metadata)

if __name__ == "__main__":
    ingest_images()