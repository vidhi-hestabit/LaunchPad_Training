import os
import sys
from PIL import Image
import numpy as np

sys.path.append(os.path.abspath(".."))

from day_3.src.embeddings.clip_embedder import CLIPEmbedder
from day_3.src.vectorstore.faiss_store import search_faiss
from day_3.generator.llm_client import get_openai_client, generate_image  


class ImageSearch:
    def __init__(self):
        self.embedder = CLIPEmbedder()

    def image_to_text_answer(self, image: Image.Image, top_k=1):
        query_vector = self.embedder.embed_image(image)
        results = search_faiss(query_vector, top_k)

        answers = []
        for r in results:
            image_path = os.path.join("src/data/raw", r.get("file_name", ""))
            if os.path.exists(image_path):
                similar_image = Image.open(image_path).convert("RGB")
            else:
                similar_image = None

            answers.append({
                "caption": r.get("caption", ""),
                "ocr_text": r.get("ocr_text", ""),
                "image_path": image_path,
                "image_obj": similar_image
            })

        return answers


def image_query_llm(image: Image.Image, user_query: str, top_k=1):
    search = ImageSearch()
    llm = get_openai_client()

    results = search.image_to_text_answer(image, top_k)
    if not results:
        return "I don't know based on the provided images.", []

    context = "\n\n".join(
        f"[IMAGE {i+1}]\nCaption: {r['caption']}\nOCR:\n{r['ocr_text']}"
        for i, r in enumerate(results)
    )

    system_prompt = f"""
You are an Image-RAG assistant.
Answer ONLY using the context below.
Provide the best fitted image to provided context no irrelevant information.

Context:
{context}

If the answer is not present, say:
"I don't know based on the provided images."
"""

    response = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0.1,
        max_tokens=300
    )

    return response.choices[0].message.content.strip(), results


if __name__ == "__main__":
    choice = input("Do you want to [1] Query an image or [2] Generate a new image? (1/2): ").strip()

    if choice == "1":
        image_path = input("Enter path to image: ").strip()
        query = input("Ask something about the image: ").strip()

        image = Image.open(image_path).convert("RGB")

        answer, references = image_query_llm(image, query)
        print("\nAnswer:\n", answer)

        for i, ref in enumerate(references, 1):
            print(f"\n[REFERENCE IMAGE {i}] {ref['image_path']}")
            if ref["image_obj"]:
                ref["image_obj"].show()

    elif choice == "2":
        prompt = input("Enter prompt to generate image: ").strip()
        images = generate_image(prompt, n_images=1)
        save_path = "generated_image.png"
        images[0].save(save_path)
        print(f"Image generated and saved at {save_path}")

    else:
        print("Invalid choice. Please enter 1 or 2.")
