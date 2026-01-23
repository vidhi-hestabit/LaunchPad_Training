import json

class BaseAgent:
    def __init__(self, name, system_prompt, llm, max_memory=10, memory_file=None):
        self.name = name
        self.system_prompt = system_prompt.strip()
        self.llm = llm
        self.memory = []
        self.max_memory = max_memory
        self.memory_file = memory_file

        if self.memory_file:
            self.load_memory(self.memory_file)

    def trim_memory(self):
        max_messages = self.max_memory * 2
        while len(self.memory) > max_messages:
            self.memory.pop(0)

    def build_messages(self, user_input):
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.memory)
        messages.append({"role": "user", "content": user_input})
        return messages

    def run(self, user_input: str) -> str:
        messages = self.build_messages(user_input)
        try:
            response = self.llm.generate(messages)
        except Exception as e:
            response = f"[LLM ERROR] {str(e)}"

        self.memory.append({"role": "user", "content": user_input})
        self.memory.append({"role": "assistant", "content": response})
        self.trim_memory()

        if self.memory_file:
            self.save_memory(self.memory_file)

        return response

    def load_memory(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.memory = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.memory = []

    def save_memory(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)
