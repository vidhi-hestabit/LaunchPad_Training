import json
import os
from datetime import datetime

MEMORY_FILE = "logs/CHAT-LOGS.json"
MAX_TURNS = 5

os.makedirs("logs", exist_ok=True)


class MemoryStore:
    def __init__(self):
        # Ensure file exists AND is valid JSON
        if not os.path.exists(MEMORY_FILE):
            self._reset_file()

    def _reset_file(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump([], f)
    def clear(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump([], f)

    def load(self):
        try:
            with open(MEMORY_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            # Auto-heal corrupted memory
            self._reset_file()
            return []

    def save(self, messages):
        with open(MEMORY_FILE, "w") as f:
            json.dump(messages[-MAX_TURNS:], f, indent=2)

    def add(self, role, content):
        messages = self.load()
        messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.save(messages)

    def get_context(self):
        messages = self.load()
        return "\n".join(
            f"{m['role'].upper()}: {m['content']}"
            for m in messages[-MAX_TURNS:]
        )
