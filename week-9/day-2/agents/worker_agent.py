from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

class WorkerAgent:
    def __init__(self, name: str, task: str, model_client):
        self.name = name
        self.task = task
        self.agent = AssistantAgent(
            name=name,
            system_message=(
                "You are a worker agent.\n"
                "Your job is to complete the assigned task accurately and thoroughly.\n"
                "Think like an expert in the field.\n"
                "Execute ONLY the given task precisely.\n"
                f"TASK: {task}"
            ),
            model_client=model_client,
        )

    async def run(self, query: str):
        cancellation = CancellationToken()

        response = await self.agent.on_messages(
            [TextMessage(content=query, source="planner")],
            cancellation,
        )

        return {
            "agent": self.name,
            "task": self.task,
            "output": response.chat_message.content,
        }
