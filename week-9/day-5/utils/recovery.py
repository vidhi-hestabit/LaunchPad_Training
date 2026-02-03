import asyncio
from typing import Callable, Any, Optional, Dict
from functools import wraps
from datetime import datetime
from utils.models import TaskStatus
from utils.logger import get_logger


class FailureRecoverySystem:    
    def __init__(self, max_retries: int = 3, retry_delay: float = 2.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = get_logger()
        self.failure_history: Dict[str, list] = {}
    
    async def execute_with_retry(
        self,
        func: Callable,
        *args,
        task_id: Optional[str] = None,
        agent: str = "unknown",
        **kwargs
    ) -> Any:
        retries = 0
        last_error = None
        
        while retries <= self.max_retries:
            try:
                if retries > 0:
                    self.logger.warning(
                        f"Retry attempt {retries}/{self.max_retries}",
                        agent=agent,
                        task_id=task_id
                    )
                    await asyncio.sleep(self.retry_delay * retries)
                
                result = await func(*args, **kwargs)
                
                if task_id and task_id in self.failure_history:
                    del self.failure_history[task_id]
                
                return result
                
            except Exception as e:
                last_error = e
                retries += 1
                
                if task_id:
                    if task_id not in self.failure_history:
                        self.failure_history[task_id] = []
                    self.failure_history[task_id].append({
                        "error": str(e),
                        "timestamp": datetime.now(),
                        "retry_count": retries
                    })
                
                self.logger.error(
                    f"Execution failed: {str(e)}",
                    agent=agent,
                    task_id=task_id,
                    details={"retry_count": retries, "error_type": type(e).__name__}
                )
                
                if retries > self.max_retries:
                    break
                
        self.logger.error(
            f"Max retries exceeded. Final error: {str(last_error)}",
            agent=agent,
            task_id=task_id
        )
        
        raise Exception(f"Failed after {self.max_retries} retries: {str(last_error)}")
    
    def with_retry(self, agent: str = "unknown", task_id: Optional[str] = None):
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                return await self.execute_with_retry(
                    func, *args, 
                    agent=agent, 
                    task_id=task_id,
                    **kwargs
                )
            return wrapper
        return decorator
    
    async def execute_with_fallback(
        self,
        primary_func: Callable,
        fallback_func: Callable,
        *args,
        agent: str = "unknown",
        task_id: Optional[str] = None,
        **kwargs
    ) -> Any:
        try:
            return await self.execute_with_retry(
                primary_func, *args,
                agent=agent,
                task_id=task_id,
                **kwargs
            )
        except Exception as e:
            self.logger.warning(
                f"Primary function failed, using fallback: {str(e)}",
                agent=agent,
                task_id=task_id
            )
            
            try:
                return await fallback_func(*args, **kwargs)
            except Exception as fallback_error:
                self.logger.error(
                    f"Fallback also failed: {str(fallback_error)}",
                    agent=agent,
                    task_id=task_id
                )
                raise
    
    def get_failure_stats(self) -> Dict[str, Any]:
        total_failures = sum(len(failures) for failures in self.failure_history.values())
        
        return {
            "total_failures": total_failures,
            "failed_tasks": len(self.failure_history),
            "tasks_with_failures": list(self.failure_history.keys())
        }
    
    def clear_history(self):
        self.failure_history.clear()


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.logger = get_logger()
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == "OPEN":
            # Check if timeout has passed
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                if elapsed > self.timeout:
                    self.logger.info("Circuit breaker entering HALF_OPEN state")
                    self.state = "HALF_OPEN"
                else:
                    raise Exception(f"Circuit breaker OPEN. Try again in {self.timeout - elapsed:.1f}s")
        
        try:
            result = await func(*args, **kwargs)
            
            if self.state == "HALF_OPEN":
                self.logger.info("Circuit breaker closing after successful call")
                self.state = "CLOSED"
                self.failure_count = 0
            
            return result
            
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.failure_count >= self.failure_threshold:
                self.logger.warning(
                    f"Circuit breaker OPENING after {self.failure_count} failures"
                )
                self.state = "OPEN"
            
            raise


_global_recovery = None

def get_recovery_system(max_retries: int = 3, retry_delay: float = 2.0) -> FailureRecoverySystem:
    global _global_recovery
    
    if _global_recovery is None:
        _global_recovery = FailureRecoverySystem(
            max_retries=max_retries,
            retry_delay=retry_delay
        )
    
    return _global_recovery