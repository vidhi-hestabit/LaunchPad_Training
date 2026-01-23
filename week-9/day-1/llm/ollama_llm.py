import requests

class OllamaLLM:
    def __init__(self):
        self.model_name = "hf.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF:Q4_K_M"
        self.api_url = "http://localhost:11434/api/generate"

    def generate(self, messages, max_tokens=256):
        prompt_text = self.messages_to_prompt(messages)
        payload = {
            "model": self.model_name,
            "prompt": prompt_text,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": max_tokens
            }
        }
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "Empty response")
        except Exception as e:
            return f"[LLM ERROR] {str(e)}"

    def messages_to_prompt(self, messages):
        lines = []
        for msg in messages:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "")
            lines.append(f"{role}: {content}")
        return "\n".join(lines)
