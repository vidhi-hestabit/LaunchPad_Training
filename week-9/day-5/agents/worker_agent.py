import asyncio
from autogen_agentchat.agents import AssistantAgent
from utils.agent_runner import run_agent
from utils.logger import get_logger
from utils.recovery import get_recovery_system
from config import config

def create_worker_agent(name: str, model_client):
    return AssistantAgent(
        name=name,
        system_message="You execute assigned tasks accurately and efficiently.",
        model_client=model_client,
    )

async def _run_single_worker(task, model_client):
    logger = get_logger()
    recovery = get_recovery_system()
    logger.trace_task_start(task.id, "worker", task.description)
    start_time = asyncio.get_event_loop().time()
    try:
        agent = create_worker_agent(task.id, model_client)
        reply = await recovery.execute_with_retry(
            run_agent,
            agent,
            task.description,
            task_id=task.id,
            agent="worker"
        )
        execution_time = asyncio.get_event_loop().time() - start_time
        logger.trace_task_complete(task.id, "worker", execution_time, success=True)
        return task.id, reply
        
    except Exception as e:
        execution_time = asyncio.get_event_loop().time() - start_time
        logger.trace_task_complete(task.id, "worker", execution_time, success=False)
        logger.error(f"Worker task failed: {str(e)}",agent="worker",task_id=task.id)
        raise

async def run_workers_parallel(tasks, model_client):
    logger = get_logger()
    logger.info(f"Running {len(tasks)} tasks in parallel", agent="worker",details={"task_count": len(tasks)})
    coros = [_run_single_worker(t, model_client) for t in tasks]
    results = await asyncio.gather(*coros, return_exceptions=True)
    task_results = {}
    for result in results:
        if isinstance(result, Exception):
            logger.error(f"Parallel task execution error: {str(result)}", agent="worker")
            continue
        
        task_id, output = result
        task_results[task_id] = output
    logger.info(
        f"Completed {len(task_results)}/{len(tasks)} tasks successfully",
        agent="worker",
        details={
            "successful": len(task_results),
            "total": len(tasks)
        }
    )    
    return task_results