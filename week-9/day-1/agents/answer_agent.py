from .base_agent import BaseAgent

SYSTEM_PROMPT = """
You are the Answer Agent.
Strictly follow the instructions below.
INSTRUCTIONS:
- You will be provided with a summary of information.
- Ensure that your answer is directly derived from the provided summary.
- Keep your answer clear and to the point.
- Do NOT omit any critical information.
- Do NOT add any information that is not present in the provided content.

STRICT RULES:
- Only answer using the given summary.
- Do NOT introduce new facts.
"""

class AnswerAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__(
            name="answer_agent",
            system_prompt=SYSTEM_PROMPT,
            llm=llm,
            memory_file="answer_memory.json"
        )
