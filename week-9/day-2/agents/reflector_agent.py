from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken


class ReflectorAgent:
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="reflector",
            system_message=(
                "You are a reflection agent.\n"
                "Merge multiple worker outputs into ONE coherent answer.\n"
                "Fix inconsistencies.\n"
                "Do NOT just summarize.\n"
                "Think like a domain expert."
            ),
            model_client=model_client,
        )

    async def run(self, worker_outputs: list[str]):
        cancellation = CancellationToken()

        merged_input = "\n\n".join(worker_outputs)

        response = await self.agent.on_messages(
            [TextMessage(content=merged_input, source="workers")],
            cancellation,
        )

        return response.chat_message.content
