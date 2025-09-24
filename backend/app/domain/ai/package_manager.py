"""
Workflow Package Manager
========================

Manages AURA-style workflow packages by loading them from the database,
converting them to executable workflows, and coordinating with the task orchestrator.

This system provides:
- Package template loading and validation
- Dynamic package customization
- Package execution orchestration
- Progress monitoring and reporting
"""

import json
import logging
from typing import Dict, Any, List, Optional, Callable
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from .task_orchestrator import (
    AITaskOrchestrator, WorkflowPackage, WorkflowStep, 
    TaskType, TaskPriority, AITaskRequest
)

logger = logging.getLogger(__name__)


class PackageExecutionContext(dict):
    """Enhanced dictionary for package execution context with validation"""
    
    def require(self, key: str, default: Any = None) -> Any:
        """Require a context value, providing a default if not present"""
        if key not in self and default is None:
            raise KeyError(f"Required context key '{key}' not found")
        return self.get(key, default)
    
    def merge_outputs(self, step_outputs: Dict[str, Any]):
        """Merge step outputs into context with conflict resolution"""
        for key, value in step_outputs.items():
            if key in self:
                # Handle conflicts by creating arrays or versioned keys
                existing = self[key]
                if isinstance(existing, list):
                    existing.append(value)
                else:
                    self[key] = [existing, value]
            else:
                self[key] = value


class WorkflowPackageManager:
    """
    Manages AURA workflow packages and their execution.
    
    Features:
    - Load package templates from database
    - Validate package definitions
    - Execute packages via task orchestrator
    - Monitor package execution status
    - Handle package customization
    """
    
    def __init__(self, db_session_factory: Callable[[], Session], 
                 task_orchestrator: AITaskOrchestrator):
        self.db_session_factory = db_session_factory
        self.orchestrator = task_orchestrator
        self.package_cache: Dict[str, WorkflowPackage] = {}
    
    async def get_available_packages(self, category: Optional[str] = None, 
                                   user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get list of available workflow packages.
        
        Args:
            category: Filter by package category (listing, nurturing, etc.)
            user_id: Filter by user access (for custom packages)
            
        Returns:
            List of package summaries
        """
        try:
            with self.db_session_factory() as db:
                query = """
                    SELECT id, name, description, category, estimated_duration, 
                           usage_count, is_template, created_by
                    FROM workflow_packages 
                    WHERE is_active = true
                """
                params = {}
                
                if category:
                    query += " AND category = :category"
                    params['category'] = category
                
                if user_id:
                    query += " AND (is_template = true OR created_by = :user_id)"
                    params['user_id'] = user_id
                
                query += " ORDER BY usage_count DESC, name ASC"
                
                result = db.execute(text(query), params)
                packages = []
                
                for row in result.fetchall():
                    packages.append({
                        'id': row.id,
                        'name': row.name,
                        'description': row.description,
                        'category': row.category,
                        'estimated_duration': row.estimated_duration,
                        'usage_count': row.usage_count,
                        'is_template': row.is_template,
                        'created_by': row.created_by
                    })
                
                return packages
                
        except Exception as e:
            logger.error(f"Failed to get available packages: {e}")
            raise
    
    async def load_package(self, package_id: int) -> WorkflowPackage:
        """
        Load a workflow package from the database.
        
        Args:
            package_id: Database ID of the package
            
        Returns:
            WorkflowPackage object ready for execution
        """
        # Check cache first
        cache_key = str(package_id)
        if cache_key in self.package_cache:
            return self.package_cache[cache_key]
        
        try:
            with self.db_session_factory() as db:
                result = db.execute(text("""
                    SELECT id, name, description, category, steps, estimated_duration
                    FROM workflow_packages 
                    WHERE id = :package_id AND is_active = true
                """), {'package_id': package_id})
                
                row = result.fetchone()
                if not row:
                    raise ValueError(f"Package {package_id} not found or inactive")
                
                # Parse steps from JSON
                steps_data = json.loads(row.steps)
                workflow_steps = []
                
                for step_data in steps_data:
                    workflow_step = WorkflowStep(
                        step_name=step_data['step_name'],
                        step_type=TaskType(step_data['step_type']),
                        description=step_data['description'],
                        estimated_duration=step_data['estimated_duration'],
                        inputs=step_data['inputs'],
                        outputs=step_data['outputs'],
                        depends_on=step_data.get('depends_on'),
                        ai_task_config=step_data.get('ai_task_config')
                    )
                    workflow_steps.append(workflow_step)
                
                package = WorkflowPackage(
                    package_id=str(row.id),
                    name=row.name,
                    description=row.description,
                    category=row.category,
                    steps=workflow_steps,
                    estimated_duration=row.estimated_duration
                )
                
                # Cache the package
                self.package_cache[cache_key] = package
                return package
                
        except Exception as e:
            logger.error(f"Failed to load package {package_id}: {e}")
            raise
    
    async def execute_package(self, package_id: int, user_id: int, 
                            context: Dict[str, Any]) -> str:
        """
        Execute a workflow package with the given context.
        
        Args:
            package_id: Database ID of the package to execute
            user_id: User executing the package
            context: Initial context data for the package
            
        Returns:
            execution_id: Unique identifier for tracking execution
        """
        try:
            # Load the package
            package = await self.load_package(package_id)
            
            # Validate context requirements
            validated_context = await self._validate_package_context(package, context)
            
            # Increment usage counter
            await self._increment_usage_count(package_id)
            
            # Execute via orchestrator
            execution_id = await self.orchestrator.execute_workflow_package(
                package, user_id, validated_context
            )
            
            logger.info(f"Package {package.name} started for user {user_id} with execution {execution_id}")
            return execution_id
            
        except Exception as e:
            logger.error(f"Failed to execute package {package_id}: {e}")
            raise
    
    async def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Get detailed status of a package execution"""
        try:
            with self.db_session_factory() as db:
                # Get execution details
                execution_result = db.execute(text("""
                    SELECT pe.id, pe.package_id, pe.user_id, pe.title, pe.status, 
                           pe.progress, pe.context_data, pe.started_at, pe.completed_at,
                           pe.error_message, wp.name as package_name
                    FROM package_executions pe
                    JOIN workflow_packages wp ON pe.package_id = wp.id
                    WHERE pe.id = :execution_id
                """), {'execution_id': execution_id})
                
                execution_row = execution_result.fetchone()
                if not execution_row:
                    raise ValueError(f"Execution {execution_id} not found")
                
                # Get step details
                steps_result = db.execute(text("""
                    SELECT step_name, step_type, status, progress, 
                           input_data, output_data, error_message,
                           started_at, completed_at
                    FROM package_steps
                    WHERE execution_id = :execution_id
                    ORDER BY created_at ASC
                """), {'execution_id': execution_id})
                
                steps = []
                for step_row in steps_result.fetchall():
                    steps.append({
                        'step_name': step_row.step_name,
                        'step_type': step_row.step_type,
                        'status': step_row.status,
                        'progress': step_row.progress,
                        'input_data': json.loads(step_row.input_data) if step_row.input_data else None,
                        'output_data': json.loads(step_row.output_data) if step_row.output_data else None,
                        'error_message': step_row.error_message,
                        'started_at': step_row.started_at,
                        'completed_at': step_row.completed_at
                    })
                
                return {
                    'execution_id': execution_row.id,
                    'package_id': execution_row.package_id,
                    'package_name': execution_row.package_name,
                    'user_id': execution_row.user_id,
                    'title': execution_row.title,
                    'status': execution_row.status,
                    'progress': execution_row.progress,
                    'context_data': json.loads(execution_row.context_data) if execution_row.context_data else {},
                    'started_at': execution_row.started_at,
                    'completed_at': execution_row.completed_at,
                    'error_message': execution_row.error_message,
                    'steps': steps
                }
                
        except Exception as e:
            logger.error(f"Failed to get execution status: {e}")
            raise
    
    async def create_custom_package(self, user_id: int, name: str, description: str,
                                  category: str, steps: List[Dict[str, Any]]) -> int:
        """
        Create a custom workflow package for a user.
        
        Args:
            user_id: User creating the package
            name: Package name
            description: Package description
            category: Package category
            steps: List of step definitions
            
        Returns:
            package_id: Database ID of the created package
        """
        try:
            # Validate steps
            validated_steps = await self._validate_package_steps(steps)
            
            # Calculate estimated duration
            total_duration = sum(step['estimated_duration'] for step in validated_steps)
            
            with self.db_session_factory() as db:
                result = db.execute(text("""
                    INSERT INTO workflow_packages (name, description, category, steps, 
                                                 estimated_duration, is_template, created_by, 
                                                 brokerage_id, created_at, updated_at)
                    VALUES (:name, :description, :category, :steps, :estimated_duration, 
                           false, :created_by, 
                           (SELECT brokerage_id FROM users WHERE id = :user_id), 
                           :created_at, :updated_at)
                    RETURNING id
                """), {
                    'name': name,
                    'description': description,
                    'category': category,
                    'steps': json.dumps(validated_steps),
                    'estimated_duration': total_duration,
                    'created_by': user_id,
                    'user_id': user_id,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                })
                
                package_id = result.fetchone().id
                db.commit()
                
                logger.info(f"Custom package '{name}' created by user {user_id} with ID {package_id}")
                return package_id
                
        except Exception as e:
            logger.error(f"Failed to create custom package: {e}")
            raise
    
    async def get_predefined_packages(self) -> Dict[str, WorkflowPackage]:
        """
        Get predefined AURA packages for immediate use.
        
        Returns:
            Dictionary of package name to WorkflowPackage objects
        """
        packages = {}
        
        # New Listing Package
        packages['new_listing'] = WorkflowPackage(
            package_id='new_listing',
            name='New Listing Package',
            description='Complete AURA-style workflow for launching a new property listing',
            category='listing',
            estimated_duration=2400,  # 40 minutes
            steps=[
                WorkflowStep(
                    step_name='Generate CMA Report',
                    step_type=TaskType.CMA_GENERATION,
                    description='Create comparative market analysis with pricing recommendations',
                    estimated_duration=300,  # 5 minutes
                    inputs=['property_address', 'property_details'],
                    outputs=['cma_report', 'price_recommendations']
                ),
                WorkflowStep(
                    step_name='Create Listing Strategy',
                    step_type=TaskType.LISTING_STRATEGY,
                    description='Develop comprehensive listing strategy document',
                    estimated_duration=480,  # 8 minutes
                    inputs=['property_details', 'cma_data', 'market_conditions'],
                    outputs=['listing_strategy', 'marketing_timeline']
                ),
                WorkflowStep(
                    step_name='Generate Marketing Campaign',
                    step_type=TaskType.CONTENT_GENERATION,
                    description='Create postcard, email, and social media content',
                    estimated_duration=600,  # 10 minutes
                    inputs=['property_details', 'listing_strategy', 'brand_assets'],
                    outputs=['marketing_campaign', 'social_posts', 'email_templates'],
                    ai_task_config={'content_type': 'marketing_campaign'}
                ),
                WorkflowStep(
                    step_name='Agent Review & Approval',
                    step_type=TaskType.HUMAN_REVIEW,
                    description='Agent reviews and approves all generated content',
                    estimated_duration=900,  # 15 minutes
                    inputs=['all_generated_content'],
                    outputs=['approved_campaign', 'revision_requests']
                ),
                WorkflowStep(
                    step_name='Launch Marketing Campaign',
                    step_type=TaskType.API_CALL,
                    description='Distribute approved marketing materials',
                    estimated_duration=120,  # 2 minutes
                    inputs=['approved_campaign'],
                    outputs=['campaign_metrics', 'distribution_report']
                )
            ]
        )
        
        # Lead Nurturing Package
        packages['lead_nurturing'] = WorkflowPackage(
            package_id='lead_nurturing',
            name='Lead Nurturing Package',
            description='Automated lead nurturing sequence with personalized touchpoints',
            category='nurturing',
            estimated_duration=960,  # 16 minutes
            steps=[
                WorkflowStep(
                    step_name='Lead Qualification Analysis',
                    step_type=TaskType.LEAD_SCORING,
                    description='Analyze lead profile and investment potential',
                    estimated_duration=180,  # 3 minutes
                    inputs=['client_profile', 'budget', 'preferences'],
                    outputs=['lead_score', 'persona_category']
                ),
                WorkflowStep(
                    step_name='Personalized Welcome Email',
                    step_type=TaskType.EMAIL_CAMPAIGN,
                    description='Generate personalized welcome email based on lead profile',
                    estimated_duration=300,  # 5 minutes
                    inputs=['client_profile', 'persona_category'],
                    outputs=['welcome_email', 'follow_up_schedule']
                ),
                WorkflowStep(
                    step_name='Property Recommendations',
                    step_type=TaskType.PROPERTY_MATCHING,
                    description='Generate curated property recommendations',
                    estimated_duration=420,  # 7 minutes
                    inputs=['client_preferences', 'current_listings'],
                    outputs=['property_list', 'matching_explanations']
                ),
                WorkflowStep(
                    step_name='Schedule Follow-up Tasks',
                    step_type=TaskType.NOTIFICATION,
                    description='Set up automated follow-up reminders for agent',
                    estimated_duration=60,  # 1 minute
                    inputs=['follow_up_schedule'],
                    outputs=['scheduled_tasks', 'reminder_notifications']
                )
            ]
        )
        
        return packages
    
    # Private helper methods
    
    async def _validate_package_context(self, package: WorkflowPackage, 
                                      context: Dict[str, Any]) -> PackageExecutionContext:
        """Validate and enrich package execution context"""
        validated_context = PackageExecutionContext(context)
        
        # Add package metadata
        validated_context['_package_id'] = package.package_id
        validated_context['_package_name'] = package.name
        validated_context['_execution_start'] = datetime.utcnow()
        
        # Validate required inputs for first step
        if package.steps:
            first_step = package.steps[0]
            for required_input in first_step.inputs:
                if required_input not in validated_context:
                    # Try to provide defaults for common inputs
                    default_value = self._get_default_context_value(required_input)
                    if default_value is not None:
                        validated_context[required_input] = default_value
                    else:
                        logger.warning(f"Missing required input '{required_input}' for package {package.name}")
        
        return validated_context
    
    def _get_default_context_value(self, input_key: str) -> Any:
        """Provide default values for common context inputs"""
        defaults = {
            'market_conditions': 'stable',
            'brand_assets': [],
            'current_listings': [],
            'agent_preferences': {},
        }
        return defaults.get(input_key)
    
    async def _validate_package_steps(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate package step definitions"""
        validated_steps = []
        
        for step in steps:
            # Required fields
            required_fields = ['step_name', 'step_type', 'description', 'estimated_duration', 'inputs', 'outputs']
            for field in required_fields:
                if field not in step:
                    raise ValueError(f"Step missing required field: {field}")
            
            # Validate task type
            try:
                TaskType(step['step_type'])
            except ValueError:
                raise ValueError(f"Invalid task type: {step['step_type']}")
            
            validated_steps.append(step)
        
        return validated_steps
    
    async def _increment_usage_count(self, package_id: int):
        """Increment the usage count for a package"""
        try:
            with self.db_session_factory() as db:
                db.execute(text("""
                    UPDATE workflow_packages 
                    SET usage_count = usage_count + 1 
                    WHERE id = :package_id
                """), {'package_id': package_id})
                db.commit()
        except Exception as e:
            logger.warning(f"Failed to increment usage count: {e}")
