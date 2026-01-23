class Orchestrator:
    def __init__(self, research_agent, summarizer_agent, answer_agent, memory_window=10):
        self.research_agent = research_agent
        self.summarizer_agent = summarizer_agent
        self.answer_agent = answer_agent
        self.memory_window = memory_window
        self.user_memory = []
        
    def trim_memory(self):
        while len(self.user_memory) > self.memory_window:
            self.user_memory.pop(0)

    def run(self, user_query: str):
        self.user_memory.append(user_query)
        self.trim_memory()
        research_output = self.research_agent.run(user_query).strip()
        summary_output = self.summarizer_agent.run(research_output).strip()
        answer_output = self.answer_agent.run(summary_output).strip()

        return {
            "research": research_output,
            "summary": summary_output,
            "answer": answer_output
        }
