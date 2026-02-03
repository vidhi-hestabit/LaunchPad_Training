import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List
from utils.models import ExecutionLog

class NexusLogger:
    def __init__(self, name: str = "NexusAI", log_dir: str = "logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.execution_logs: List[ExecutionLog] = []
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"nexus_{timestamp}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        
        json_log_file = self.log_dir / f"nexus_{timestamp}.json"
        self.json_handler = logging.FileHandler(json_log_file)
        self.json_handler.setLevel(logging.DEBUG)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(self.json_handler)
    
    def log(self,message: str,level: str = "INFO",agent: str = "system",task_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None):
        log_entry = ExecutionLog(
            agent=agent,
            task_id=task_id,
            event=message,
            details=details or {},
            level=level
        )
        self.execution_logs.append(log_entry)
        json_data = log_entry.model_dump(mode='json')
        self.json_handler.stream.write(json.dumps(json_data, default=str) + "\n")
        self.json_handler.flush()
        
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(f"[{agent}] {message}")
    
    def info(self, message: str, **kwargs):
        self.log(message, level="INFO", **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.log(message, level="WARNING", **kwargs)
    
    def error(self, message: str, **kwargs):
        self.log(message, level="ERROR", **kwargs)
    
    def debug(self, message: str, **kwargs):
        self.log(message, level="DEBUG", **kwargs)
    
    def trace_task_start(self, task_id: str, agent: str, description: str):
        self.log(
            f"Task started: {description}",
            level="INFO",
            agent=agent,
            task_id=task_id,
            details={"event_type": "task_start", "description": description}
        )
    
    def trace_task_complete(self,task_id: str, agent: str, execution_time: float, success: bool = True):
        status = "success" if success else "failure"
        self.log(
            f"Task completed: {status} in {execution_time:.2f}s",
            level="INFO" if success else "ERROR",
            agent=agent,
            task_id=task_id,
            details={"event_type": "task_complete","execution_time": execution_time,"success": success}
        )
    
    def trace_agent_action(
        self, 
        agent: str, 
        action: str, 
        details: Optional[Dict[str, Any]] = None
    ):
        self.log(f"Agent action: {action}",level="INFO",agent=agent,details={"event_type": "agent_action", "action": action, **(details or {})})
    
    def get_execution_timeline(self) -> List[Dict[str, Any]]:
        return [log.model_dump(mode='json') for log in self.execution_logs]
    
    def get_agent_activity(self, agent: str) -> List[ExecutionLog]:
        return [log for log in self.execution_logs if log.agent == agent]
    
    def get_task_logs(self, task_id: str) -> List[ExecutionLog]:
        return [log for log in self.execution_logs if log.task_id == task_id]
    
    def generate_summary_report(self) -> str:
        total_logs = len(self.execution_logs)
        level_counts = {}
        agent_counts = {}
        
        for log in self.execution_logs:
            level_counts[log.level] = level_counts.get(log.level, 0) + 1
            agent_counts[log.agent] = agent_counts.get(log.agent, 0) + 1
        report = ["Execution Summary ",f"Total Events: {total_logs}","","Events by Level:"]
        
        for level, count in sorted(level_counts.items()):
            report.append(f"  {level}: {count}")
        
        report.extend([
            "","Events by Agent:"
        ])
        
        for agent, count in sorted(agent_counts.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {agent}: {count}")
        return "\n".join(report)
    
    def save_summary(self, filename: Optional[str] = None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_{timestamp}.txt"
        
        summary_path = self.log_dir / filename
        
        with open(summary_path, 'w') as f:
            f.write(self.generate_summary_report())
            f.write("\n\n Detailed Timeline\n\n")
            for log in self.execution_logs:
                f.write(f"{log.timestamp} - [{log.agent}] {log.event}\n")
        
        return summary_path

_global_logger = None

def get_logger(name: str = "NexusAI", log_dir: str = "logs") -> NexusLogger:
    global _global_logger
    
    if _global_logger is None:
        _global_logger = NexusLogger(name, log_dir)
    
    return _global_logger