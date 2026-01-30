import asyncio
import os
from orchestrator.planner import create_planner_agent, plan_tasks
from agents.worker_agent import run_workers_parallel
from agents.reflector_agent import create_reflection_agent, reflect_answer
from agents.validator_agent import create_validator_agent, validate_answer
from utils.dag import init_task_status, get_ready_tasks
from utils.models import TaskStatus
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()
model_client = OpenAIChatCompletionClient(
    model="llama-3.3-70b-versatile",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    model_info={
        "vision": True,
        "function_calling": True,
        "json_output": True,
        "family": "llama-3.3",
        "structured_output": True,
    }
)


async def run_pipeline(query: str, logger=None):
    planner_agent = create_planner_agent(model_client)
    reflection_agent = create_reflection_agent(model_client)
    validator_agent = create_validator_agent(model_client)

    plan = await plan_tasks(planner_agent, query)

    task_status = init_task_status(plan)
    task_results = {}

    if logger:
        logger("Plan created")

    while len(task_results) < len(plan.tasks):
        ready_tasks = get_ready_tasks(plan, task_status)

        for t in ready_tasks:
            task_status[t.id] = TaskStatus.RUNNING
            if logger:
                logger(f"Running task: {t.description}")

        results = await run_workers_parallel(ready_tasks, model_client)

        for task_id, output in results.items():
            task_status[task_id] = TaskStatus.DONE
            task_results[task_id] = output
            if logger:
                logger(f"Task {task_id} completed")

    merged_output = "\n\n".join(task_results[t.id] for t in plan.tasks)

    improved = await reflect_answer(reflection_agent, merged_output)
    verdict = await validate_answer(validator_agent, improved)

    return {
        "answer": improved,
        "verdict": verdict.verdict,
        "reason": verdict.reason
    }
