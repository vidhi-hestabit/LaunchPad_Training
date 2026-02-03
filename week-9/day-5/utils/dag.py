from typing import Dict, List, Set
from utils.models import TaskStatus, PlanModel, TaskModel


def init_task_status(plan: PlanModel) -> Dict[str, TaskStatus]:
    return {t.id: TaskStatus.PENDING for t in plan.tasks}


def get_ready_tasks(plan: PlanModel, task_status: Dict[str, TaskStatus]) -> List[TaskModel]:
    return [
        t for t in plan.tasks
        if task_status[t.id] == TaskStatus.PENDING
        and all(task_status.get(dep, TaskStatus.PENDING) == TaskStatus.DONE for dep in t.deps)
    ]

def validate_dag(plan: PlanModel) -> bool:
    graph = {task.id: task.deps for task in plan.tasks}
    visited = set()
    rec_stack = set()

    def has_cycle(node: str) -> bool:
        visited.add(node)
        rec_stack.add(node)    
        for dep in graph.get(node, []):
            if dep not in visited:
                if has_cycle(dep):
                    return True
            elif dep in rec_stack:
                return True        
        rec_stack.remove(node)
        return False
    
    for task_id in graph:
        if task_id not in visited:
            if has_cycle(task_id):
                return False    
    return True

def get_execution_order(plan: PlanModel) -> List[List[str]]:
    task_status = init_task_status(plan)
    execution_order = []
    
    while any(status == TaskStatus.PENDING for status in task_status.values()):
        ready = get_ready_tasks(plan, task_status)
        
        if not ready:
            raise ValueError("Circular dependency detected in task plan")
        batch = [task.id for task in ready]
        execution_order.append(batch)
        for task_id in batch:
            task_status[task_id] = TaskStatus.DONE
    return execution_order

def get_critical_path(plan: PlanModel) -> List[str]:
    task_dict = {t.id: t for t in plan.tasks}
    depths = {}
    
    def calculate_depth(task_id: str) -> int:
        if task_id in depths:
            return depths[task_id]
        task = task_dict[task_id]
        if not task.deps:
            depths[task_id] = 0
            return 0        
        max_dep_depth = max(calculate_depth(dep) for dep in task.deps)
        depths[task_id] = max_dep_depth + 1
        return depths[task_id]
    
    for task_id in task_dict:
        calculate_depth(task_id)
    max_depth_task = max(depths, key=depths.get)
    critical_path = [max_depth_task]
    current = max_depth_task
    
    while task_dict[current].deps:
        deps_with_depths = [(dep, depths[dep]) for dep in task_dict[current].deps]
        next_task = max(deps_with_depths, key=lambda x: x[1])[0]
        critical_path.append(next_task)
        current = next_task
    return list(reversed(critical_path))


def estimate_execution_time(plan: PlanModel, avg_task_time: float = 10.0) -> float:
    critical_path = get_critical_path(plan)
    return len(critical_path) * avg_task_time

def get_parallel_efficiency(plan: PlanModel) -> float:
    total_tasks = len(plan.tasks)
    execution_order = get_execution_order(plan)
    actual_depth = len(execution_order)
    efficiency = (total_tasks - actual_depth)/(total_tasks - 1) if total_tasks > 1 else 1.0
    return max(0.0, min(1.0, efficiency))


def optimize_task_order(plan: PlanModel) -> PlanModel:
    task_dict = {t.id: t for t in plan.tasks}    
    depths = {}
    def get_depth(task_id: str) -> int:
        if task_id in depths:
            return depths[task_id]
        task = task_dict[task_id]
        if not task.deps:
            depths[task_id] = 0
            return 0
        depths[task_id] = max(get_depth(dep) for dep in task.deps) + 1
        return depths[task_id]
    
    for task_id in task_dict:
        get_depth(task_id)
    sorted_tasks = sorted(
        plan.tasks,
        key=lambda t: (depths[t.id], -t.priority)
    )
    return PlanModel(tasks=sorted_tasks)