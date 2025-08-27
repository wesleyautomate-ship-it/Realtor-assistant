"""
Sentry configuration for RAG Real Estate System
"""
import os
import logging
from typing import Optional, Dict, Any
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.httpx import HttpxIntegration
from sentry_sdk.integrations.asyncio import AsyncioIntegration

logger = logging.getLogger(__name__)

class SentryConfig:
    """Sentry configuration manager"""
    
    def __init__(self):
        self.dsn = os.getenv("SENTRY_DSN")
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.release = os.getenv("RELEASE_VERSION", "1.0.0")
        self.debug = os.getenv("SENTRY_DEBUG", "false").lower() == "true"
        self.traces_sample_rate = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1"))
        self.profiles_sample_rate = float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.1"))
        
    def initialize(self) -> bool:
        """Initialize Sentry SDK"""
        if not self.dsn:
            logger.warning("SENTRY_DSN not provided, Sentry will not be initialized")
            return False
        
        try:
            # Configure logging integration
            logging_integration = LoggingIntegration(
                level=logging.INFO,        # Capture info and above as breadcrumbs
                event_level=logging.ERROR  # Send errors as events
            )
            
            # Initialize Sentry SDK
            sentry_sdk.init(
                dsn=self.dsn,
                environment=self.environment,
                release=self.release,
                debug=self.debug,
                traces_sample_rate=self.traces_sample_rate,
                profiles_sample_rate=self.profiles_sample_rate,
                integrations=[
                    FastApiIntegration(),
                    RedisIntegration(),
                    SqlalchemyIntegration(),
                    logging_integration,
                    HttpxIntegration(),
                    AsyncioIntegration(),
                ],
                # Configure before_send to filter sensitive data
                before_send=self._before_send,
                # Configure before_breadcrumb to add context
                before_breadcrumb=self._before_breadcrumb,
                # Set default tags
                default_tags={
                    "service": "rag-real-estate",
                    "component": "backend"
                }
            )
            
            logger.info(f"Sentry initialized for environment: {self.environment}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Sentry: {e}")
            return False
    
    def _before_send(self, event: Dict[str, Any], hint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Filter and sanitize events before sending to Sentry"""
        try:
            # Remove sensitive data from event
            if "request" in event:
                # Remove authorization headers
                if "headers" in event["request"]:
                    sensitive_headers = ["authorization", "cookie", "x-api-key"]
                    for header in sensitive_headers:
                        if header in event["request"]["headers"]:
                            event["request"]["headers"][header] = "[REDACTED]"
                
                # Remove sensitive query parameters
                if "query_string" in event["request"]:
                    sensitive_params = ["password", "token", "key", "secret"]
                    query_string = event["request"]["query_string"]
                    for param in sensitive_params:
                        if param in query_string:
                            query_string = query_string.replace(f"{param}=", f"{param}=[REDACTED]")
                    event["request"]["query_string"] = query_string
            
            # Add custom context
            event.setdefault("tags", {}).update({
                "service": "rag-real-estate",
                "component": "backend"
            })
            
            # Add user context if available
            if "user" in event and not event["user"].get("id"):
                event["user"]["id"] = "[ANONYMOUS]"
            
            return event
            
        except Exception as e:
            logger.error(f"Error in before_send: {e}")
            return event
    
    def _before_breadcrumb(self, breadcrumb: Dict[str, Any], hint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Add context to breadcrumbs before sending to Sentry"""
        try:
            # Add custom context to breadcrumbs
            breadcrumb.setdefault("data", {}).update({
                "service": "rag-real-estate",
                "component": "backend"
            })
            
            # Filter out sensitive breadcrumbs
            sensitive_categories = ["auth", "http"]
            if breadcrumb.get("category") in sensitive_categories:
                # Remove sensitive data from breadcrumb
                if "data" in breadcrumb:
                    sensitive_keys = ["password", "token", "authorization"]
                    for key in sensitive_keys:
                        if key in breadcrumb["data"]:
                            breadcrumb["data"][key] = "[REDACTED]"
            
            return breadcrumb
            
        except Exception as e:
            logger.error(f"Error in before_breadcrumb: {e}")
            return breadcrumb
    
    def set_user_context(self, user_id: str, email: Optional[str] = None, username: Optional[str] = None):
        """Set user context for Sentry"""
        try:
            sentry_sdk.set_user({
                "id": user_id,
                "email": email,
                "username": username
            })
        except Exception as e:
            logger.error(f"Error setting user context: {e}")
    
    def set_tag(self, key: str, value: str):
        """Set a tag for Sentry"""
        try:
            sentry_sdk.set_tag(key, value)
        except Exception as e:
            logger.error(f"Error setting tag: {e}")
    
    def set_context(self, name: str, data: Dict[str, Any]):
        """Set context data for Sentry"""
        try:
            sentry_sdk.set_context(name, data)
        except Exception as e:
            logger.error(f"Error setting context: {e}")
    
    def add_breadcrumb(self, message: str, category: str = "default", level: str = "info", data: Optional[Dict[str, Any]] = None):
        """Add a breadcrumb to Sentry"""
        try:
            sentry_sdk.add_breadcrumb(
                message=message,
                category=category,
                level=level,
                data=data or {}
            )
        except Exception as e:
            logger.error(f"Error adding breadcrumb: {e}")
    
    def capture_exception(self, exception: Exception, context: Optional[Dict[str, Any]] = None):
        """Capture an exception in Sentry"""
        try:
            if context:
                with sentry_sdk.push_scope() as scope:
                    for key, value in context.items():
                        scope.set_context(key, value)
                    sentry_sdk.capture_exception(exception)
            else:
                sentry_sdk.capture_exception(exception)
        except Exception as e:
            logger.error(f"Error capturing exception: {e}")
    
    def capture_message(self, message: str, level: str = "info", context: Optional[Dict[str, Any]] = None):
        """Capture a message in Sentry"""
        try:
            if context:
                with sentry_sdk.push_scope() as scope:
                    for key, value in context.items():
                        scope.set_context(key, value)
                    sentry_sdk.capture_message(message, level=level)
            else:
                sentry_sdk.capture_message(message, level=level)
        except Exception as e:
            logger.error(f"Error capturing message: {e}")
    
    def start_transaction(self, name: str, operation: str = "default") -> Any:
        """Start a performance transaction"""
        try:
            return sentry_sdk.start_transaction(name=name, operation=operation)
        except Exception as e:
            logger.error(f"Error starting transaction: {e}")
            return None
    
    def set_extra(self, key: str, value: Any):
        """Set extra data for Sentry"""
        try:
            sentry_sdk.set_extra(key, value)
        except Exception as e:
            logger.error(f"Error setting extra: {e}")
    
    def flush(self, timeout: float = 2.0):
        """Flush Sentry events"""
        try:
            sentry_sdk.flush(timeout=timeout)
        except Exception as e:
            logger.error(f"Error flushing Sentry: {e}")

# Global Sentry configuration instance
sentry_config = SentryConfig()

def initialize_sentry() -> bool:
    """Initialize Sentry globally"""
    return sentry_config.initialize()

def get_sentry_config() -> SentryConfig:
    """Get the global Sentry configuration"""
    return sentry_config

# Convenience functions for common Sentry operations
def set_user_context(user_id: str, email: Optional[str] = None, username: Optional[str] = None):
    """Set user context for Sentry"""
    sentry_config.set_user_context(user_id, email, username)

def add_breadcrumb(message: str, category: str = "default", level: str = "info", data: Optional[Dict[str, Any]] = None):
    """Add a breadcrumb to Sentry"""
    sentry_config.add_breadcrumb(message, category, level, data)

def capture_exception(exception: Exception, context: Optional[Dict[str, Any]] = None):
    """Capture an exception in Sentry"""
    sentry_config.capture_exception(exception, context)

def capture_message(message: str, level: str = "info", context: Optional[Dict[str, Any]] = None):
    """Capture a message in Sentry"""
    sentry_config.capture_message(message, level, context)

def start_transaction(name: str, operation: str = "default") -> Any:
    """Start a performance transaction"""
    return sentry_config.start_transaction(name, operation)
