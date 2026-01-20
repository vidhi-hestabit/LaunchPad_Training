import requests

class OllamaLLM:
    def __init__(self):
        # Model you already pulled with Ollama
        self.model = "hf.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M"
        self.url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        """
        Sends the prompt to Ollama local server and returns the response text.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": max_tokens
            }
        }

        response = requests.post(self.url, json=payload)
        response.raise_for_status()  # Raise error if request fails

        # The generated text is under 'response'
        return response.json()["response"]
