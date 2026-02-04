import os
import asyncio
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from datetime import datetime
from config import config
from agents.orchestrator_agent import create_orchestrator_agent
from agents.planner_agent import create_planner_agent
from agents.researcher_agent import create_researcher_agent
from agents.coder_agent import create_coder_agent
from agents.analyst_agent import create_analyst_agent
from agents.critic_agent import create_critic_agent
from agents.optimizer_agent import create_optimizer_agent
from agents.validator_agent import create_validator_agent
from agents.reporter_agent import create_reporter_agent
from agents.worker_agent import run_workers_parallel
from utils.dag import init_task_status, get_ready_tasks, validate_dag, get_execution_order
from utils.models import TaskStatus, SystemState, AgentState, AgentRole, TaskResult
from utils.logger import get_logger
from utils.memory import get_memory_system
from utils.recovery import get_recovery_system

# Import model client
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

class NexusAI:
    def __init__(self):
        config.validate_config() 
        self.model_client = OpenAIChatCompletionClient(
            model=config.MODEL_NAME,
            base_url=config.BASE_URL,
            api_key=config.API_KEY,
            model_info=config.MODEL_INFO
        ) 
        self.logger = get_logger()
        self.memory = get_memory_system()
        self.recovery = get_recovery_system(
            max_retries=config.MAX_RETRIES,
            retry_delay=config.RETRY_DELAY
        )
        
        # Initialize agents
        self.logger.info("Initializing Nexus AI agents", agent="system")
        
        self.orchestrator = create_orchestrator_agent(self.model_client)
        self.planner = create_planner_agent(self.model_client)
        self.researcher = create_researcher_agent(self.model_client)
        self.coder = create_coder_agent(self.model_client)
        self.analyst = create_analyst_agent(self.model_client)
        self.critic = create_critic_agent(self.model_client)
        self.optimizer = create_optimizer_agent(self.model_client)
        self.validator = create_validator_agent(self.model_client)
        self.reporter = create_reporter_agent(self.model_client) 
        self.orchestrator.register_agent("planner", self.planner)
        self.orchestrator.register_agent("researcher", self.researcher)
        self.orchestrator.register_agent("coder", self.coder)
        self.orchestrator.register_agent("analyst", self.analyst)
        self.orchestrator.register_agent("critic", self.critic)
        self.orchestrator.register_agent("optimizer", self.optimizer)
        self.orchestrator.register_agent("validator", self.validator)
        self.orchestrator.register_agent("reporter", self.reporter)
        
        # Initialize system state
        self.system_state = None
        
        self.logger.info(
            "Nexus AI initialized successfully",
            agent="system",
            details=self.orchestrator.get_system_status()
        )
    
    async def run(
        self, 
        query: str,
        enable_reflection: bool = True,
        enable_optimization: bool = True,
        max_iterations: int = None
    ) -> Dict[str, Any]:
        start_time = datetime.now()
        max_iterations = max_iterations or config.MAX_ITERATIONS
        
        # Initialize system state
        self.system_state = SystemState(query=query)
        
        self.logger.info(
            f"Starting Nexus AI pipeline for query: {query[:100]}...",
            agent="system"
        )
        
        # Store query in memory
        self.memory.add_memory(
            content=f"Processing query: {query}",
            memory_type="fact",
            metadata={"query": query}
        )
        
        try:
            # Step 1: Planning
            self.logger.info("Step 1: Creating execution plan", agent="system")
            plan = await self.planner.create_plan(query)
            self.system_state.plan = plan
            
            # Validate DAG
            if not validate_dag(plan):
                raise ValueError("Invalid task plan: circular dependencies detected")
            
            execution_order = get_execution_order(plan)
            self.logger.info(
                f"Plan validated: {len(plan.tasks)} tasks in {len(execution_order)} batches",
                agent="system",
                details={
                    "total_tasks": len(plan.tasks),
                    "batches": len(execution_order)
                }
            )
            
            # Step 2: Execute tasks with specialized agents
            self.logger.info("Step 2: Executing tasks", agent="system")
            task_status = init_task_status(plan)
            task_results = {}
            
            iteration = 0
            while len(task_results) < len(plan.tasks):
                iteration += 1
                ready_tasks = get_ready_tasks(plan, task_status)
                
                if not ready_tasks:
                    break
                
                self.logger.info(
                    f"Batch {iteration}: {len(ready_tasks)} tasks ready",
                    agent="system"
                )
                
                # Mark tasks as running
                for t in ready_tasks:
                    task_status[t.id] = TaskStatus.RUNNING
                
                # Route tasks to specialized agents or use workers
                batch_results = {}
                for task in ready_tasks:
                    try:
                        # Check if task should use specialized agent
                        if hasattr(task, 'agent') and task.agent != "worker":
                            specialized_agent = self.orchestrator.get_agent(task.agent)
                            if specialized_agent:
                                self.logger.info(
                                    f"Routing {task.id} to {task.agent}",
                                    agent="orchestrator"
                                )
                                
                                # Execute based on agent type
                                if task.agent == "researcher":
                                    result = await specialized_agent.research(task.description)
                                elif task.agent == "coder":
                                    result = await specialized_agent.generate_code(task.description)
                                elif task.agent == "analyst":
                                    result = await specialized_agent.analyze_data(task.description)
                                elif task.agent == "reporter":
                                    # Reporter synthesizes all previous results
                                    findings = "\n\n".join(task_results.values())
                                    result = await specialized_agent.generate_report(query, findings)
                                else:
                                    from utils.agent_runner import run_agent
                                    result = await run_agent(specialized_agent.agent, task.description)
                                
                                batch_results[task.id] = result
                            else:
                                # Fallback to worker
                                worker_results = await run_workers_parallel([task], self.model_client)
                                batch_results.update(worker_results)
                        else:
                            # Use worker pool for generic tasks
                            worker_results = await run_workers_parallel([task], self.model_client)
                            batch_results.update(worker_results)
                    
                    except Exception as e:
                        self.logger.error(
                            f"Task {task.id} failed: {str(e)}",
                            agent="system",
                            task_id=task.id
                        )
                        task_status[task.id] = TaskStatus.FAILED
                        continue
                
                # Update results and status
                for task_id, output in batch_results.items():
                    task_status[task_id] = TaskStatus.DONE
                    task_results[task_id] = output
                    
                    # Store task result
                    self.system_state.task_results[task_id] = TaskResult(
                        task_id=task_id,
                        status=TaskStatus.DONE,
                        output=output,
                        agent="specialized",
                        execution_time=0.0
                    )
            
            # Step 3: Merge results
            self.logger.info("Step 3: Merging results", agent="system")
            merged_output = "\n\n".join(
                f"=== Task {t.id}: {t.description} ===\n{task_results.get(t.id, 'No output')}"
                for t in plan.tasks
                if t.id in task_results
            )
            
            current_output = merged_output
            
            # Step 4: Self-reflection (optional)
            if enable_reflection:
                self.logger.info("Step 4: Self-reflection with Critic", agent="system")
                evaluation = await self.critic.evaluate(current_output, context=query)
                
                self.logger.info(
                    f"Critical evaluation: {evaluation.overall_score}/10",
                    agent="system",
                    details={"score": evaluation.overall_score}
                )
                
                # If score is low, suggest improvements
                if evaluation.overall_score < 7.0:
                    improvements = "\n".join(evaluation.suggestions)
                    current_output = f"{current_output}\n\n=== Suggested Improvements ===\n{improvements}"
            
            # Step 5: Optimization (optional)
            if enable_optimization and enable_reflection:
                self.logger.info("Step 5: Optimization", agent="system")
                optimized_output = await self.optimizer.optimize(
                    current_output,
                    optimization_target="quality and clarity"
                )
                current_output = optimized_output
            
            # Step 6: Final validation
            self.logger.info("Step 6: Final validation", agent="system")
            validation_result = await self.validator.validate(
                current_output,
                requirements=query
            )
            
            self.system_state.validation_result = validation_result
            
            self.logger.info(
                f"Validation result: {validation_result.verdict} (score: {validation_result.score})",
                agent="system",
                details={
                    "verdict": validation_result.verdict,
                    "score": validation_result.score
                }
            )
            
            # Step 7: Generate final report
            self.logger.info("Step 7: Generating final report", agent="system")
            final_report = await self.reporter.generate_report(
                query=query,
                findings=current_output,
                include_context=True
            )
            
            self.system_state.final_output = final_report
            self.system_state.completed_at = datetime.now()
            
            # Calculate execution time
            execution_time = (self.system_state.completed_at - start_time).total_seconds()
            
            # Store final result in memory
            self.memory.add_memory(
                content=f"Query completed successfully: {query[:100]}",
                memory_type="result",
                relevance_score=validation_result.score,
                metadata={
                    "query": query,
                    "score": validation_result.score,
                    "execution_time": execution_time
                }
            )
            
            self.logger.info(
                f"Pipeline completed successfully in {execution_time:.2f}s",
                agent="system",
                details={
                    "execution_time": execution_time,
                    "validation_score": validation_result.score
                }
            )
            
            # Return comprehensive results
            return {
                "answer": final_report,
                "verdict": validation_result.verdict,
                "score": validation_result.score,
                "reason": validation_result.reason,
                "issues": validation_result.issues,
                "suggestions": validation_result.suggestions,
                "execution_time": execution_time,
                "tasks_completed": len(task_results),
                "total_tasks": len(plan.tasks),
                "memory_stats": self.memory.get_statistics(),
                "system_state": self.system_state
            }
            
        except Exception as e:
            self.logger.error(
                f"Pipeline failed: {str(e)}",
                agent="system",
                details={"error": str(e)}
            )
            
            # Store failure in memory
            self.memory.add_memory(
                content=f"Query failed: {query[:100]} - Error: {str(e)}",
                memory_type="feedback",
                relevance_score=0.0,
                metadata={"query": query, "error": str(e)}
            )
            
            raise
    
    def get_system_status(self) -> Dict[str, Any]:
        return {
            "orchestrator_status": self.orchestrator.get_system_status(),
            "memory_stats": self.memory.get_statistics(),
            "recovery_stats": self.recovery.get_failure_stats(),
            "system_state": self.system_state.model_dump() if self.system_state else None
        }
    
    def save_logs(self):
        self.logger.save_summary()
        self.logger.info("Logs saved successfully", agent="system")


# Convenience function for simple usage
async def run_nexus(query: str, **kwargs) -> Dict[str, Any]:
    
    nexus = NexusAI()
    return await nexus.run(query, **kwargs)