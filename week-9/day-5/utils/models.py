from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"
    RETRYING = "RETRYING"

class AgentRole(str, Enum):
    ORCHESTRATOR = "orchestrator"
    PLANNER = "planner"
    RESEARCHER = "researcher"
    CODER = "coder"
    ANALYST = "analyst"
    CRITIC = "critic"
    OPTIMIZER = "optimizer"
    VALIDATOR = "validator"
    REPORTER = "reporter"

class TaskModel(BaseModel):
    id: str = Field(..., pattern=r"task_\d+")
    description: str
    deps: List[str] = Field(default_factory=list)
    agent: str = Field(default="worker")
    priority: int = Field(default=5, ge=1, le=10)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class PlanModel(BaseModel):
    tasks: List[TaskModel]
    total_tasks: Optional[int] = None
    estimated_duration: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.total_tasks is None:
            self.total_tasks = len(self.tasks)

class ValidationResult(BaseModel):
    verdict: str  # "PASS" or "FAIL"
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    reason: str
    issues: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)

class CriticalEvaluation(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    risk_assessment: str
    overall_score: float = Field(ge=0.0, le=10.0)

class TaskResult(BaseModel):
    task_id: str
    status: TaskStatus
    output: str
    agent: str
    execution_time: float
    timestamp: datetime = Field(default_factory=datetime.now)
    error: Optional[str] = None
    retry_count: int = 0

class ExecutionLog(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    agent: str
    task_id: Optional[str] = None
    event: str
    details: Dict[str, Any] = Field(default_factory=dict)
    level: str = "INFO"

class MemoryEntry(BaseModel):
    id: str
    content: str
    type: str
    relevance_score: float = Field(default=1.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)
    accessed_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentState(BaseModel):
    name: str
    role: AgentRole
    status: str = "idle" 
    current_task: Optional[str] = None
    tasks_completed: int = 0
    success_rate: float = 1.0
    last_activity: datetime = Field(default_factory=datetime.now)

class SystemState(BaseModel):
    query: str
    plan: Optional[PlanModel] = None
    agent_states: Dict[str, AgentState] = Field(default_factory=dict)
    task_results: Dict[str, TaskResult] = Field(default_factory=dict)
    execution_logs: List[ExecutionLog] = Field(default_factory=list)
    memory: List[MemoryEntry] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    final_output: Optional[str] = None
    validation_result: Optional[ValidationResult] = None

class OptimizationSuggestion(BaseModel):
    target: str 
    current_state: str
    proposed_change: str
    expected_improvement: str
    impact_score: float = Field(ge=0.0, le=10.0)
    implementation_difficulty: str 

class ResearchFindings(BaseModel):
    query: str
    sources: List[Dict[str, str]] 
    key_findings: List[str]
    summary: str
    confidence_score: float = Field(ge=0.0, le=1.0)

class CodeArtifact(BaseModel):
    language: str
    code: str
    description: str
    dependencies: List[str] = Field(default_factory=list)
    tests: Optional[str] = None
    documentation: Optional[str] = None
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)

class AnalysisReport(BaseModel):
    data_summary: str
    key_insights: List[str]
    patterns: List[str]
    trends: List[str]
    recommendations: List[str]
    confidence_level: str
    visualizations: List[str] = Field(default_factory=list)

class FinalReport(BaseModel):
    executive_summary: str
    key_findings: List[str]
    detailed_analysis: str
    recommendations: List[str]
    conclusions: str
    appendices: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)