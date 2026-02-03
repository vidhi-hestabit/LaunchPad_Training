from autogen_agentchat.agents import AssistantAgent
from utils.agent_runner import run_agent
from utils.logger import get_logger
from utils.memory import get_memory_system
from utils.models import AnalysisReport
from config import config

class AnalystAgent:
    def __init__(self, model_client):
        self.model_client = model_client
        self.logger = get_logger()
        self.memory = get_memory_system()
        agent_config = config.get_agent_config("analyst")
        
        self.agent = AssistantAgent(name=agent_config["name"],system_message=agent_config["system_message"],
            model_client=model_client)
    
    async def analyze_data(self, data: str, analysis_type: str = "general"):
        self.logger.info(f"Analyzing data: {analysis_type}",agent="analyst",details={"analysis_type": analysis_type})
        
        prompt = f"""
Perform {analysis_type} analysis on the following data:

Data:
{data}
Provide:
1. Data summary and overview
2. Key patterns identified
3. Notable trends
4. Statistical insights
5. Actionable recommendations
6. Confidence levels
7. Visualization recommendations

Format as a structured analysis report.
"""
        result = await run_agent(self.agent, prompt)
        self.memory.add_memory(content=f"Analysis completed: {analysis_type}",memory_type="result",
            metadata={
                "analysis_type": analysis_type,
                "data_length": len(data)
            }
        )
        
        self.logger.info("Analysis completed",agent="analyst",details={"analysis_type": analysis_type})
        return result
    
    async def find_patterns(self, data: str):
        self.logger.info("Identifying patterns", agent="analyst")
        
        prompt = f"""
Identify patterns and correlations in the following data:
Data:
{data}
Focus on:
1. Recurring patterns
2. Anomalies
3. Correlations
4. Trends over time
5. Causal relationships

Provide detailed findings with confidence scores.
"""
        
        result = await run_agent(self.agent, prompt)
        return result
    
    async def compare_datasets(self, dataset1: str, dataset2: str) -> str:
        self.logger.info(
            "Comparing datasets",
            agent="analyst"
        )
        
        prompt = f"""
Compare and contrast the following datasets:

Dataset 1:
{dataset1}

Dataset 2:
{dataset2}

Provide:
1. Similarities
2. Differences
3. Relative strengths/weaknesses
4. Key takeaways
5. Recommendations
"""
        
        result = await run_agent(self.agent, prompt)
        
        return result
    
    async def predict_trends(self, historical_data: str) -> str:
        self.logger.info(
            "Predicting trends",
            agent="analyst"
        )
        
        prompt = f"""
Based on the following historical data, predict future trends:

Historical Data:
{historical_data}

Provide:
1. Identified trends
2. Predictions with timeframes
3. Confidence levels
4. Supporting evidence
5. Risk factors
6. Alternative scenarios
"""
        
        result = await run_agent(self.agent, prompt)
        
        return result


def create_analyst_agent(model_client) -> AnalystAgent:
    return AnalystAgent(model_client)