from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
class ValidatorAgent:
    def __init__(self, model_client):
        self.agent = AssistantAgent(
            name="validator",
            system_message=(
                "You are an expert evaluator.\n"
                "Your job is to validate multiple worker responses.\n"
                "Check for:\n"
                "- Accuracy\n"
                "- Completeness\n"
                "- Conflicts\n"
                "- Logical consistency\n\n"
                "FORMAT:\n"
                "SUMMARY: <short verdict>\n"
                "ISSUES: <list conflicts or errors>\n"
                "BEST_RESPONSE: <index or short reason>\n"
            ),
            model_client=model_client,
        )

    async def run(self, query: str, worker_outputs: list[str]):
        cancellation = CancellationToken()
        merged = "\n\n".join(
            f"WORKER {i+1}:\n{output}"
            for i, output in enumerate(worker_outputs)
        )
        content = f"QUERY:\n{query}\n\nRESPONSES:\n{merged}"
        response = await self.agent.on_messages(
            [TextMessage(content=content, source="workers")],
            cancellation,
        )

        return response.chat_message.content
