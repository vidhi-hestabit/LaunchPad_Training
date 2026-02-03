from autogen_agentchat.agents import AssistantAgent
from utils.agent_runner import run_agent
from utils.logger import get_logger
from utils.memory import get_memory_system
from utils.models import FinalReport
from config import config

class ReporterAgent:
    def __init__(self, model_client):
        self.model_client = model_client
        self.logger = get_logger()
        self.memory = get_memory_system()
        agent_config = config.get_agent_config("reporter")
        self.agent = AssistantAgent(
            name=agent_config["name"],
            system_message=agent_config["system_message"],
            model_client=model_client
        )
    
    async def generate_report(self, query: str, findings: str, include_context: bool = True):
        self.logger.info(
            "Generating final report",
            agent="reporter",
            details={"query": query[:100]}
        )        
        # Get context from memory if requested
        context = ""
        if include_context:
            context = self.memory.get_context_summary(limit=5)
        
        prompt = f"""
Create a comprehensive, professional report based on the following:
Original Query:
{query}
Findings and Results:
{findings}
{f"Additional Context:\n{context}" if context else ""}
Structure your report with:
# Executive Summary
Brief overview of key findings and recommendations
# Key Findings
Main discoveries and insights
# Detailed Analysis  
In-depth examination of results
# Recommendations
Actionable next steps and suggestions
# Conclusions
Summary and final thoughts
Use clear, professional language. Be thorough but concise.
"""
        
        result = await run_agent(self.agent, prompt)
        
        # Store report in memory
        self.memory.add_memory(
            content=f"Final report generated for: {query[:100]}",
            memory_type="result",
            metadata={"query": query, "report_length": len(result)}
        )
        
        self.logger.info("Report generation completed",agent="reporter",details={"report_length": len(result)})
        
        return result
    
    async def synthesize_findings(self, multiple_findings: list) -> str:
        self.logger.info(
            f"Synthesizing {len(multiple_findings)} findings",
            agent="reporter"
        )
        
        findings_text = "\n\n---\n\n".join(
            f"Finding {i+1}:\n{finding}" 
            for i, finding in enumerate(multiple_findings)
        )
        
        prompt = f"""
Synthesize the following findings into a coherent, comprehensive narrative:

{findings_text}

Create a unified analysis that:
1. Integrates all findings
2. Identifies common themes
3. Resolves any contradictions
4. Highlights key insights
5. Provides clear conclusions

Format as a well-structured synthesis.
"""
        
        result = await run_agent(self.agent, prompt)
        
        return result
    
    async def create_executive_summary(self, full_report: str) -> str:
        self.logger.info("Creating executive summary",agent="reporter")
        
        prompt = f"""
Create a concise executive summary of the following report:

{full_report}

The summary should:
1. Be 3-5 paragraphs maximum
2. Highlight key findings
3. Include main recommendations
4. Be suitable for decision-makers
5. Use clear, direct language

Focus on actionable insights.
"""
        
        result = await run_agent(self.agent, prompt)
        return result

def create_reporter_agent(model_client) -> ReporterAgent:
    return ReporterAgent(model_client)