import asyncio
import json
from typing import Dict, List
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from orchestrator.prompt import PLANNER_PROMPT
from orchestrator.dag_schema import DAGNode
from orchestrator.json_utils import extract_json_object
from agents.worker_agent import WorkerAgent
from agents.reflector_agent import ReflectorAgent
from agents.validator import ValidatorAgent
from utils.model_client import get_model_client

class Planner:
    def __init__(self):
        self.model_client = get_model_client()
        self.execution_tree: Dict[str, Dict] = {}
        self.planner_agent = AssistantAgent(
            name="planner",
            system_message=PLANNER_PROMPT,
            model_client=self.model_client,
        )

    def _validate_dag(self, nodes: List[DAGNode]) -> None:
        ids = {n.id for n in nodes}
        for node in nodes:
            for dep in node.deps:
                if dep not in ids:
                    raise ValueError(f"Node '{node.id}' depends on unknown node '{dep}'")

        reflectors = [n for n in nodes if n.role == "reflector"]
        validators = [n for n in nodes if n.role == "validator"]

        if len(reflectors) != 1:
            raise ValueError("DAG must contain exactly one reflector")
        if len(validators) != 1:
            raise ValueError("DAG must contain exactly one validator")
        if reflectors[0].id not in validators[0].deps:
            raise ValueError("Validator must depend on reflector")

    async def create_plan(self, query: str) -> List[DAGNode]:
        cancellation = CancellationToken()
        async def _attempt(extra_hint=""):
            response = await self.planner_agent.on_messages(
                [TextMessage(content=query + extra_hint, source="user")],
                cancellation,
            )
            output = response.chat_message.content
            json_text = extract_json_object(output)
            raw = json.loads(json_text)

            if "nodes" not in raw:
                raise ValueError("Missing 'nodes' key")

            nodes = [DAGNode(**n) for n in raw["nodes"]]
            self._validate_dag(nodes)
            return nodes

        try:
            return await _attempt()
        except Exception:
            retry_hint = (
                "\n\nIMPORTANT:\n"
                "- Exactly one reflector\n"
                "- Exactly one validator\n"
                "- Validator must depend on reflector\n"
                "- Output ONLY JSON\n"
            )
            return await _attempt(retry_hint)

    async def run(self, query: str):
        nodes = await self.create_plan(query)

        results: Dict[str, str] = {}
        pending = {n.id: n for n in nodes}

        while pending:
            ready = [
                n for n in pending.values()
                if all(dep in results for dep in n.deps)
            ]

            if not ready:
                raise RuntimeError("Cyclic or invalid DAG detected")

            tasks = []

            for node in ready:
                if node.role == "worker":
                    agent = WorkerAgent(node.id, node.task, self.model_client)
                    tasks.append(self._run_worker(agent, node, query))

                elif node.role == "reflector":
                    agent = ReflectorAgent(self.model_client)
                    inputs = [results[d] for d in node.deps]
                    tasks.append(self._run_reflector(agent, node, inputs))

                elif node.role == "validator":
                    agent = ValidatorAgent(self.model_client)
                    input_text = results[node.deps[0]]
                    tasks.append(self._run_validator(agent, node, query, input_text))

            outputs = await asyncio.gather(*tasks)

            for node_id, output in outputs:
                results[node_id] = output
                self.execution_tree[node_id] = {
                    "deps": pending[node_id].deps,
                    "output": output,
                }
                del pending[node_id]

        final_node_id = next(n.id for n in nodes if n.role == "reflector")
        return results[final_node_id], self.execution_tree

    async def _run_worker(self, agent, node: DAGNode, query: str):
        output = await agent.run(query)
        return node.id, output["output"]

    async def _run_reflector(self, agent, node: DAGNode, inputs: List[str]):
        output = await agent.run(inputs)
        return node.id, output

    async def _run_validator(self, agent, node: DAGNode, query: str, input_text: str):
        output = await agent.run(query, input_text)
        return node.id, output
