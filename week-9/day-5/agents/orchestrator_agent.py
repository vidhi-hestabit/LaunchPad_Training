from typing import Dict, Any, Optional
from autogen_agentchat.agents import AssistantAgent
from config import config
from utils.logger import get_logger
from utils.memory import get_memory_system
from utils.agent_runner import run_agent

class OrchestratorAgent:    
    def __init__(self, model_client):
        self.model_client = model_client
        self.logger = get_logger()
        self.memory = get_memory_system()
        
        agent_config = config.get_agent_config("orchestrator")
        
        self.agent = AssistantAgent(
            name=agent_config["name"],
            system_message=agent_config["system_message"],
            model_client=model_client
        )
        
        self.agent_registry: Dict[str, Any] = {}
    
    def register_agent(self, role: str, agent: Any):
        self.agent_registry[role] = agent
        self.logger.info(
            f"Registered agent: {role}",
            agent="orchestrator",
            details={"role": role}
        )
    
    def get_agent(self, role: str) -> Optional[Any]:
        return self.agent_registry.get(role)
    
    async def route_task(self, task_description: str, preferred_agent: str) -> str:
        agent = self.get_agent(preferred_agent)
        if not agent:
            self.logger.warning(
                f"Agent not found: {preferred_agent}, using orchestrator",
                agent="orchestrator"
            )
            return await run_agent(self.agent, task_description)
        
        self.logger.info(
            f"Routing task to {preferred_agent}",
            agent="orchestrator",
            details={"target_agent": preferred_agent}
        )
        result = await run_agent(agent, task_description)
        
        self.memory.add_memory(
            content=f"Task routed to {preferred_agent}: {task_description[:100]}...",
            memory_type="procedure",
            metadata={"agent": preferred_agent, "task": task_description}
        )
        
        return result
    
    def get_system_status(self) -> Dict[str, Any]:
        return {
            "registered_agents": list(self.agent_registry.keys()),
            "total_agents": len(self.agent_registry),
            "memory_stats": self.memory.get_statistics()
        }

def create_orchestrator_agent(model_client) -> OrchestratorAgent:
    return OrchestratorAgent(model_client)