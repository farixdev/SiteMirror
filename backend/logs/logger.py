"""
Logging system for SiteMirror extraction engine.
Provides real-time log streaming with different severity levels.
"""

from enum import Enum
from datetime import datetime
from typing import Callable, List
from dataclasses import dataclass
import queue
import threading


class LogLevel(Enum):
    """Log severity levels."""
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    NETWORK = "NETWORK"
    DEBUG = "DEBUG"


@dataclass
class LogEntry:
    """Represents a single log entry."""
    timestamp: str
    level: LogLevel
    message: str
    thread_id: int = None
    
    def __str__(self) -> str:
        """Format log entry for display."""
        return f"[{self.timestamp}] {self.message}"


class Logger:
    """
    Thread-safe logger with callback system for real-time log streaming.
    """
    
    def __init__(self, max_entries: int = 10000):
        self.max_entries = max_entries
        self.logs: List[LogEntry] = []
        self.callbacks: List[Callable[[LogEntry], None]] = []
        self.lock = threading.Lock()
        self.log_queue = queue.Queue()
    
    def add_listener(self, callback: Callable[[LogEntry], None]) -> None:
        """Register a callback to receive log entries."""
        with self.lock:
            self.callbacks.append(callback)
    
    def remove_listener(self, callback: Callable[[LogEntry], None]) -> None:
        """Unregister a callback."""
        with self.lock:
            if callback in self.callbacks:
                self.callbacks.remove(callback)
    
    def _log(self, level: LogLevel, message: str) -> LogEntry:
        """Internal logging method."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        thread_id = threading.get_ident()
        
        entry = LogEntry(
            timestamp=timestamp,
            level=level,
            message=message,
            thread_id=thread_id
        )
        
        with self.lock:
            self.logs.append(entry)
            
            # Maintain max entries
            if len(self.logs) > self.max_entries:
                self.logs.pop(0)
            
            # Notify all listeners
            for callback in self.callbacks:
                try:
                    callback(entry)
                except Exception as e:
                    # Prevent callback errors from breaking logging
                    pass
        
        return entry
    
    def info(self, message: str) -> LogEntry:
        """Log info message."""
        return self._log(LogLevel.INFO, message)
    
    def success(self, message: str) -> LogEntry:
        """Log success message."""
        return self._log(LogLevel.SUCCESS, message)
    
    def warning(self, message: str) -> LogEntry:
        """Log warning message."""
        return self._log(LogLevel.WARNING, message)
    
    def error(self, message: str) -> LogEntry:
        """Log error message."""
        return self._log(LogLevel.ERROR, message)
    
    def network(self, message: str) -> LogEntry:
        """Log network activity."""
        return self._log(LogLevel.NETWORK, message)
    
    def debug(self, message: str) -> LogEntry:
        """Log debug message."""
        return self._log(LogLevel.DEBUG, message)
    
    def get_all_logs(self) -> List[LogEntry]:
        """Get all logged entries."""
        with self.lock:
            return self.logs.copy()
    
    def get_logs_by_level(self, level: LogLevel) -> List[LogEntry]:
        """Get logs filtered by level."""
        with self.lock:
            return [log for log in self.logs if log.level == level]
    
    def clear(self) -> None:
        """Clear all logs."""
        with self.lock:
            self.logs.clear()


# Global logger instance
_global_logger = Logger()


def get_logger() -> Logger:
    """Get the global logger instance."""
    return _global_logger
