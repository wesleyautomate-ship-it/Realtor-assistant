"""
Smart Notification Service - Intelligent Alert System

This service provides intelligent notification capabilities including:
- Market opportunity alerts
- Price change notifications
- Client follow-up reminders
- Performance alerts
- Context-aware notifications
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import json
from enum import Enum
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationPriority(Enum):
    """Notification priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class NotificationType(Enum):
    """Notification types"""
    MARKET_OPPORTUNITY = "market_opportunity"
    PRICE_CHANGE = "price_change"
    CLIENT_FOLLOW_UP = "client_follow_up"
    PERFORMANCE_ALERT = "performance_alert"
    SYSTEM_ALERT = "system_alert"
    INVESTMENT_INSIGHT = "investment_insight"
    MARKET_TREND = "market_trend"
    PROPERTY_UPDATE = "property_update"

class NotificationStatus(Enum):
    """Notification status"""
    ACTIVE = "active"
    READ = "read"
    ARCHIVED = "archived"
    EXPIRED = "expired"

class SmartNotificationService:
    """Service for intelligent notifications and alerts"""
    
    def __init__(self):
        self.notifications = []
        self.notification_rules = self._load_notification_rules()
        self.user_preferences = {}
        self.alert_history = []
        
    def _load_notification_rules(self) -> Dict[str, Any]:
        """Load notification rules and triggers"""
        return {
            'market_opportunity': {
                'triggers': ['new_property_listing', 'price_drop', 'market_shift'],
                'priority': NotificationPriority.HIGH,
                'auto_expire_hours': 72,
                'max_frequency_hours': 24
            },
            'price_change': {
                'triggers': ['significant_price_change', 'market_correction', 'neighborhood_shift'],
                'priority': NotificationPriority.MEDIUM,
                'auto_expire_hours': 48,
                'max_frequency_hours': 12
            },
            'client_follow_up': {
                'triggers': ['client_inactivity', 'deal_stagnation', 'opportunity_window'],
                'priority': NotificationPriority.MEDIUM,
                'auto_expire_hours': 168,  # 1 week
                'max_frequency_hours': 24
            },
            'performance_alert': {
                'triggers': ['goal_milestone', 'performance_drop', 'achievement_celebration'],
                'priority': NotificationPriority.HIGH,
                'auto_expire_hours': 336,  # 2 weeks
                'max_frequency_hours': 48
            },
            'system_alert': {
                'triggers': ['system_maintenance', 'feature_update', 'security_alert'],
                'priority': NotificationPriority.URGENT,
                'auto_expire_hours': 24,
                'max_frequency_hours': 1
            },
            'investment_insight': {
                'triggers': ['market_analysis', 'investment_timing', 'risk_alert'],
                'priority': NotificationPriority.MEDIUM,
                'auto_expire_hours': 96,
                'max_frequency_hours': 24
            },
            'market_trend': {
                'triggers': ['trend_emergence', 'market_shift', 'seasonal_pattern'],
                'priority': NotificationPriority.LOW,
                'auto_expire_hours': 120,
                'max_frequency_hours': 48
            },
            'property_update': {
                'triggers': ['status_change', 'new_photos', 'price_update'],
                'priority': NotificationPriority.LOW,
                'auto_expire_hours': 72,
                'max_frequency_hours': 12
            }
        }
    
    async def create_smart_notification(
        self,
        notification_type: str,
        user_id: int,
        title: str,
        message: str,
        priority: Optional[str] = None,
        context_data: Optional[Dict[str, Any]] = None,
        custom_message: Optional[str] = None,
        action_required: bool = False
    ) -> Dict[str, Any]:
        """Create an intelligent notification"""
        try:
            # Validate notification type
            if notification_type not in [nt.value for nt in NotificationType]:
                raise ValueError(f"Invalid notification type: {notification_type}")
            
            # Get notification rules
            rules = self.notification_rules.get(notification_type, {})
            
            # Set priority based on rules or user input
            if not priority:
                priority = rules.get('priority', NotificationPriority.MEDIUM).value
            
            # Check frequency limits
            if not await self._check_frequency_limit(user_id, notification_type, rules):
                logger.info(f"Frequency limit reached for {notification_type} notification for user {user_id}")
                return None
            
            # Create notification
            notification = {
                'id': f"notif_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id}",
                'type': notification_type,
                'user_id': user_id,
                'title': title,
                'message': custom_message or message,
                'priority': priority,
                'status': NotificationStatus.ACTIVE.value,
                'context_data': context_data or {},
                'action_required': action_required,
                'created_at': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(hours=rules.get('auto_expire_hours', 48))).isoformat(),
                'read_at': None,
                'archived_at': None
            }
            
            # Store notification
            self.notifications.append(notification)
            
            # Log alert
            await self._log_alert(notification)
            
            logger.info(f"Smart notification created: {notification['id']} for user {user_id}")
            return notification
            
        except Exception as e:
            logger.error(f"Error creating smart notification: {e}")
            raise
    
    async def create_market_opportunity_alert(
        self,
        user_id: int,
        opportunity_type: str,
        location: str,
        property_type: str,
        confidence_score: float,
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a market opportunity alert"""
        try:
            title = f"New Investment Opportunity in {location}"
            
            if confidence_score >= 0.8:
                priority = NotificationPriority.HIGH.value
                message = f"High-confidence {opportunity_type} opportunity detected in {location} for {property_type} properties."
            elif confidence_score >= 0.6:
                priority = NotificationPriority.MEDIUM.value
                message = f"Moderate-confidence {opportunity_type} opportunity detected in {location} for {property_type} properties."
            else:
                priority = NotificationPriority.LOW.value
                message = f"Potential {opportunity_type} opportunity detected in {location} for {property_type} properties."
            
            context_data = context_data or {}
            context_data.update({
                'opportunity_type': opportunity_type,
                'location': location,
                'property_type': property_type,
                'confidence_score': confidence_score,
                'detected_at': datetime.now().isoformat()
            })
            
            return await self.create_smart_notification(
                notification_type=NotificationType.MARKET_OPPORTUNITY.value,
                user_id=user_id,
                title=title,
                message=message,
                priority=priority,
                context_data=context_data,
                action_required=True
            )
            
        except Exception as e:
            logger.error(f"Error creating market opportunity alert: {e}")
            raise
    
    async def create_price_change_alert(
        self,
        user_id: int,
        property_id: str,
        old_price: float,
        new_price: float,
        change_percentage: float,
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a price change alert"""
        try:
            # Determine alert significance
            if abs(change_percentage) >= 10:
                priority = NotificationPriority.HIGH.value
                significance = "significant"
            elif abs(change_percentage) >= 5:
                priority = NotificationPriority.MEDIUM.value
                significance = "moderate"
            else:
                priority = NotificationPriority.LOW.value
                significance = "minor"
            
            direction = "increased" if change_percentage > 0 else "decreased"
            title = f"Price {direction} for Property {property_id}"
            message = f"Property {property_id} price has {direction} by {abs(change_percentage):.1f}% ({significance} change)."
            
            context_data = context_data or {}
            context_data.update({
                'property_id': property_id,
                'old_price': old_price,
                'new_price': new_price,
                'change_percentage': change_percentage,
                'change_direction': direction,
                'significance': significance
            })
            
            return await self.create_smart_notification(
                notification_type=NotificationType.PRICE_CHANGE.value,
                user_id=user_id,
                title=title,
                message=message,
                priority=priority,
                context_data=context_data,
                action_required=False
            )
            
        except Exception as e:
            logger.error(f"Error creating price change alert: {e}")
            raise
    
    async def create_client_follow_up_reminder(
        self,
        user_id: int,
        client_id: str,
        client_name: str,
        last_contact: datetime,
        follow_up_type: str,
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a client follow-up reminder"""
        try:
            days_since_contact = (datetime.now() - last_contact).days
            
            if days_since_contact >= 30:
                priority = NotificationPriority.HIGH.value
                urgency = "urgent"
            elif days_since_contact >= 14:
                priority = NotificationPriority.MEDIUM.value
                urgency = "important"
            else:
                priority = NotificationPriority.LOW.value
                urgency = "routine"
            
            title = f"Follow-up Reminder: {client_name}"
            message = f"Client {client_name} hasn't been contacted for {days_since_contact} days. {follow_up_type} follow-up is {urgency}."
            
            context_data = context_data or {}
            context_data.update({
                'client_id': client_id,
                'client_name': client_name,
                'last_contact': last_contact.isoformat(),
                'days_since_contact': days_since_contact,
                'follow_up_type': follow_up_type,
                'urgency': urgency
            })
            
            return await self.create_smart_notification(
                notification_type=NotificationType.CLIENT_FOLLOW_UP.value,
                user_id=user_id,
                title=title,
                message=message,
                priority=priority,
                context_data=context_data,
                action_required=True
            )
            
        except Exception as e:
            logger.error(f"Error creating client follow-up reminder: {e}")
            raise
    
    async def create_performance_alert(
        self,
        user_id: int,
        alert_type: str,
        metric_name: str,
        current_value: Union[int, float],
        target_value: Union[int, float],
        period: str,
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a performance alert"""
        try:
            # Calculate performance
            if target_value > 0:
                performance_percentage = (current_value / target_value) * 100
            else:
                performance_percentage = 0
            
            # Determine alert type and priority
            if alert_type == 'milestone_achieved':
                priority = NotificationPriority.MEDIUM.value
                title = f"Goal Milestone Achieved: {metric_name}"
                message = f"Congratulations! You've achieved your {metric_name} goal for {period}."
            elif alert_type == 'performance_drop':
                if performance_percentage < 50:
                    priority = NotificationPriority.HIGH.value
                else:
                    priority = NotificationPriority.MEDIUM.value
                title = f"Performance Alert: {metric_name}"
                message = f"Your {metric_name} performance is at {performance_percentage:.1f}% of target for {period}."
            elif alert_type == 'achievement_celebration':
                priority = NotificationPriority.LOW.value
                title = f"Performance Celebration: {metric_name}"
                message = f"Great work! Your {metric_name} performance is {performance_percentage:.1f}% above target for {period}."
            else:
                priority = NotificationPriority.MEDIUM.value
                title = f"Performance Update: {metric_name}"
                message = f"Your {metric_name} performance update for {period}."
            
            context_data = context_data or {}
            context_data.update({
                'alert_type': alert_type,
                'metric_name': metric_name,
                'current_value': current_value,
                'target_value': target_value,
                'performance_percentage': performance_percentage,
                'period': period
            })
            
            return await self.create_smart_notification(
                notification_type=NotificationType.PERFORMANCE_ALERT.value,
                user_id=user_id,
                title=title,
                message=message,
                priority=priority,
                context_data=context_data,
                action_required=False
            )
            
        except Exception as e:
            logger.error(f"Error creating performance alert: {e}")
            raise
    
    async def get_user_notifications(
        self,
        user_id: int,
        status: Optional[str] = None,
        notification_type: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get notifications for a specific user with optional filters"""
        try:
            filtered_notifications = []
            
            for notification in self.notifications:
                if notification['user_id'] != user_id:
                    continue
                
                # Apply filters
                if status and notification['status'] != status:
                    continue
                if notification_type and notification['type'] != notification_type:
                    continue
                if priority and notification['priority'] != priority:
                    continue
                
                filtered_notifications.append(notification)
            
            # Sort by creation date (newest first) and apply limit
            sorted_notifications = sorted(
                filtered_notifications,
                key=lambda x: x['created_at'],
                reverse=True
            )[:limit]
            
            return sorted_notifications
            
        except Exception as e:
            logger.error(f"Error getting user notifications: {e}")
            return []
    
    async def mark_notification_read(self, notification_id: str, user_id: int) -> bool:
        """Mark a notification as read"""
        try:
            for notification in self.notifications:
                if (notification['id'] == notification_id and 
                    notification['user_id'] == user_id):
                    notification['status'] = NotificationStatus.READ.value
                    notification['read_at'] = datetime.now().isoformat()
                    logger.info(f"Notification {notification_id} marked as read")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            return False
    
    async def archive_notification(self, notification_id: str, user_id: int) -> bool:
        """Archive a notification"""
        try:
            for notification in self.notifications:
                if (notification['id'] == notification_id and 
                    notification['user_id'] == user_id):
                    notification['status'] = NotificationStatus.ARCHIVED.value
                    notification['archived_at'] = datetime.now().isoformat()
                    logger.info(f"Notification {notification_id} archived")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error archiving notification: {e}")
            return False
    
    async def delete_notification(self, notification_id: str, user_id: int) -> bool:
        """Delete a notification"""
        try:
            for i, notification in enumerate(self.notifications):
                if (notification['id'] == notification_id and 
                    notification['user_id'] == user_id):
                    del self.notifications[i]
                    logger.info(f"Notification {notification_id} deleted")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error deleting notification: {e}")
            return False
    
    async def get_notification_summary(self, user_id: int) -> Dict[str, Any]:
        """Get a summary of user notifications"""
        try:
            user_notifications = [n for n in self.notifications if n['user_id'] == user_id]
            
            summary = {
                'total_notifications': len(user_notifications),
                'unread_count': len([n for n in user_notifications if n['status'] == NotificationStatus.ACTIVE.value]),
                'high_priority_count': len([n for n in user_notifications if n['priority'] == NotificationPriority.HIGH.value and n['status'] == NotificationStatus.ACTIVE.value]),
                'urgent_count': len([n for n in user_notifications if n['priority'] == NotificationPriority.URGENT.value and n['status'] == NotificationStatus.ACTIVE.value]),
                'action_required_count': len([n for n in user_notifications if n['action_required'] and n['status'] == NotificationStatus.ACTIVE.value]),
                'by_type': {},
                'by_priority': {}
            }
            
            # Count by type
            for notification in user_notifications:
                if notification['status'] == NotificationStatus.ACTIVE.value:
                    notif_type = notification['type']
                    summary['by_type'][notif_type] = summary['by_type'].get(notif_type, 0) + 1
                    
                    priority = notification['priority']
                    summary['by_priority'][priority] = summary['by_priority'].get(priority, 0) + 1
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting notification summary: {e}")
            return {}
    
    async def _check_frequency_limit(
        self,
        user_id: int,
        notification_type: str,
        rules: Dict[str, Any]
    ) -> bool:
        """Check if notification frequency limit is reached"""
        try:
            max_frequency_hours = rules.get('max_frequency_hours', 24)
            cutoff_time = datetime.now() - timedelta(hours=max_frequency_hours)
            
            # Count recent notifications of this type for this user
            recent_count = 0
            for notification in self.notifications:
                if (notification['user_id'] == user_id and
                    notification['type'] == notification_type and
                    notification['created_at'] > cutoff_time.isoformat()):
                    recent_count += 1
            
            # Allow if under limit (default limit is 1 per frequency period)
            return recent_count < 1
            
        except Exception as e:
            logger.error(f"Error checking frequency limit: {e}")
            return True  # Allow if check fails
    
    async def _log_alert(self, notification: Dict[str, Any]) -> None:
        """Log alert for monitoring and analytics"""
        try:
            alert_log = {
                'notification_id': notification['id'],
                'type': notification['type'],
                'user_id': notification['user_id'],
                'priority': notification['priority'],
                'created_at': notification['created_at'],
                'action_required': notification['action_required']
            }
            
            self.alert_history.append(alert_log)
            
            # Keep only last 1000 alerts
            if len(self.alert_history) > 1000:
                self.alert_history = self.alert_history[-1000:]
                
        except Exception as e:
            logger.error(f"Error logging alert: {e}")
    
    async def cleanup_expired_notifications(self) -> int:
        """Clean up expired notifications"""
        try:
            expired_count = 0
            current_time = datetime.now()
            
            for notification in self.notifications[:]:  # Copy list to avoid modification during iteration
                if notification['expires_at']:
                    expiry_time = datetime.fromisoformat(notification['expires_at'])
                    if current_time > expiry_time:
                        notification['status'] = NotificationStatus.EXPIRED.value
                        expired_count += 1
            
            logger.info(f"Cleaned up {expired_count} expired notifications")
            return expired_count
            
        except Exception as e:
            logger.error(f"Error cleaning up expired notifications: {e}")
            return 0
    
    async def get_alert_analytics(self, user_id: Optional[int] = None, days: int = 30) -> Dict[str, Any]:
        """Get analytics on notification patterns"""
        try:
            cutoff_time = datetime.now() - timedelta(days=days)
            
            if user_id:
                relevant_alerts = [a for a in self.alert_history if a['user_id'] == user_id and a['created_at'] > cutoff_time.isoformat()]
            else:
                relevant_alerts = [a for a in self.alert_history if a['created_at'] > cutoff_time.isoformat()]
            
            analytics = {
                'total_alerts': len(relevant_alerts),
                'by_type': {},
                'by_priority': {},
                'action_required_count': 0,
                'average_daily_alerts': len(relevant_alerts) / days if days > 0 else 0
            }
            
            for alert in relevant_alerts:
                # Count by type
                alert_type = alert['type']
                analytics['by_type'][alert_type] = analytics['by_type'].get(alert_type, 0) + 1
                
                # Count by priority
                priority = alert['priority']
                analytics['by_priority'][priority] = analytics['by_priority'].get(priority, 0) + 1
                
                # Count action required
                if alert.get('action_required', False):
                    analytics['action_required_count'] += 1
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting alert analytics: {e}")
            return {}

# Initialize service
smart_notification_service = SmartNotificationService()
