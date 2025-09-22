#!/usr/bin/env python3
"""
Enhanced Task Manager for Real Estate Operations
Handles task creation, status tracking, result storage, and AI-powered task management
"""

import uuid
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, asdict
import threading
import time
import google.generativeai as genai
import os

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"

class TaskPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"

class TaskCategory(Enum):
    CLIENT_COMMUNICATION = "client_communication"
    PROPERTY_LISTING = "property_listing"
    MARKET_RESEARCH = "market_research"
    DOCUMENT_PROCESSING = "document_processing"
    FOLLOW_UP = "follow_up"
    DEAL_STRUCTURING = "deal_structuring"
    CONTENT_GENERATION = "content_generation"
    ADMINISTRATIVE = "administrative"
    MARKETING = "marketing"
    COMPLIANCE = "compliance"

@dataclass
class ProcessingTask:
    task_id: str
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    instructions: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    progress: float = 0.0
    execution_plan: Optional[Dict[str, Any]] = None
    storage_summary: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    
    # Enhanced real estate specific fields
    priority: TaskPriority = TaskPriority.NORMAL
    category: TaskCategory = TaskCategory.ADMINISTRATIVE
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None
    client_id: Optional[str] = None
    property_id: Optional[str] = None
    lead_id: Optional[str] = None
    estimated_duration: Optional[int] = None  # in minutes
    actual_duration: Optional[int] = None
    tags: List[str] = None
    dependencies: List[str] = None
    ai_suggestions: Optional[Dict[str, Any]] = None
    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.dependencies is None:
            self.dependencies = []

class TaskManager:
    """Enhanced task manager for real estate operations with AI-powered features"""
    
    def __init__(self):
        self.tasks: Dict[str, ProcessingTask] = {}
        self._lock = threading.Lock()
        self.setup_ai_model()
    
    def setup_ai_model(self):
        """Initialize AI model for task suggestions and automation"""
        try:
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.ai_model = genai.GenerativeModel('gemini-1.5-flash')
                self.ai_available = True
                logger.info("✅ AI model configured for task management")
            else:
                self.ai_model = None
                self.ai_available = False
                logger.warning("⚠️ GOOGLE_API_KEY not found, AI features disabled")
        except Exception as e:
            self.ai_model = None
            self.ai_available = False
            logger.error(f"❌ Failed to setup AI model: {e}")
    
    def create_task(self, file_path: str, file_type: str, instructions: str = "") -> str:
        """Create a new processing task (legacy method)"""
        task_id = str(uuid.uuid4())
        
        task = ProcessingTask(
            task_id=task_id,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            file_path=file_path,
            file_type=file_type,
            instructions=instructions
        )
        
        with self._lock:
            self.tasks[task_id] = task
        
        logger.info(f"Created task {task_id} for file {file_path}")
        return task_id
    
    def create_real_estate_task(
        self,
        title: str,
        description: str,
        category: TaskCategory,
        priority: TaskPriority = TaskPriority.NORMAL,
        assigned_to: Optional[str] = None,
        due_date: Optional[datetime] = None,
        client_id: Optional[str] = None,
        property_id: Optional[str] = None,
        lead_id: Optional[str] = None,
        estimated_duration: Optional[int] = None,
        tags: Optional[List[str]] = None,
        dependencies: Optional[List[str]] = None
    ) -> str:
        """Create a new real estate specific task with enhanced metadata"""
        task_id = str(uuid.uuid4())
        
        task = ProcessingTask(
            task_id=task_id,
            status=TaskStatus.PENDING,
            created_at=datetime.now(),
            instructions=description,
            priority=priority,
            category=category,
            assigned_to=assigned_to,
            due_date=due_date,
            client_id=client_id,
            property_id=property_id,
            lead_id=lead_id,
            estimated_duration=estimated_duration,
            tags=tags or [],
            dependencies=dependencies or []
        )
        
        with self._lock:
            self.tasks[task_id] = task
        
        # Generate AI suggestions for the task
        if self.ai_available:
            self._generate_ai_suggestions(task_id)
        
        logger.info(f"Created real estate task {task_id}: {title}")
        return task_id
    
    def _generate_ai_suggestions(self, task_id: str):
        """Generate AI-powered suggestions for task optimization"""
        try:
            task = self.get_task(task_id)
            if not task or not self.ai_available:
                return
            
            prompt = f"""
            As a real estate AI assistant, analyze this task and provide optimization suggestions:
            
            Task: {task.instructions}
            Category: {task.category.value}
            Priority: {task.priority.value}
            Client ID: {task.client_id or 'N/A'}
            Property ID: {task.property_id or 'N/A'}
            
            Provide suggestions for:
            1. Estimated duration (in minutes)
            2. Recommended priority level
            3. Suggested tags for better organization
            4. Potential dependencies or related tasks
            5. Follow-up actions needed
            6. Best practices for this type of task
            
            Format as JSON with keys: estimated_duration, suggested_priority, suggested_tags, dependencies, follow_up_actions, best_practices
            """
            
            response = self.ai_model.generate_content(prompt)
            suggestions = json.loads(response.text)
            
            with self._lock:
                if task_id in self.tasks:
                    self.tasks[task_id].ai_suggestions = suggestions
                    
                    # Apply AI suggestions if they make sense
                    if suggestions.get('estimated_duration') and not task.estimated_duration:
                        self.tasks[task_id].estimated_duration = suggestions['estimated_duration']
                    
                    if suggestions.get('suggested_tags'):
                        self.tasks[task_id].tags.extend(suggestions['suggested_tags'])
                        self.tasks[task_id].tags = list(set(self.tasks[task_id].tags))  # Remove duplicates
                    
                    if suggestions.get('dependencies'):
                        self.tasks[task_id].dependencies.extend(suggestions['dependencies'])
                        self.tasks[task_id].dependencies = list(set(self.tasks[task_id].dependencies))
            
            logger.info(f"Generated AI suggestions for task {task_id}")
            
        except Exception as e:
            logger.error(f"Failed to generate AI suggestions for task {task_id}: {e}")
    
    def get_task(self, task_id: str) -> Optional[ProcessingTask]:
        """Get task by ID"""
        with self._lock:
            return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: TaskStatus, **kwargs):
        """Update task status and optional fields"""
        with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.status = status
                
                if status == TaskStatus.PROCESSING and not task.started_at:
                    task.started_at = datetime.now()
                elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED] and not task.completed_at:
                    task.completed_at = datetime.now()
                
                # Update any additional fields
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                
                logger.info(f"Updated task {task_id} status to {status}")
    
    def set_task_result(self, task_id: str, result: Dict[str, Any]):
        """Set the final result for a completed task"""
        with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.result = result
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                logger.info(f"Set result for task {task_id}")
    
    def set_task_error(self, task_id: str, error_message: str):
        """Set error message for a failed task"""
        with self._lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.error_message = error_message
                task.status = TaskStatus.FAILED
                task.completed_at = datetime.now()
                logger.error(f"Task {task_id} failed: {error_message}")
    
    def update_progress(self, task_id: str, progress: float):
        """Update task progress (0.0 to 1.0)"""
        with self._lock:
            if task_id in self.tasks:
                self.tasks[task_id].progress = min(1.0, max(0.0, progress))
    
    def cleanup_old_tasks(self, max_age_hours: int = 24):
        """Clean up tasks older than specified hours"""
        cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
        
        with self._lock:
            tasks_to_remove = [
                task_id for task_id, task in self.tasks.items()
                if task.created_at.timestamp() < cutoff_time
            ]
            
            for task_id in tasks_to_remove:
                del self.tasks[task_id]
            
            if tasks_to_remove:
                logger.info(f"Cleaned up {len(tasks_to_remove)} old tasks")
    
    def get_task_summary(self, task_id: str) -> Dict[str, Any]:
        """Get a summary of task for API response"""
        task = self.get_task(task_id)
        if not task:
            return None
        
        return {
            "task_id": task.task_id,
            "status": task.status.value,
            "progress": task.progress,
            "created_at": task.created_at.isoformat(),
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "result": task.result,
            "error_message": task.error_message,
            "execution_plan": task.execution_plan,
            "storage_summary": task.storage_summary,
            "performance_metrics": task.performance_metrics,
            "priority": task.priority.value,
            "category": task.category.value,
            "assigned_to": task.assigned_to,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "client_id": task.client_id,
            "property_id": task.property_id,
            "lead_id": task.lead_id,
            "estimated_duration": task.estimated_duration,
            "actual_duration": task.actual_duration,
            "tags": task.tags,
            "dependencies": task.dependencies,
            "ai_suggestions": task.ai_suggestions,
            "follow_up_required": task.follow_up_required,
            "follow_up_date": task.follow_up_date.isoformat() if task.follow_up_date else None
        }
    
    def get_tasks_by_category(self, category: TaskCategory) -> List[ProcessingTask]:
        """Get all tasks in a specific category"""
        with self._lock:
            return [task for task in self.tasks.values() if task.category == category]
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[ProcessingTask]:
        """Get all tasks with a specific priority"""
        with self._lock:
            return [task for task in self.tasks.values() if task.priority == priority]
    
    def get_tasks_by_assignee(self, assignee: str) -> List[ProcessingTask]:
        """Get all tasks assigned to a specific person"""
        with self._lock:
            return [task for task in self.tasks.values() if task.assigned_to == assignee]
    
    def get_overdue_tasks(self) -> List[ProcessingTask]:
        """Get all overdue tasks"""
        now = datetime.now()
        with self._lock:
            return [
                task for task in self.tasks.values()
                if task.due_date and task.due_date < now and task.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]
            ]
    
    def get_tasks_due_soon(self, hours: int = 24) -> List[ProcessingTask]:
        """Get tasks due within specified hours"""
        now = datetime.now()
        cutoff = now + timedelta(hours=hours)
        with self._lock:
            return [
                task for task in self.tasks.values()
                if task.due_date and now < task.due_date <= cutoff and task.status not in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]
            ]
    
    def get_tasks_by_client(self, client_id: str) -> List[ProcessingTask]:
        """Get all tasks related to a specific client"""
        with self._lock:
            return [task for task in self.tasks.values() if task.client_id == client_id]
    
    def get_tasks_by_property(self, property_id: str) -> List[ProcessingTask]:
        """Get all tasks related to a specific property"""
        with self._lock:
            return [task for task in self.tasks.values() if task.property_id == property_id]
    
    def get_tasks_by_lead(self, lead_id: str) -> List[ProcessingTask]:
        """Get all tasks related to a specific lead"""
        with self._lock:
            return [task for task in self.tasks.values() if task.lead_id == lead_id]
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """Get comprehensive task statistics"""
        with self._lock:
            total_tasks = len(self.tasks)
            if total_tasks == 0:
                return {"total_tasks": 0}
            
            status_counts = {}
            priority_counts = {}
            category_counts = {}
            
            for task in self.tasks.values():
                # Status counts
                status_counts[task.status.value] = status_counts.get(task.status.value, 0) + 1
                
                # Priority counts
                priority_counts[task.priority.value] = priority_counts.get(task.priority.value, 0) + 1
                
                # Category counts
                category_counts[task.category.value] = category_counts.get(task.category.value, 0) + 1
            
            overdue_count = len(self.get_overdue_tasks())
            due_soon_count = len(self.get_tasks_due_soon())
            
            return {
                "total_tasks": total_tasks,
                "status_breakdown": status_counts,
                "priority_breakdown": priority_counts,
                "category_breakdown": category_counts,
                "overdue_tasks": overdue_count,
                "due_soon_tasks": due_soon_count,
                "completion_rate": (status_counts.get("completed", 0) / total_tasks) * 100
            }
    
    def suggest_next_tasks(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """AI-powered task suggestions based on context"""
        if not self.ai_available:
            return []
        
        try:
            prompt = f"""
            As a real estate AI assistant, suggest the next 5 most important tasks based on this context:
            
            Context: {json.dumps(context, indent=2)}
            
            Consider:
            - Current market conditions
            - Client needs and timeline
            - Property status
            - Agent workload
            - Business priorities
            
            Return as JSON array with objects containing: title, description, category, priority, estimated_duration, reasoning
            """
            
            response = self.ai_model.generate_content(prompt)
            suggestions = json.loads(response.text)
            
            return suggestions if isinstance(suggestions, list) else []
            
        except Exception as e:
            logger.error(f"Failed to generate task suggestions: {e}")
            return []
    
    def auto_assign_priority(self, task_id: str) -> bool:
        """Automatically assign priority based on AI analysis"""
        if not self.ai_available:
            return False
        
        try:
            task = self.get_task(task_id)
            if not task:
                return False
            
            prompt = f"""
            Analyze this real estate task and assign the most appropriate priority level:
            
            Task: {task.instructions}
            Category: {task.category.value}
            Client ID: {task.client_id or 'N/A'}
            Property ID: {task.property_id or 'N/A'}
            Due Date: {task.due_date.isoformat() if task.due_date else 'Not set'}
            
            Priority levels: low, normal, high, urgent, critical
            
            Consider:
            - Client urgency and timeline
            - Market conditions
            - Deal value and importance
            - Regulatory deadlines
            - Business impact
            
            Return only the priority level as a single word.
            """
            
            response = self.ai_model.generate_content(prompt)
            suggested_priority = response.text.strip().lower()
            
            # Map to enum
            priority_mapping = {
                'low': TaskPriority.LOW,
                'normal': TaskPriority.NORMAL,
                'high': TaskPriority.HIGH,
                'urgent': TaskPriority.URGENT,
                'critical': TaskPriority.CRITICAL
            }
            
            if suggested_priority in priority_mapping:
                with self._lock:
                    if task_id in self.tasks:
                        self.tasks[task_id].priority = priority_mapping[suggested_priority]
                        logger.info(f"Auto-assigned priority {suggested_priority} to task {task_id}")
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to auto-assign priority for task {task_id}: {e}")
            return False

# Global task manager instance
task_manager = TaskManager()
