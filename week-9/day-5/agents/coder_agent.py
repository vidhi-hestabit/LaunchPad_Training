from autogen_agentchat.agents import AssistantAgent
from utils.agent_runner import run_agent
from utils.logger import get_logger
from utils.memory import get_memory_system
from utils.models import CodeArtifact
from config import config

class CoderAgent:
    def __init__(self, model_client):
        self.model_client = model_client
        self.logger = get_logger()
        self.memory = get_memory_system()
        
        agent_config = config.get_agent_config("coder")
        self.agent = AssistantAgent(
            name=agent_config["name"],
            system_message=agent_config["system_message"],
            model_client=model_client
        )
    
    async def generate_code(self, requirements: str, language: str = "python"):
        self.logger.info(f"Generating {language} code",agent="coder",details={"language": language})
        
        prompt = f"""
Generate clean, well-documented {language} code for the following requirements:

Requirements:
{requirements}

Provide:
1. Complete, working code
2. Comprehensive docstrings/comments
3. Error handling
4. Usage examples
5. Any necessary dependencies

Format as markdown code blocks.
"""

        result = await run_agent(self.agent, prompt)
        
        # Store in memory
        self.memory.add_memory(
            content=f"Generated {language} code for: {requirements[:100]}",
            memory_type="result",
            metadata={"language": language, "code_length": len(result)}
        )
        
        self.logger.info(
            "Code generation completed",
            agent="coder",
            details={"language": language, "result_length": len(result)}
        )
        return result
    
    async def debug_code(self, code: str, error: str):
        self.logger.info("Debugging code",agent="coder",details={"error": error[:100]})
        
        prompt = f"""
Debug the following code and fix the error:

Code:
{code}

Error:
{error}

Provide:
1. Explanation of the issue
2. Fixed code
3. Explanation of the fix
4. Suggestions to prevent similar issues
"""
        
        result = await run_agent(self.agent, prompt)
        
        return result
    
    async def optimize_code(self, code: str):
        self.logger.info(
            "Optimizing code",
            agent="coder"
        )
        
        prompt = f"""
Optimize the following code for better performance and readability:

Code:
{code}

Provide:
1. Optimized version
2. Explanation of improvements
3. Performance impact analysis
4. Best practices applied
"""
        
        result = await run_agent(self.agent, prompt)
        
        return result
    
    async def write_tests(self, code: str):
        self.logger.info(
            "Writing tests",
            agent="coder"
        )
        
        prompt = f"""
Write comprehensive tests for the following code:

Code:
{code}

Provide:
1. Unit tests
2. Edge cases
3. Test documentation
4. Coverage information
"""
        
        result = await run_agent(self.agent, prompt)
        
        return result


def create_coder_agent(model_client) -> CoderAgent:
    return CoderAgent(model_client)