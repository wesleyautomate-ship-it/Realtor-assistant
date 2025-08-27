#!/usr/bin/env python3
"""
AI Action Engine for Conversational CRM & Workflow Automation
============================================================

This module handles natural language commands to perform CRM actions
such as updating lead status, logging interactions, and scheduling follow-ups.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
import dateparser

from rag_service import QueryIntent

logger = logging.getLogger(__name__)

@dataclass
class ActionPlan:
    """Represents a plan for an action to be executed"""
    action_type: str
    lead_id: Optional[int] = None
    details: Dict[str, Any] = None
    confirmation_message: str = ""
    requires_confirmation: bool = True

class ActionEngine:
    """
    Core action engine that handles CRM workflow automation
    """
    
    def __init__(self, db_session: Session, agent_id: int):
        self.db = db_session
        self.agent_id = agent_id
        
        # Valid lead statuses
        self.valid_statuses = [
            'new', 'contacted', 'qualified', 'negotiating', 'closed_won', 'closed_lost', 'follow_up'
        ]
        
        # Interaction types
        self.interaction_types = [
            'call', 'email', 'meeting', 'viewing', 'proposal', 'negotiation', 'closing'
        ]

    def _find_lead_by_name(self, name: str) -> Optional[Dict]:
        """Securely finds a lead belonging to the current agent"""
        try:
            result = self.db.execute(text("""
                SELECT id, name, status, email, phone 
                FROM leads 
                WHERE agent_id = :agent_id 
                AND name ILIKE :name_pattern
                ORDER BY created_at DESC
                LIMIT 1
            """), {
                "agent_id": self.agent_id,
                "name_pattern": f"%{name}%"
            })
            
            row = result.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "status": row[2],
                    "email": row[3],
                    "phone": row[4]
                }
            return None
        except Exception as e:
            logger.error(f"Error finding lead by name: {e}")
            return None

    def _parse_datetime(self, datetime_str: str) -> Optional[datetime]:
        """Parse natural language datetime strings"""
        try:
            # Handle common patterns
            if 'tomorrow' in datetime_str.lower():
                base_date = datetime.now() + timedelta(days=1)
            elif 'next week' in datetime_str.lower():
                base_date = datetime.now() + timedelta(days=7)
            else:
                base_date = datetime.now()
            
            # Extract time if present
            time_match = re.search(r'(\d{1,2}(?::\d{2})?\s*[ap]m)', datetime_str.lower())
            if time_match:
                time_str = time_match.group(1)
                parsed_time = dateparser.parse(time_str, settings={'PREFER_DATES_FROM': 'future'})
                if parsed_time:
                    return datetime.combine(base_date.date(), parsed_time.time())
            
            return base_date
        except Exception as e:
            logger.error(f"Error parsing datetime: {e}")
            return None

    def prepare_action(self, intent: QueryIntent, entities: Dict[str, Any]) -> ActionPlan:
        """
        Prepares a plan for an action and a confirmation message for the agent.
        """
        if intent == QueryIntent.UPDATE_LEAD:
            return self._prepare_update_lead_action(entities)
        elif intent == QueryIntent.LOG_INTERACTION:
            return self._prepare_log_interaction_action(entities)
        elif intent == QueryIntent.SCHEDULE_FOLLOW_UP:
            return self._prepare_schedule_follow_up_action(entities)
        else:
            return ActionPlan(
                action_type="unknown",
                confirmation_message="I'm not sure how to handle that request.",
                requires_confirmation=False
            )

    def _prepare_update_lead_action(self, entities: Dict[str, Any]) -> ActionPlan:
        """Prepare action plan for updating lead status"""
        lead_name = entities.get('lead_name')
        new_status = entities.get('new_status')
        
        if not lead_name or not new_status:
            return ActionPlan(
                action_type="update_lead",
                confirmation_message="I need both a client name and a new status to update a lead. Please provide both.",
                requires_confirmation=False
            )
        
        # Find the lead
        lead = self._find_lead_by_name(lead_name)
        if not lead:
            return ActionPlan(
                action_type="update_lead",
                confirmation_message=f"I couldn't find a lead named '{lead_name}' in your database. Please check the name and try again.",
                requires_confirmation=False
            )
        
        # Validate status
        if new_status.lower() not in self.valid_statuses:
            valid_statuses_str = ", ".join(self.valid_statuses)
            return ActionPlan(
                action_type="update_lead",
                confirmation_message=f"'{new_status}' is not a valid status. Valid statuses are: {valid_statuses_str}",
                requires_confirmation=False
            )
        
        # Check if status is already the same
        if lead['status'] == new_status.lower():
            return ActionPlan(
                action_type="update_lead",
                confirmation_message=f"Lead '{lead['name']}' is already marked as '{new_status}'.",
                requires_confirmation=False
            )
        
        return ActionPlan(
            action_type="update_lead",
            lead_id=lead['id'],
            details={
                "status": new_status.lower(),
                "lead_name": lead['name'],
                "current_status": lead['status']
            },
            confirmation_message=f"Okay, I will update the status for lead '{lead['name']}' from '{lead['status']}' to '{new_status}'. Shall I proceed?",
            requires_confirmation=True
        )

    def _prepare_log_interaction_action(self, entities: Dict[str, Any]) -> ActionPlan:
        """Prepare action plan for logging an interaction"""
        lead_name = entities.get('lead_name')
        interaction_notes = entities.get('interaction_notes')
        
        if not lead_name:
            return ActionPlan(
                action_type="log_interaction",
                confirmation_message="I need a client name to log an interaction. Please specify which client this interaction was with.",
                requires_confirmation=False
            )
        
        # Find the lead
        lead = self._find_lead_by_name(lead_name)
        if not lead:
            return ActionPlan(
                action_type="log_interaction",
                confirmation_message=f"I couldn't find a lead named '{lead_name}' in your database. Please check the name and try again.",
                requires_confirmation=False
            )
        
        # Determine interaction type from notes
        interaction_type = 'general'
        if interaction_notes:
            notes_lower = interaction_notes.lower()
            if any(word in notes_lower for word in ['call', 'phone', 'telephone']):
                interaction_type = 'call'
            elif any(word in notes_lower for word in ['meeting', 'appointment', 'visit']):
                interaction_type = 'meeting'
            elif any(word in notes_lower for word in ['viewing', 'property', 'show']):
                interaction_type = 'viewing'
            elif any(word in notes_lower for word in ['email', 'mail']):
                interaction_type = 'email'
        
        return ActionPlan(
            action_type="log_interaction",
            lead_id=lead['id'],
            details={
                "interaction_type": interaction_type,
                "notes": interaction_notes or "Interaction logged via chat",
                "lead_name": lead['name']
            },
            confirmation_message=f"I will log a {interaction_type} interaction for '{lead['name']}' with the note: '{interaction_notes or 'No specific notes provided'}'. Shall I proceed?",
            requires_confirmation=True
        )

    def _prepare_schedule_follow_up_action(self, entities: Dict[str, Any]) -> ActionPlan:
        """Prepare action plan for scheduling a follow-up"""
        lead_name = entities.get('lead_name')
        task_datetime = entities.get('task_datetime')
        
        if not lead_name:
            return ActionPlan(
                action_type="schedule_follow_up",
                confirmation_message="I need a client name to schedule a follow-up. Please specify which client this is for.",
                requires_confirmation=False
            )
        
        # Find the lead
        lead = self._find_lead_by_name(lead_name)
        if not lead:
            return ActionPlan(
                action_type="schedule_follow_up",
                confirmation_message=f"I couldn't find a lead named '{lead_name}' in your database. Please check the name and try again.",
                requires_confirmation=False
            )
        
        # Parse datetime
        scheduled_time = None
        if task_datetime:
            scheduled_time = self._parse_datetime(task_datetime)
        
        if not scheduled_time:
            # Default to tomorrow at 10 AM
            scheduled_time = datetime.now() + timedelta(days=1)
            scheduled_time = scheduled_time.replace(hour=10, minute=0, second=0, microsecond=0)
        
        return ActionPlan(
            action_type="schedule_follow_up",
            lead_id=lead['id'],
            details={
                "scheduled_time": scheduled_time,
                "lead_name": lead['name'],
                "appointment_type": "follow_up"
            },
            confirmation_message=f"I will schedule a follow-up for '{lead['name']}' on {scheduled_time.strftime('%B %d, %Y at %I:%M %p')}. Shall I proceed?",
            requires_confirmation=True
        )

    def execute_action(self, plan: ActionPlan) -> str:
        """
        Executes the confirmed action plan against the database.
        """
        try:
            if plan.action_type == "update_lead":
                return self._execute_update_lead(plan)
            elif plan.action_type == "log_interaction":
                return self._execute_log_interaction(plan)
            elif plan.action_type == "schedule_follow_up":
                return self._execute_schedule_follow_up(plan)
            else:
                return "Action could not be completed - unknown action type."
        except Exception as e:
            logger.error(f"Error executing action: {e}")
            return f"Error executing action: {str(e)}"

    def _execute_update_lead(self, plan: ActionPlan) -> str:
        """Execute lead status update"""
        try:
            # Log the change in lead_history
            self.db.execute(text("""
                INSERT INTO lead_history (lead_id, status_from, status_to, changed_by_agent_id)
                VALUES (:lead_id, :status_from, :status_to, :agent_id)
            """), {
                "lead_id": plan.lead_id,
                "status_from": plan.details["current_status"],
                "status_to": plan.details["status"],
                "agent_id": self.agent_id
            })
            
            # Update the lead status
            self.db.execute(text("""
                UPDATE leads 
                SET status = :new_status, updated_at = CURRENT_TIMESTAMP
                WHERE id = :lead_id AND agent_id = :agent_id
            """), {
                "new_status": plan.details["status"],
                "lead_id": plan.lead_id,
                "agent_id": self.agent_id
            })
            
            self.db.commit()
            return f"✅ Done! The status for {plan.details['lead_name']} has been updated from '{plan.details['current_status']}' to '{plan.details['status']}'."
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating lead: {e}")
            return f"❌ Error updating lead status: {str(e)}"

    def _execute_log_interaction(self, plan: ActionPlan) -> str:
        """Execute interaction logging"""
        try:
            # Log the interaction
            self.db.execute(text("""
                INSERT INTO client_interactions (lead_id, agent_id, interaction_type, notes, interaction_date)
                VALUES (:lead_id, :agent_id, :interaction_type, :notes, CURRENT_TIMESTAMP)
            """), {
                "lead_id": plan.lead_id,
                "agent_id": self.agent_id,
                "interaction_type": plan.details["interaction_type"],
                "notes": plan.details["notes"]
            })
            
            # Update last_contacted timestamp on lead
            self.db.execute(text("""
                UPDATE leads 
                SET last_contacted = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                WHERE id = :lead_id AND agent_id = :agent_id
            """), {
                "lead_id": plan.lead_id,
                "agent_id": self.agent_id
            })
            
            self.db.commit()
            return f"✅ Done! I've logged a {plan.details['interaction_type']} interaction for {plan.details['lead_name']} with the note: '{plan.details['notes']}'"
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error logging interaction: {e}")
            return f"❌ Error logging interaction: {str(e)}"

    def _execute_schedule_follow_up(self, plan: ActionPlan) -> str:
        """Execute follow-up scheduling"""
        try:
            # Schedule the appointment
            self.db.execute(text("""
                INSERT INTO appointments (agent_id, client_name, appointment_date, appointment_time, appointment_type, notes, status)
                VALUES (:agent_id, :client_name, :appointment_date, :appointment_time, :appointment_type, :notes, 'scheduled')
            """), {
                "agent_id": self.agent_id,
                "client_name": plan.details["lead_name"],
                "appointment_date": plan.details["scheduled_time"].date(),
                "appointment_time": plan.details["scheduled_time"].time(),
                "appointment_type": plan.details["appointment_type"],
                "notes": f"Follow-up scheduled via chat interface"
            })
            
            self.db.commit()
            return f"✅ Done! I've scheduled a follow-up for {plan.details['lead_name']} on {plan.details['scheduled_time'].strftime('%B %d, %Y at %I:%M %p')}."
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error scheduling follow-up: {e}")
            return f"❌ Error scheduling follow-up: {str(e)}"

