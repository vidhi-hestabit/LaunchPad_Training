from autogen_agentchat.agents import AssistantAgent
from utils.agent_runner import run_agent
from utils.logger import get_logger
from utils.memory import get_memory_system
from utils.models import ResearchFindings
from config import config

class ResearcherAgent:
    def __init__(self, model_client):
        self.model_client = model_client
        self.logger = get_logger()
        self.memory = get_memory_system()
        agent_config = config.get_agent_config("researcher")
        self.agent = AssistantAgent(
            name=agent_config["name"],
            system_message=agent_config["system_message"],
            model_client=model_client
        )
    
    async def research(self, topic: str) -> str:
        self.logger.info(
            f"Researching topic: {topic}",
            agent="researcher",
            details={"topic": topic}
        )
        
        prompt = f"""
Research the following topic comprehensively:
Topic: {topic}
Provide:
1. Key information and facts
2. Multiple perspectives if applicable
3. Recent developments
4. Relevant context
5. Source quality assessment
Format your response as a structured research report.
"""
        
        result = await run_agent(self.agent, prompt)
        
        self.memory.add_memory(
            content=f"Research completed on: {topic}",
            memory_type="fact",
            metadata={"topic": topic, "findings_length": len(result)}
        )
        
        self.logger.info(
            "Research completed",
            agent="researcher",
            details={"topic": topic, "result_length": len(result)}
        )
        
        return result
    
    async def fact_check(self, claim: str) -> str:
        self.logger.info(
            f"Fact checking: {claim[:50]}...",
            agent="researcher"
        )
        
        prompt = f"""
Fact-check the following claim:

Claim: {claim}

Provide:
1. Verification status (True/False/Uncertain)
2. Supporting evidence
3. Contradicting evidence
4. Confidence level
5. Sources
"""
        result = await run_agent(self.agent, prompt)
        return result

def create_researcher_agent(model_client) -> ResearcherAgent:
    return ResearcherAgent(model_client)