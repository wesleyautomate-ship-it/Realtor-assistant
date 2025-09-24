"""
AI Task Orchestration Framework
===============================

AURA-inspired task orchestration system that manages async AI workflows,
package executions, and provides status tracking with retry logic.

This system powers all AURA-style features by:
- Managing async AI task queues
- Executing workflow packages (New Listing, Lead Nurturing, etc.)
- Providing real-time status updates
- Handling retries and error recovery
- Integrating with existing AI routers
"""

import uuid
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel, Field

# Import existing AI components
try:
    from domain.ai.action_engine import ActionEngine
    from domain.ai.ai_manager import AIEnhancementManager
except ImportError:
    ActionEngine = None
    AIEnhancementManager = None

logger = logging.getLogger(__name__)


class TaskStatus(str, Enum):
    """Task execution status"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class TaskType(str, Enum):
    """AI task types for AURA features"""
    # Marketing Automation
    CONTENT_GENERATION = "content_generation"
    POSTCARD_GENERATION = "postcard_generation"
    EMAIL_CAMPAIGN = "email_campaign"
    SOCIAL_MEDIA_POST = "social_media_post"
    
    # Data & Analytics
    CMA_GENERATION = "cma_generation"
    MARKET_ANALYSIS = "market_analysis"
    TREND_ANALYSIS = "trend_analysis"
    PRICE_PREDICTION = "price_prediction"
    
    # Strategy & Advisory
    LISTING_STRATEGY = "listing_strategy"
    NEGOTIATION_PREP = "negotiation_prep"
    INVESTMENT_OUTLOOK = "investment_outlook"
    
    # Lead & Client Management
    LEAD_SCORING = "lead_scoring"
    PROPERTY_MATCHING = "property_matching"
    NURTURE_SEQUENCE = "nurture_sequence"
    
    # Workflow & Package Management
    WORKFLOW_EXECUTION = "workflow_execution"
    PACKAGE_ORCHESTRATION = "package_orchestration"
    
    # Cross-cutting
    NOTIFICATION = "notification"
    API_CALL = "api_call"
    HUMAN_REVIEW = "human_review"


class TaskPriority(int, Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 5
    HIGH = 8
    URGENT = 10


class AITaskRequest(BaseModel):
    """AI task request model"""
    task_type: TaskType
    user_id: int
    input_data: Dict[str, Any]
    priority: TaskPriority = TaskPriority.NORMAL
    max_retries: int = 3
    timeout_seconds: int = 300
    context: Optional[Dict[str, Any]] = None


class AITaskResult(BaseModel):
    """AI task result model"""
    task_id: str
    status: TaskStatus
    progress: int = Field(ge=0, le=100)
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retries: int = 0


class WorkflowStep(BaseModel):
    """Individual workflow step definition"""
    step_name: str
    step_type: TaskType
    description: str
    estimated_duration: int  # seconds
    inputs: List[str]
    outputs: List[str]
    depends_on: Optional[List[str]] = None
    ai_task_config: Optional[Dict[str, Any]] = None


class WorkflowPackage(BaseModel):
    """AURA-style workflow package definition"""
    package_id: str
    name: str
    description: str
    category: str
    steps: List[WorkflowStep]
    estimated_duration: int
    context_data: Optional[Dict[str, Any]] = None


class AITaskOrchestrator:
    """
    Main orchestrator for AI tasks and AURA-style workflow packages.
    
    Features:
    - Async task queue management
    - Workflow package execution
    - Status tracking and notifications
    - Error handling and retries
    - Integration with existing AI services
    """
    
    def __init__(self, db_session_factory: Callable[[], Session]):
        self.db_session_factory = db_session_factory
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.task_processors: Dict[TaskType, Callable] = {}
        self.action_engine = ActionEngine() if ActionEngine else None
        
        # Register default task processors
        self._register_default_processors()
    
    def _register_default_processors(self):
        """Register default task processors for AURA features"""
        self.task_processors.update({
            TaskType.CONTENT_GENERATION: self._process_content_generation,
            TaskType.CMA_GENERATION: self._process_cma_generation,
            TaskType.LISTING_STRATEGY: self._process_listing_strategy,
            TaskType.LEAD_SCORING: self._process_lead_scoring,
            TaskType.SOCIAL_MEDIA_POST: self._process_social_media_post,
            TaskType.WORKFLOW_EXECUTION: self._process_workflow_execution,
            TaskType.NOTIFICATION: self._process_notification,
        })
    
    async def submit_task(self, request: AITaskRequest) -> str:
        """
        Submit a new AI task for processing.
        
        Args:
            request: AI task request with type, data, and configuration
            
        Returns:
            task_id: Unique identifier for tracking the task
        """
        task_id = str(uuid.uuid4())
        
        try:
            # Store task in database
            with self.db_session_factory() as db:
                db.execute(text("""
                    INSERT INTO ai_tasks (id, user_id, task_type, input_data, status, 
                                        priority, progress, retries, max_retries, created_at)
                    VALUES (:task_id, :user_id, :task_type, :input_data, :status, 
                           :priority, :progress, :retries, :max_retries, :created_at)
                """), {
                    'task_id': task_id,
                    'user_id': request.user_id,
                    'task_type': request.task_type.value,
                    'input_data': json.dumps(request.input_data),
                    'status': TaskStatus.QUEUED.value,
                    'priority': request.priority.value,
                    'progress': 0,
                    'retries': 0,
                    'max_retries': request.max_retries,
                    'created_at': datetime.utcnow()
                })
                db.commit()
            
            # Start async processing
            asyncio.create_task(self._process_task(task_id, request))
            
            logger.info(f"AI task {task_id} submitted for processing")
            return task_id
            
        except Exception as e:
            logger.error(f"Failed to submit task: {e}")
            raise
    
    async def get_task_status(self, task_id: str) -> AITaskResult:
        """Get current status of a task"""
        try:
            with self.db_session_factory() as db:
                result = db.execute(text("""
                    SELECT id, status, progress, output_data, error_message, 
                           started_at, completed_at, retries
                    FROM ai_tasks 
                    WHERE id = :task_id
                """), {'task_id': task_id})
                
                row = result.fetchone()
                if not row:
                    raise ValueError(f"Task {task_id} not found")
                
                return AITaskResult(
                    task_id=row.id,
                    status=TaskStatus(row.status),
                    progress=row.progress,
                    output_data=json.loads(row.output_data) if row.output_data else None,
                    error_message=row.error_message,
                    started_at=row.started_at,
                    completed_at=row.completed_at,
                    retries=row.retries
                )
                
        except Exception as e:
            logger.error(f"Failed to get task status: {e}")
            raise
    
    async def execute_workflow_package(self, package: WorkflowPackage, 
                                     user_id: int, context: Dict[str, Any]) -> str:
        """
        Execute a complete AURA-style workflow package.
        
        Args:
            package: Workflow package definition
            user_id: User executing the package
            context: Initial context data (property details, client info, etc.)
            
        Returns:
            execution_id: Unique identifier for tracking the package execution
        """
        execution_id = str(uuid.uuid4())
        
        try:
            # Store package execution in database
            with self.db_session_factory() as db:
                db.execute(text("""
                    INSERT INTO package_executions (id, package_id, user_id, title, status, 
                                                   progress, context_data, started_at, created_at)
                    VALUES (:execution_id, :package_id, :user_id, :title, :status, 
                           :progress, :context_data, :started_at, :created_at)
                """), {
                    'execution_id': execution_id,
                    'package_id': package.package_id,
                    'user_id': user_id,
                    'title': f"{package.name} - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
                    'status': 'running',
                    'progress': 0,
                    'context_data': json.dumps(context),
                    'started_at': datetime.utcnow(),
                    'created_at': datetime.utcnow()
                })
                db.commit()
            
            # Start async package execution
            asyncio.create_task(self._execute_package_steps(execution_id, package, user_id, context))
            
            logger.info(f"Workflow package {package.name} started with execution ID {execution_id}")
            return execution_id
            
        except Exception as e:
            logger.error(f"Failed to execute workflow package: {e}")
            raise
    
    async def _process_task(self, task_id: str, request: AITaskRequest):
        """Process a single AI task"""
        try:
            # Update task status to processing
            await self._update_task_status(task_id, TaskStatus.PROCESSING, 0)
            
            # Get appropriate processor
            processor = self.task_processors.get(request.task_type)
            if not processor:
                raise ValueError(f"No processor registered for task type {request.task_type}")
            
            # Process the task
            result = await processor(task_id, request)
            
            # Update task with results
            await self._update_task_completion(task_id, TaskStatus.COMPLETED, 100, result)
            
        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            await self._handle_task_failure(task_id, request, str(e))
    
    async def _execute_package_steps(self, execution_id: str, package: WorkflowPackage, 
                                   user_id: int, context: Dict[str, Any]):
        """Execute all steps in a workflow package"""
        try:
            total_steps = len(package.steps)
            completed_steps = 0
            execution_context = context.copy()
            
            for step in package.steps:
                try:
                    # Create step record
                    step_id = await self._create_package_step(execution_id, step)
                    
                    # Process the step
                    step_result = await self._process_package_step(step_id, step, user_id, execution_context)
                    
                    # Update execution context with step outputs
                    if step_result:
                        execution_context.update(step_result)
                    
                    completed_steps += 1
                    progress = int((completed_steps / total_steps) * 100)
                    
                    # Update package execution progress
                    await self._update_package_execution(execution_id, 'running', progress, execution_context)
                    
                except Exception as step_error:
                    logger.error(f"Step {step.step_name} failed: {step_error}")
                    await self._update_package_execution(execution_id, 'failed', progress, execution_context, str(step_error))
                    return
            
            # Mark package as completed
            await self._update_package_execution(execution_id, 'completed', 100, execution_context)
            logger.info(f"Workflow package execution {execution_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Package execution {execution_id} failed: {e}")
            await self._update_package_execution(execution_id, 'failed', 0, context, str(e))
    
    async def _process_package_step(self, step_id: str, step: WorkflowStep, 
                                  user_id: int, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process an individual package step"""
        try:
            # Update step status
            await self._update_package_step(step_id, 'running', 0)
            
            if step.step_type == TaskType.HUMAN_REVIEW:
                # For human review steps, mark as pending and return
                await self._update_package_step(step_id, 'pending', 0, 
                                              {"message": "Waiting for human review"})
                return {"human_review_required": True, "step_id": step_id}
            
            # Create AI task request for the step
            task_request = AITaskRequest(
                task_type=step.step_type,
                user_id=user_id,
                input_data={
                    "step_name": step.step_name,
                    "step_context": context,
                    "step_config": step.ai_task_config or {}
                }
            )
            
            # Submit and wait for task completion
            task_id = await self.submit_task(task_request)
            
            # Poll for completion (with timeout)
            timeout = datetime.utcnow() + timedelta(seconds=step.estimated_duration * 2)
            while datetime.utcnow() < timeout:
                task_status = await self.get_task_status(task_id)
                
                if task_status.status == TaskStatus.COMPLETED:
                    await self._update_package_step(step_id, 'completed', 100, task_status.output_data)
                    return task_status.output_data
                elif task_status.status == TaskStatus.FAILED:
                    await self._update_package_step(step_id, 'failed', 0, 
                                                  {"error": task_status.error_message})
                    raise Exception(f"Step task failed: {task_status.error_message}")
                
                await asyncio.sleep(2)  # Poll every 2 seconds
            
            raise TimeoutError(f"Step {step.step_name} timed out")
            
        except Exception as e:
            await self._update_package_step(step_id, 'failed', 0, {"error": str(e)})
            raise
    
    # Task Processors for AURA Features
    async def _process_content_generation(self, task_id: str, request: AITaskRequest) -> Dict[str, Any]:
        """Process content generation tasks (marketing copy, descriptions, etc.)"""
        await self._update_task_progress(task_id, 25)
        
        input_data = request.input_data
        content_type = input_data.get('content_type', 'general')
        
        if content_type == 'marketing_campaign':
            return await self._generate_marketing_campaign(input_data)
        elif content_type == 'property_description':
            return await self._generate_property_description(input_data)
        else:
            return await self._generate_general_content(input_data)
    
    async def _process_cma_generation(self, task_id: str, request: AITaskRequest) -> Dict[str, Any]:
        """Process CMA (Comparative Market Analysis) generation"""
        await self._update_task_progress(task_id, 20)
        
        property_data = request.input_data
        # Integrate with existing ML insights router
        cma_data = await self._generate_cma_analysis(property_data)
        
        await self._update_task_progress(task_id, 80)
        
        return {
            "cma_report": cma_data,
            "pdf_generated": True,
            "confidence_score": 0.85
        }
    
    async def _process_listing_strategy(self, task_id: str, request: AITaskRequest) -> Dict[str, Any]:
        """Process listing strategy generation"""
        await self._update_task_progress(task_id, 30)
        
        property_data = request.input_data
        strategy = await self._generate_listing_strategy(property_data)
        
        await self._update_task_progress(task_id, 90)
        
        return {
            "listing_strategy": strategy,
            "target_audience": strategy.get("target_audience"),
            "marketing_timeline": strategy.get("timeline")
        }
    
    async def _process_social_media_post(self, task_id: str, request: AITaskRequest) -> Dict[str, Any]:
        """Process social media post generation"""
        await self._update_task_progress(task_id, 40)
        
        post_data = request.input_data
        platform = post_data.get('platform', 'instagram')
        
        content = await self._generate_social_media_content(post_data, platform)
        
        await self._update_task_progress(task_id, 90)
        
        return {
            "platform": platform,
            "content": content,
            "hashtags": content.get("hashtags", []),
            "scheduled_time": None
        }
    
    # Helper methods for database operations
    async def _update_task_status(self, task_id: str, status: TaskStatus, progress: int):
        """Update task status and progress"""
        with self.db_session_factory() as db:
            db.execute(text("""
                UPDATE ai_tasks 
                SET status = :status, progress = :progress,
                    started_at = CASE WHEN :status = 'processing' AND started_at IS NULL 
                                     THEN :now ELSE started_at END
                WHERE id = :task_id
            """), {
                'task_id': task_id,
                'status': status.value,
                'progress': progress,
                'now': datetime.utcnow()
            })
            db.commit()
    
    async def _update_task_completion(self, task_id: str, status: TaskStatus, 
                                    progress: int, output_data: Dict[str, Any]):
        """Update task completion with results"""
        with self.db_session_factory() as db:
            db.execute(text("""
                UPDATE ai_tasks 
                SET status = :status, progress = :progress, output_data = :output_data,
                    completed_at = :completed_at
                WHERE id = :task_id
            """), {
                'task_id': task_id,
                'status': status.value,
                'progress': progress,
                'output_data': json.dumps(output_data),
                'completed_at': datetime.utcnow()
            })
            db.commit()
    
    async def _handle_task_failure(self, task_id: str, request: AITaskRequest, error_message: str):
        """Handle task failure with retry logic"""
        with self.db_session_factory() as db:
            # Get current retry count
            result = db.execute(text("SELECT retries, max_retries FROM ai_tasks WHERE id = :task_id"), 
                              {'task_id': task_id})
            row = result.fetchone()
            
            if row and row.retries < row.max_retries:
                # Retry the task
                db.execute(text("""
                    UPDATE ai_tasks 
                    SET status = :status, retries = retries + 1, error_message = :error_message
                    WHERE id = :task_id
                """), {
                    'task_id': task_id,
                    'status': TaskStatus.RETRYING.value,
                    'error_message': error_message
                })
                db.commit()
                
                # Schedule retry after delay
                await asyncio.sleep(min(2 ** row.retries, 30))  # Exponential backoff
                asyncio.create_task(self._process_task(task_id, request))
            else:
                # Mark as permanently failed
                db.execute(text("""
                    UPDATE ai_tasks 
                    SET status = :status, error_message = :error_message, completed_at = :completed_at
                    WHERE id = :task_id
                """), {
                    'task_id': task_id,
                    'status': TaskStatus.FAILED.value,
                    'error_message': error_message,
                    'completed_at': datetime.utcnow()
                })
                db.commit()
    
    # Placeholder implementations for AI processing
    # These will integrate with your existing AI routers
    
    async def _generate_marketing_campaign(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate marketing campaign content"""
        # This would integrate with your existing AI assistant router
        return {
            "campaign_type": "just_listed",
            "content": {
                "headline": "Luxury Apartment in Dubai Marina",
                "description": "Stunning 2BR with marina views...",
                "call_to_action": "Schedule your viewing today!"
            }
        }
    
    async def _generate_cma_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate CMA analysis"""
        # This would integrate with your ML insights router
        return {
            "comparable_properties": [],
            "price_recommendations": {
                "aggressive": 2500000,
                "standard": 2300000,
                "conservative": 2100000
            },
            "market_conditions": "strong"
        }
    
    async def _generate_listing_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate listing strategy"""
        return {
            "target_audience": "Luxury investors and families",
            "key_selling_points": ["Marina views", "Premium finishes", "Prime location"],
            "timeline": "4-week marketing campaign"
        }
    
    async def _generate_social_media_content(self, data: Dict[str, Any], platform: str) -> Dict[str, Any]:
        """Generate social media content"""
        return {
            "caption": "✨ JUST LISTED ✨ Luxury apartment in Dubai Marina...",
            "hashtags": ["#DubaiRealEstate", "#LuxuryLiving", "#PropertyPro"]
        }
