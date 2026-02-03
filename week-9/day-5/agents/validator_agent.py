import json
from autogen_agentchat.agents import AssistantAgent
from pydantic import ValidationError
from utils.models import ValidationResult
from utils.agent_runner import run_agent
from utils.logger import get_logger
from utils.memory import get_memory_system
from config import config

class ValidatorAgent:
    def __init__(self, model_client):
        self.model_client = model_client
        self.logger = get_logger()
        self.memory = get_memory_system()
        agent_config = config.get_agent_config("validator")        
        self.agent = AssistantAgent(
            name=agent_config["name"],
            system_message=agent_config["system_message"],
            model_client=model_client
        )
    
    async def validate(
        self, 
        content: str, 
        requirements: str = ""
    ) -> ValidationResult:
        self.logger.info(
            "Validating content",
            agent="validator",
            details={"content_length": len(content)}
        )
        
        prompt = f"""
Validate the following content:
Content:
{content}
{f"Requirements: {requirements}" if requirements else ""}
Return ONLY JSON format:
{{
  "verdict": "PASS" or "FAIL",
  "score": 0.85,
  "reason": "detailed explanation",
  "issues": ["issue1", "issue2"],
  "suggestions": ["suggestion1", "suggestion2"]
}}
Be thorough and specific.
"""
        reply = await run_agent(self.agent, prompt)
        json_str = reply.strip()
        if json_str.startswith("```"):
            json_str = json_str.strip("`").strip()
            if json_str.lower().startswith("json"):
                json_str = json_str[4:].strip()
        start = json_str.find("{")
        end = json_str.rfind("}")
        if start != -1 and end != -1:
            json_str = json_str[start:end + 1]
        try:
            data = json.loads(json_str)
            result = ValidationResult(**data)            
            self.memory.add_memory(
                content=f"Validation: {result.verdict} (score: {result.score})",
                memory_type="feedback",
                relevance_score=result.score,
                metadata={
                    "verdict": result.verdict,
                    "score": result.score
                }
            )
            self.logger.info(
                f"Validation completed: {result.verdict}",
                agent="validator",
                details={
                    "verdict": result.verdict,
                    "score": result.score
                }
            )
            
            return result
            
        except (json.JSONDecodeError, ValidationError) as e:
            self.logger.error(
                f"Validation output parse error: {e}",
                agent="validator",
                details={"raw_output": reply[:200]}
            )
            raise ValueError(f"Invalid validator output:\n{e}\n\nRaw:\n{reply}")
    
    async def check_completeness(self, content: str, checklist: list) -> str:
        self.logger.info(
            "Checking completeness",
            agent="validator",
            details={"checklist_items": len(checklist)}
        )        
        checklist_text = "\n".join(f"- {item}" for item in checklist)
        prompt = f"""
Check if the following content satisfies all items in the checklist:
Checklist:
{checklist_text}
Content:
{content}
For each item, indicate:
- Present and complete
- Partially present
- Missing
Provide summary and recommendations.
"""
        result = await run_agent(self.agent, prompt)
        return result
    
    async def verify_accuracy(self, content: str, reference: str = "") -> str:
        self.logger.info(
            "Verifying accuracy",
            agent="validator"
        )
        prompt = f"""
Verify the accuracy of the following content:
Content:
{content}
{f"Reference: {reference}" if reference else ""}
Check for:
1. Factual correctness
2. Logical consistency
3. Completeness
4. Potential errors or inaccuracies
Provide detailed findings.
"""
        
        result = await run_agent(self.agent, prompt)
        return result


def create_validator_agent(model_client) -> ValidatorAgent:
    return ValidatorAgent(model_client)