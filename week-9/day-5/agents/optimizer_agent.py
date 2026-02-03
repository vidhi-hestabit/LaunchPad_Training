from autogen_agentchat.agents import AssistantAgent
from utils.agent_runner import run_agent
from utils.logger import get_logger
from utils.memory import get_memory_system
from utils.models import OptimizationSuggestion
from config import config

class OptimizerAgent:
    def __init__(self, model_client):
        self.model_client = model_client
        self.logger = get_logger()
        self.memory = get_memory_system()
        
        agent_config = config.get_agent_config("optimizer")
        
        self.agent = AssistantAgent(
            name=agent_config["name"],
            system_message=agent_config["system_message"],
            model_client=model_client
        )
    
    async def optimize(self,content: str,optimization_target: str = "performance"):
        self.logger.info(f"Optimizing for: {optimization_target}",agent="optimizer",
            details={"target": optimization_target}
        )
        
        prompt = f"""
Optimize the following content for {optimization_target}:

Content:
{content}

Provide:
1. Optimized version
2. Specific changes made
3. Before/after comparison
4. Expected improvements
5. Trade-offs considered
6. Implementation notes

Be thorough and explain your reasoning.
"""
        
        result = await run_agent(self.agent, prompt)
        
        self.memory.add_memory(content=f"Optimization completed for: {optimization_target}",
            memory_type="result", metadata={"target": optimization_target})
        
        self.logger.info(
            "Optimization completed",
            agent="optimizer",
            details={"target": optimization_target}
        )
        
        return result
    
    async def identify_bottlenecks(self, system_description: str):
        self.logger.info("Identifying bottlenecks",agent="optimizer")
        
        prompt = f"""
Analyze the following system and identify bottlenecks:

System:
{system_description}

For each bottleneck, provide:
1. Description
2. Impact severity (1-10)
3. Root cause
4. Optimization recommendations
5. Implementation difficulty

Prioritize by impact.
"""
        
        result = await run_agent(self.agent, prompt)
        
        return result
    
    async def suggest_improvements(
        self, 
        content: str,
        focus_areas: list = None
    ) -> str:
        if focus_areas is None:
            focus_areas = [
                "Performance",
                "Efficiency", 
                "Scalability",
                "Maintainability",
                "Cost"
            ]
        
        self.logger.info(
            "Suggesting improvements",
            agent="optimizer",
            details={"focus_areas": focus_areas}
        )
        
        focus_text = "\n".join(f"- {area}" for area in focus_areas)
        
        prompt = f"""
Suggest improvements in these areas:

{focus_text}

Content:
{content}

For each improvement:
1. Specific change to make
2. Expected benefit
3. Implementation effort
4. Priority level

Format as actionable recommendations.
"""
        
        result = await run_agent(self.agent, prompt)
        
        return result
    
    async def refactor_for_quality(self, content: str) -> str:
        self.logger.info(
            "Refactoring for quality",
            agent="optimizer"
        )
        
        prompt = f"""
Refactor the following content to improve quality:

Content:
{content}

Focus on:
1. Code/content structure
2. Readability
3. Maintainability
4. Best practices
5. Design patterns

Provide refactored version with explanations.
"""
        
        result = await run_agent(self.agent, prompt)
        
        return result


def create_optimizer_agent(model_client) -> OptimizerAgent:
    return OptimizerAgent(model_client)