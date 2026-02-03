import json
from autogen_agentchat.agents import AssistantAgent
from utils.agent_runner import run_agent
from utils.logger import get_logger
from utils.memory import get_memory_system
from utils.models import CriticalEvaluation
from config import config

class CriticAgent:
    def __init__(self, model_client):
        self.model_client = model_client
        self.logger = get_logger()
        self.memory = get_memory_system()
        agent_config = config.get_agent_config("critic")
        self.agent = AssistantAgent(name=agent_config["name"],system_message=agent_config["system_message"],
            model_client=model_client)
    
    async def evaluate(self, content: str, context: str = "") -> CriticalEvaluation:
        self.logger.info(
            "Evaluating content",
            agent="critic",
            details={"content_length": len(content)}
        )
        
        prompt = f"""
Critically evaluate the following content:

Content:
{content}

{f"Context: {context}" if context else ""}

Provide evaluation in JSON format:
{{
  "strengths": ["strength1", "strength2", ...],
  "weaknesses": ["weakness1", "weakness2", ...],
  "suggestions": ["suggestion1", "suggestion2", ...],
  "risk_assessment": "detailed risk analysis",
  "overall_score": 8.5
}}

Be constructive and specific.
"""
        
        result = await run_agent(self.agent, prompt)
        
        if "```" in result:
            result = result.split("```")[1].strip()
            if result.startswith("json"):
                result = result[4:].strip()
        
        start = result.find("{")
        end = result.rfind("}")
        
        if start != -1 and end != -1:
            json_str = result[start:end + 1]
            data = json.loads(json_str)
            evaluation = CriticalEvaluation(**data)
            self.memory.add_memory(
                content=f"Evaluation completed with score: {evaluation.overall_score}/10",
                memory_type="feedback",
                relevance_score=evaluation.overall_score / 10,
                metadata={"score": evaluation.overall_score}
            )
            
            self.logger.info(
                f"Evaluation completed: {evaluation.overall_score}/10",
                agent="critic",
                details={"score": evaluation.overall_score}
            )
            
            return evaluation
        else:
            self.logger.warning(
                "Could not parse evaluation JSON, using default",
                agent="critic"
            )
            return CriticalEvaluation(
                strengths=["Evaluation completed"],
                weaknesses=["Could not parse detailed feedback"],
                suggestions=["Review output format"],
                risk_assessment="Unknown",
                overall_score=5.0
            )
    
    async def identify_improvements(self, content: str):
        self.logger.info("Identifying improvements",agent="critic")
        
        prompt = f"""
Review the following content and identify specific improvements:

Content:
{content}

For each improvement, provide:
1. What to improve
2. Why it needs improvement
3. How to improve it
4. Expected impact

Be specific and actionable.
"""
        
        result = await run_agent(self.agent, prompt)
        
        return result
    
    async def assess_quality(self, content: str, criteria: list = None):
        if criteria is None:
            criteria = [
                "Accuracy",
                "Completeness",
                "Clarity",
                "Efficiency",
                "Best Practices"
            ]
        
        self.logger.info(
            "Assessing quality",
            agent="critic",
            details={"criteria_count": len(criteria)}
        )
        
        criteria_text = "\n".join(f"- {c}" for c in criteria)
        
        prompt = f"""
Assess the quality of the following content against these criteria:

{criteria_text}

Content:
{content}

For each criterion, provide:
1. Score (0-10)
2. Justification
3. Specific examples

Include an overall quality score.
"""
        
        result = await run_agent(self.agent, prompt)
        
        return result


def create_critic_agent(model_client) -> CriticAgent:
    return CriticAgent(model_client)