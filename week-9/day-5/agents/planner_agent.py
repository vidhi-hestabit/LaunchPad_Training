import json
from autogen_agentchat.agents import AssistantAgent
from utils.models import PlanModel, TaskModel
from utils.agent_runner import run_agent
from utils.logger import get_logger
from utils.memory import get_memory_system
from config import config

class PlannerAgent:
    def __init__(self, model_client):
        self.model_client = model_client
        self.logger = get_logger()
        self.memory = get_memory_system()
        agent_config = config.get_agent_config("planner")
        
        self.agent = AssistantAgent(
            name=agent_config["name"],
            system_message=agent_config["system_message"],
            model_client=model_client
        )
    
    async def create_plan(self, query: str) -> PlanModel:
        self.logger.info(
            "Creating execution plan",
            agent="planner",
            details={"query": query[:100]}
        )
        
        context = self.memory.get_context_summary(limit=3)
        
        enhanced_prompt = f"""
Create a detailed execution plan for the following query.

Query: {query}

{context if context else ""}

Remember to:
1. Break down into atomic tasks
2. Assign appropriate agents (researcher, coder, analyst, critic, optimizer, validator, reporter)
3. Define clear dependencies
4. Enable parallel execution where possible
5. Always include a final reporter task to synthesize results

Return ONLY valid JSON.
"""
        
        reply = await run_agent(self.agent, enhanced_prompt)

        if "```" in reply:
            reply = reply.split("```")[1].strip()
            if reply.startswith("json"):
                reply = reply[4:].strip()
        
        start = reply.find("{")
        end = reply.rfind("}")
        
        if start == -1 or end == -1:
            self.logger.error(
                "Planner did not return valid JSON",
                agent="planner",
                details={"response": reply[:200]}
            )
            raise ValueError(f"Planner did not return JSON:\n{reply}")
        
        json_str = reply[start:end + 1]
        data = json.loads(json_str)
        tasks = [TaskModel(**t) for t in data["tasks"]]
        plan = PlanModel(tasks=tasks)
        self.memory.add_memory(
            content=f"Created plan with {len(tasks)} tasks for: {query[:100]}",
            memory_type="procedure",
            metadata={"total_tasks": len(tasks), "query": query}
        )        
        self.logger.info(
            f"Plan created with {len(tasks)} tasks",
            agent="planner",
            details={"task_count": len(tasks)}
        )
        return plan


def create_planner_agent(model_client) -> PlannerAgent:
    return PlannerAgent(model_client)