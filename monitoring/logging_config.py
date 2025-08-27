"""
Structured logging configuration for RAG Real Estate System
"""
import logging
import logging.handlers
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import traceback
from pythonjsonlogger import jsonlogger

class StructuredFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter with structured logging"""
    
    def add_fields(self, log_record, record, message_dict):
        """Add custom fields to log record"""
        super().add_fields(log_record, record, message_dict)
        
        # Add timestamp
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().isoformat()
        
        # Add log level
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
        
        # Add service information
        log_record['service'] = 'rag-real-estate'
        log_record['component'] = 'backend'
        
        # Add process information
        log_record['process_id'] = record.process
        log_record['thread_id'] = record.thread
        
        # Add module and function information
        log_record['module'] = record.module
        log_record['function'] = record.funcName
        log_record['line'] = record.lineno
        
        # Add request information if available
        if hasattr(record, 'request_id'):
            log_record['request_id'] = record.request_id
        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id
        if hasattr(record, 'session_id'):
            log_record['session_id'] = record.session_id
        
        # Add custom fields
        if hasattr(record, 'custom_fields'):
            log_record.update(record.custom_fields)

class LoggingConfig:
    """Logging configuration manager"""
    
    def __init__(self):
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.log_format = os.getenv("LOG_FORMAT", "json")  # json or text
        self.log_file = os.getenv("LOG_FILE", "logs/app.log")
        self.max_log_size = int(os.getenv("MAX_LOG_SIZE", "10"))  # MB
        self.backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))
        self.enable_console = os.getenv("ENABLE_CONSOLE_LOGGING", "true").lower() == "true"
        self.enable_file = os.getenv("ENABLE_FILE_LOGGING", "true").lower() == "true"
        self.enable_syslog = os.getenv("ENABLE_SYSLOG", "false").lower() == "true"
        
        # Create logs directory if it doesn't exist
        log_dir = Path(self.log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
    
    def setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        # Create root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.log_level))
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Create formatter
        if self.log_format == "json":
            formatter = StructuredFormatter(
                '%(timestamp)s %(level)s %(name)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        # Console handler
        if self.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, self.log_level))
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # File handler with rotation
        if self.enable_file:
            file_handler = logging.handlers.RotatingFileHandler(
                self.log_file,
                maxBytes=self.max_log_size * 1024 * 1024,  # Convert MB to bytes
                backupCount=self.backup_count
            )
            file_handler.setLevel(getattr(logging, self.log_level))
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        # Syslog handler
        if self.enable_syslog:
            try:
                syslog_handler = logging.handlers.SysLogHandler(
                    address='/dev/log',
                    facility=logging.handlers.SysLogHandler.LOG_LOCAL0
                )
                syslog_handler.setLevel(getattr(logging, self.log_level))
                syslog_handler.setFormatter(formatter)
                root_logger.addHandler(syslog_handler)
            except Exception as e:
                print(f"Failed to setup syslog handler: {e}")
        
        # Create application logger
        app_logger = logging.getLogger("rag_real_estate")
        app_logger.setLevel(getattr(logging, self.log_level))
        
        return app_logger
    
    def setup_request_logging(self) -> logging.Logger:
        """Setup request-specific logging"""
        request_logger = logging.getLogger("rag_real_estate.requests")
        request_logger.setLevel(getattr(logging, self.log_level))
        
        return request_logger
    
    def setup_error_logging(self) -> logging.Logger:
        """Setup error-specific logging"""
        error_logger = logging.getLogger("rag_real_estate.errors")
        error_logger.setLevel(logging.ERROR)
        
        return error_logger
    
    def setup_performance_logging(self) -> logging.Logger:
        """Setup performance-specific logging"""
        perf_logger = logging.getLogger("rag_real_estate.performance")
        perf_logger.setLevel(getattr(logging, self.log_level))
        
        return perf_logger

class RequestLogger:
    """Request logging middleware"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_request(self, request_id: str, method: str, path: str, user_id: Optional[str] = None, 
                   session_id: Optional[str] = None, **kwargs):
        """Log incoming request"""
        log_record = self.logger.makeRecord(
            name=self.logger.name,
            level=logging.INFO,
            fn="",
            lno=0,
            msg=f"Request: {method} {path}",
            args=(),
            exc_info=None
        )
        
        # Add custom fields
        log_record.request_id = request_id
        log_record.user_id = user_id
        log_record.session_id = session_id
        log_record.custom_fields = {
            "event_type": "request_start",
            "method": method,
            "path": path,
            "user_agent": kwargs.get("user_agent"),
            "ip_address": kwargs.get("ip_address"),
            "query_params": kwargs.get("query_params"),
            "request_size": kwargs.get("request_size")
        }
        
        self.logger.handle(log_record)
    
    def log_response(self, request_id: str, status_code: int, response_time: float, 
                    response_size: Optional[int] = None, **kwargs):
        """Log response"""
        log_record = self.logger.makeRecord(
            name=self.logger.name,
            level=logging.INFO,
            fn="",
            lno=0,
            msg=f"Response: {status_code} ({response_time:.3f}s)",
            args=(),
            exc_info=None
        )
        
        # Add custom fields
        log_record.request_id = request_id
        log_record.custom_fields = {
            "event_type": "request_end",
            "status_code": status_code,
            "response_time": response_time,
            "response_size": response_size,
            "error": kwargs.get("error")
        }
        
        self.logger.handle(log_record)

class ErrorLogger:
    """Error logging utility"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None, 
                  request_id: Optional[str] = None, user_id: Optional[str] = None):
        """Log error with context"""
        log_record = self.logger.makeRecord(
            name=self.logger.name,
            level=logging.ERROR,
            fn="",
            lno=0,
            msg=str(error),
            args=(),
            exc_info=(type(error), error, error.__traceback__)
        )
        
        # Add custom fields
        log_record.request_id = request_id
        log_record.user_id = user_id
        log_record.custom_fields = {
            "event_type": "error",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        
        self.logger.handle(log_record)
    
    def log_warning(self, message: str, context: Optional[Dict[str, Any]] = None,
                   request_id: Optional[str] = None, user_id: Optional[str] = None):
        """Log warning with context"""
        log_record = self.logger.makeRecord(
            name=self.logger.name,
            level=logging.WARNING,
            fn="",
            lno=0,
            msg=message,
            args=(),
            exc_info=None
        )
        
        # Add custom fields
        log_record.request_id = request_id
        log_record.user_id = user_id
        log_record.custom_fields = {
            "event_type": "warning",
            "context": context or {}
        }
        
        self.logger.handle(log_record)

class PerformanceLogger:
    """Performance logging utility"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_performance(self, operation: str, duration: float, success: bool = True,
                       metadata: Optional[Dict[str, Any]] = None, request_id: Optional[str] = None):
        """Log performance metrics"""
        log_record = self.logger.makeRecord(
            name=self.logger.name,
            level=logging.INFO,
            fn="",
            lno=0,
            msg=f"Performance: {operation} ({duration:.3f}s)",
            args=(),
            exc_info=None
        )
        
        # Add custom fields
        log_record.request_id = request_id
        log_record.custom_fields = {
            "event_type": "performance",
            "operation": operation,
            "duration": duration,
            "success": success,
            "metadata": metadata or {}
        }
        
        self.logger.handle(log_record)
    
    def log_rag_query(self, query_type: str, duration: float, success: bool = True,
                     result_count: Optional[int] = None, request_id: Optional[str] = None):
        """Log RAG query performance"""
        self.log_performance(
            operation=f"rag_query_{query_type}",
            duration=duration,
            success=success,
            metadata={
                "query_type": query_type,
                "result_count": result_count
            },
            request_id=request_id
        )
    
    def log_database_query(self, query_type: str, duration: float, success: bool = True,
                          row_count: Optional[int] = None, request_id: Optional[str] = None):
        """Log database query performance"""
        self.log_performance(
            operation=f"db_query_{query_type}",
            duration=duration,
            success=success,
            metadata={
                "query_type": query_type,
                "row_count": row_count
            },
            request_id=request_id
        )
    
    def log_external_api_call(self, api_name: str, duration: float, success: bool = True,
                             status_code: Optional[int] = None, request_id: Optional[str] = None):
        """Log external API call performance"""
        self.log_performance(
            operation=f"api_call_{api_name}",
            duration=duration,
            success=success,
            metadata={
                "api_name": api_name,
                "status_code": status_code
            },
            request_id=request_id
        )

# Global logging configuration
logging_config = LoggingConfig()

def setup_logging() -> logging.Logger:
    """Setup logging globally"""
    return logging_config.setup_logging()

def get_request_logger() -> RequestLogger:
    """Get request logger"""
    logger = logging_config.setup_request_logging()
    return RequestLogger(logger)

def get_error_logger() -> ErrorLogger:
    """Get error logger"""
    logger = logging_config.setup_error_logging()
    return ErrorLogger(logger)

def get_performance_logger() -> PerformanceLogger:
    """Get performance logger"""
    logger = logging_config.setup_performance_logging()
    return PerformanceLogger(logger)

# Convenience functions for common logging operations
def log_info(message: str, **kwargs):
    """Log info message"""
    logger = logging.getLogger("rag_real_estate")
    logger.info(message, extra=kwargs)

def log_warning(message: str, **kwargs):
    """Log warning message"""
    logger = logging.getLogger("rag_real_estate")
    logger.warning(message, extra=kwargs)

def log_error(message: str, **kwargs):
    """Log error message"""
    logger = logging.getLogger("rag_real_estate")
    logger.error(message, extra=kwargs)

def log_critical(message: str, **kwargs):
    """Log critical message"""
    logger = logging.getLogger("rag_real_estate")
    logger.critical(message, extra=kwargs)
