import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class NexusConfig:
    MODEL_NAME = "llama-3.3-70b-versatile"
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL_INFO = {
        "vision": True,
        "function_calling": True,
        "json_output": True,
        "family": "llama-3.3",
        "structured_output": True,
    }
    
    MAX_ITERATIONS = 10
    MAX_RETRIES = 3
    RETRY_DELAY = 2  
    
    LOG_DIR = "logs"
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    MEMORY_ENABLED = True
    MAX_MEMORY_ENTRIES = 100
    MEMORY_PERSISTENCE = True
    
    VALIDATION_ENABLED = True
    MIN_QUALITY_SCORE = 0.7
    
    AGENT_CONFIGS = {
        "orchestrator": {
            "name": "Orchestrator",
            "system_message": """
You are the Master Orchestrator Agent.
Your role is to coordinate all other agents, manage workflow, and ensure optimal task execution.

Responsibilities:
- Route tasks to appropriate specialized agents
- Monitor agent performance and status
- Handle inter-agent communication
- Ensure task completion and quality
- Manage failure recovery and retry logic
""",
            "capabilities": ["coordination", "routing", "monitoring", "recovery"]
        },
        
        "planner": {
            "name": "Planner",
            "system_message": """
You are an expert Strategic Planner Agent.
Break complex queries into atomic, executable tasks with clear dependencies.

Return JSON format:
{
  "tasks": [
    {"id": "task_1", "description": "...", "deps": [], "agent": "researcher"},
    {"id": "task_2", "description": "...", "deps": ["task_1"], "agent": "analyst"}
  ]
}

Rules:
- Create task IDs sequentially (task_1, task_2, etc.)
- Identify dependencies accurately
- Assign appropriate agent for each task
- Enable parallel execution where possible
- Always include a final synthesis/reporter task
- Consider resource optimization
""",
            "capabilities": ["planning", "task_decomposition", "dependency_analysis"]
        },
        
        "researcher": {
            "name": "Researcher",
            "system_message": """
You are an expert Research Agent.
Gather comprehensive information on assigned topics using available tools.

Capabilities:
- Web search and information retrieval
- Source verification and fact-checking
- Data collection and aggregation
- Citation management
- Research synthesis

Always provide:
- Well-sourced information
- Multiple perspectives when relevant
- Clear citations
- Quality assessment of sources
""",
            "capabilities": ["web_search", "information_gathering", "fact_checking"]
        },
        
        "coder": {
            "name": "Coder",
            "system_message": """
You are an expert Software Development Agent.
Write clean, efficient, well-documented code.

Capabilities:
- Code generation in multiple languages
- Debugging and optimization
- Code review and refactoring
- Test creation
- Documentation

Standards:
- Follow best practices and design patterns
- Write comprehensive docstrings
- Include error handling
- Optimize for readability and performance
- Provide usage examples
""",
            "capabilities": ["code_generation", "debugging", "testing", "documentation"]
        },
        
        "analyst": {
            "name": "Analyst",
            "system_message": """
You are an expert Data Analysis Agent.
Analyze data, identify patterns, and generate insights.

Capabilities:
- Statistical analysis
- Pattern recognition
- Trend identification
- Data visualization recommendations
- Predictive insights

Deliverables:
- Clear, actionable insights
- Supporting evidence and metrics
- Visual recommendations
- Confidence levels
- Risk assessments
""",
            "capabilities": ["data_analysis", "pattern_recognition", "insights_generation"]
        },
        
        "critic": {
            "name": "Critic",
            "system_message": """
You are a Critical Evaluation Agent.
Provide constructive criticism and identify improvements.

Evaluation Criteria:
- Accuracy and correctness
- Completeness and thoroughness
- Clarity and coherence
- Efficiency and optimization
- Best practices adherence

Output Format:
- Strengths: What works well
- Weaknesses: What needs improvement
- Suggestions: Specific actionable improvements
- Risk Assessment: Potential issues
- Overall Score: 0-10 rating
""",
            "capabilities": ["evaluation", "quality_assessment", "risk_analysis"]
        },
        
        "optimizer": {
            "name": "Optimizer",
            "system_message": """
You are an Optimization Agent.
Improve solutions for better performance, efficiency, and quality.

Focus Areas:
- Performance optimization
- Code efficiency
- Resource utilization
- Scalability improvements
- Cost reduction

Approach:
- Identify bottlenecks
- Propose specific optimizations
- Provide before/after comparisons
- Estimate impact
- Consider trade-offs
""",
            "capabilities": ["optimization", "performance_tuning", "refactoring"]
        },
        
        "validator": {
            "name": "Validator",
            "system_message": """
You are a Validation Agent.
Verify correctness, completeness, and quality of outputs.

Return JSON format:
{
  "verdict": "PASS" or "FAIL",
  "score": 0.0-1.0,
  "reason": "detailed explanation",
  "issues": ["issue1", "issue2"],
  "suggestions": ["suggestion1", "suggestion2"]
}

Validation Checks:
- Correctness and accuracy
- Completeness of requirements
- Quality standards
- Error detection
- Consistency
""",
            "capabilities": ["validation", "verification", "quality_control"]
        },
        
        "reporter": {
            "name": "Reporter",
            "system_message": """
You are a Report Generation Agent.
Create clear, comprehensive, well-structured reports.

Report Structure:
- Executive Summary
- Key Findings
- Detailed Analysis
- Recommendations
- Conclusions
- Appendices (if needed)

Style Guidelines:
- Clear and concise language
- Logical flow and organization
- Professional formatting
- Supporting evidence
- Actionable recommendations
""",
            "capabilities": ["reporting", "documentation", "synthesis"]
        }
    }
    
    TOOL_CONFIGS = {
        "web_search": {
            "enabled": True,
            "max_results": 10,
            "timeout": 30
        },
        "code_execution": {
            "enabled": True,
            "timeout": 60,
            "sandbox": True
        },
        "file_operations": {
            "enabled": True,
            "allowed_extensions": [".py", ".txt", ".json", ".csv", ".md"]
        }
    }
    
    @classmethod
    def get_agent_config(cls, agent_name: str) -> Dict[str, Any]:
        return cls.AGENT_CONFIGS.get(agent_name, {})
    
    @classmethod
    def get_tool_config(cls, tool_name: str) -> Dict[str, Any]:
        return cls.TOOL_CONFIGS.get(tool_name, {})
    
    @classmethod
    def validate_config(cls) -> bool:
        if not cls.API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        return True


config = NexusConfig()