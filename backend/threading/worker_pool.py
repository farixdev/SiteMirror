"""
Worker pool for multi-threaded extraction tasks.
Manages a pool of worker threads and distributes tasks.
"""

import threading
import queue
from typing import Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum
import time


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class Task:
    """Represents a task to be executed by a worker."""
    task_id: str
    func: Callable
    args: tuple = ()
    kwargs: dict = None
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Exception = None
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}


class WorkerPool:
    """
    Thread pool manager for extracting tasks.
    """
    
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.task_queue: queue.Queue = queue.Queue()
        self.workers: list = []
        self.tasks_dict: dict = {}
        self.lock = threading.Lock()
        self.running = False
        self.active_count = 0
        self.completed_count = 0
        self.failed_count = 0
        self.request_count = 0
    
    def start(self) -> None:
        """Start the worker pool."""
        if self.running:
            return
        
        self.running = True
        self.active_count = 0
        self.completed_count = 0
        self.failed_count = 0
        
        for i in range(self.num_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                daemon=True,
                name=f"Worker-{i}"
            )
            worker.start()
            self.workers.append(worker)
    
    def stop(self) -> None:
        """Stop the worker pool."""
        self.running = False
        
        # Clear queue
        while not self.task_queue.empty():
            try:
                self.task_queue.get_nowait()
            except queue.Empty:
                pass
    
    def _worker_loop(self) -> None:
        """Main worker loop - processes tasks from queue."""
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
                self._execute_task(task)
            except queue.Empty:
                continue
            except Exception as e:
                pass
    
    def _execute_task(self, task: Task) -> None:
        """Execute a single task."""
        try:
            with self.lock:
                task.status = TaskStatus.RUNNING
                self.active_count += 1
            
            # Execute the task function
            task.result = task.func(*task.args, **task.kwargs)
            
            with self.lock:
                task.status = TaskStatus.COMPLETED
                self.completed_count += 1
                self.active_count = max(0, self.active_count - 1)
        
        except Exception as e:
            with self.lock:
                task.status = TaskStatus.FAILED
                task.error = e
                self.failed_count += 1
                self.active_count = max(0, self.active_count - 1)
    
    def submit_task(self, task_id: str, func: Callable, 
                   args: tuple = (), kwargs: dict = None) -> Task:
        """Submit a task to the pool."""
        task = Task(
            task_id=task_id,
            func=func,
            args=args,
            kwargs=kwargs or {}
        )
        
        with self.lock:
            self.tasks_dict[task_id] = task
            self.request_count += 1
        
        self.task_queue.put(task)
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID."""
        with self.lock:
            return self.tasks_dict.get(task_id)
    
    def get_stats(self) -> dict:
        """Get pool statistics."""
        with self.lock:
            return {
                'active_threads': self.active_count,
                'queue_size': self.task_queue.qsize(),
                'completed': self.completed_count,
                'failed': self.failed_count,
                'total_requests': self.request_count,
                'num_workers': self.num_workers
            }
    
    def wait_all(self, timeout: Optional[float] = None) -> bool:
        """Wait for all tasks to complete."""
        start_time = time.time()
        
        while True:
            with self.lock:
                if (self.task_queue.empty() and self.active_count == 0):
                    return True
            
            if timeout is not None:
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    return False
            
            time.sleep(0.1)


# Global worker pool instance
_global_worker_pool = None


def get_worker_pool(num_workers: int = 4) -> WorkerPool:
    """Get or create the global worker pool."""
    global _global_worker_pool
    
    if _global_worker_pool is None:
        _global_worker_pool = WorkerPool(num_workers)
        _global_worker_pool.start()
    
    return _global_worker_pool
