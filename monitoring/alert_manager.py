"""
Alert management system for RAG Real Estate System
"""
import asyncio
import json
import logging
import smtplib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import redis
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import aiohttp
import os

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertType(Enum):
    """Alert types"""
    PERFORMANCE = "performance"
    ERROR = "error"
    SECURITY = "security"
    SYSTEM = "system"
    BUSINESS = "business"
    CUSTOM = "custom"

class NotificationChannel(Enum):
    """Notification channels"""
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"
    PAGERDUTY = "pagerduty"

@dataclass
class Alert:
    """Alert data structure"""
    id: str
    type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    timestamp: datetime
    source: str
    metadata: Dict[str, Any]
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved: bool = False
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None

@dataclass
class NotificationConfig:
    """Notification configuration"""
    channel: NotificationChannel
    enabled: bool = True
    recipients: List[str] = None
    webhook_url: Optional[str] = None
    template: Optional[str] = None
    conditions: Dict[str, Any] = None

class AlertManager:
    """Comprehensive alert management system"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client
        self.notification_configs = self._initialize_notification_configs()
        self.alert_rules = self._initialize_alert_rules()
        self.alert_history = []
        self.active_alerts = {}
        
    def _initialize_notification_configs(self) -> Dict[NotificationChannel, NotificationConfig]:
        """Initialize notification configurations"""
        return {
            NotificationChannel.EMAIL: NotificationConfig(
                channel=NotificationChannel.EMAIL,
                enabled=True,
                recipients=["admin@rag-real-estate.com"],
                conditions={"severity": [AlertSeverity.ERROR, AlertSeverity.CRITICAL]}
            ),
            NotificationChannel.SLACK: NotificationConfig(
                channel=NotificationChannel.SLACK,
                enabled=True,
                webhook_url=os.getenv("SLACK_WEBHOOK_URL"),
                conditions={"severity": [AlertSeverity.WARNING, AlertSeverity.ERROR, AlertSeverity.CRITICAL]}
            ),
            NotificationChannel.WEBHOOK: NotificationConfig(
                channel=NotificationChannel.WEBHOOK,
                enabled=True,
                webhook_url=os.getenv("ALERT_WEBHOOK_URL"),
                conditions={"severity": [AlertSeverity.CRITICAL]}
            )
        }
    
    def _initialize_alert_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize alert rules"""
        return {
            "high_cpu_usage": {
                "condition": "cpu_usage > 80",
                "severity": AlertSeverity.WARNING,
                "type": AlertType.PERFORMANCE,
                "message_template": "CPU usage is high: {value}%"
            },
            "high_memory_usage": {
                "condition": "memory_usage > 85",
                "severity": AlertSeverity.WARNING,
                "type": AlertType.PERFORMANCE,
                "message_template": "Memory usage is high: {value}%"
            },
            "high_error_rate": {
                "condition": "error_rate > 5",
                "severity": AlertSeverity.ERROR,
                "type": AlertType.ERROR,
                "message_template": "Error rate is high: {value}%"
            },
            "service_down": {
                "condition": "service_status == 'down'",
                "severity": AlertSeverity.CRITICAL,
                "type": AlertType.SYSTEM,
                "message_template": "Service is down: {service_name}"
            },
            "database_connection_failed": {
                "condition": "db_connection_failed",
                "severity": AlertSeverity.CRITICAL,
                "type": AlertType.SYSTEM,
                "message_template": "Database connection failed"
            },
            "rag_query_timeout": {
                "condition": "rag_query_time > 30",
                "severity": AlertSeverity.WARNING,
                "type": AlertType.PERFORMANCE,
                "message_template": "RAG query timeout: {value}s"
            }
        }
    
    async def create_alert(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        title: str,
        message: str,
        source: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new alert"""
        try:
            alert_id = f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(message) % 10000}"
            
            alert = Alert(
                id=alert_id,
                type=alert_type,
                severity=severity,
                title=title,
                message=message,
                timestamp=datetime.now(),
                source=source,
                metadata=metadata or {}
            )
            
            # Store alert
            await self._store_alert(alert)
            
            # Add to active alerts
            self.active_alerts[alert_id] = alert
            
            # Send notifications
            await self._send_notifications(alert)
            
            logger.info(f"Alert created: {alert_id} - {title}")
            return alert_id
            
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return "alert_creation_failed"
    
    async def _store_alert(self, alert: Alert):
        """Store alert in Redis"""
        if not self.redis_client:
            return
        
        try:
            alert_data = asdict(alert)
            alert_data['timestamp'] = alert.timestamp.isoformat()
            alert_data['type'] = alert.type.value
            alert_data['severity'] = alert.severity.value
            
            # Store alert
            self.redis_client.lpush(f"alerts:{alert.id}", json.dumps(alert_data))
            self.redis_client.expire(f"alerts:{alert.id}", 86400 * 30)  # 30 days
            
            # Store in recent alerts
            self.redis_client.lpush("alerts:recent", json.dumps(alert_data))
            self.redis_client.ltrim("alerts:recent", 0, 999)  # Keep last 1000 alerts
            
            # Store by type
            self.redis_client.lpush(f"alerts:type:{alert.type.value}", json.dumps(alert_data))
            self.redis_client.ltrim(f"alerts:type:{alert.type.value}", 0, 999)
            
            # Store by severity
            self.redis_client.lpush(f"alerts:severity:{alert.severity.value}", json.dumps(alert_data))
            self.redis_client.ltrim(f"alerts:severity:{alert.severity.value}", 0, 999)
            
        except Exception as e:
            logger.error(f"Error storing alert: {e}")
    
    async def _send_notifications(self, alert: Alert):
        """Send notifications for an alert"""
        try:
            for channel, config in self.notification_configs.items():
                if not config.enabled:
                    continue
                
                # Check if alert meets notification conditions
                if not self._should_send_notification(alert, config):
                    continue
                
                # Send notification based on channel
                if channel == NotificationChannel.EMAIL:
                    await self._send_email_notification(alert, config)
                elif channel == NotificationChannel.SLACK:
                    await self._send_slack_notification(alert, config)
                elif channel == NotificationChannel.WEBHOOK:
                    await self._send_webhook_notification(alert, config)
                    
        except Exception as e:
            logger.error(f"Error sending notifications: {e}")
    
    def _should_send_notification(self, alert: Alert, config: NotificationConfig) -> bool:
        """Check if notification should be sent based on conditions"""
        if not config.conditions:
            return True
        
        # Check severity condition
        if "severity" in config.conditions:
            allowed_severities = config.conditions["severity"]
            if alert.severity not in allowed_severities:
                return False
        
        # Check type condition
        if "type" in config.conditions:
            allowed_types = config.conditions["type"]
            if alert.type not in allowed_types:
                return False
        
        return True
    
    async def _send_email_notification(self, alert: Alert, config: NotificationConfig):
        """Send email notification"""
        try:
            if not config.recipients:
                logger.warning("No email recipients configured")
                return
            
            # Email configuration
            smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_username = os.getenv("SMTP_USERNAME")
            smtp_password = os.getenv("SMTP_PASSWORD")
            
            if not all([smtp_username, smtp_password]):
                logger.warning("SMTP credentials not configured")
                return
            
            # Create email message
            msg = MimeMultipart()
            msg['From'] = smtp_username
            msg['To'] = ", ".join(config.recipients)
            msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.title}"
            
            # Email body
            body = f"""
            Alert Details:
            --------------
            Title: {alert.title}
            Message: {alert.message}
            Severity: {alert.severity.value}
            Type: {alert.type.value}
            Source: {alert.source}
            Timestamp: {alert.timestamp}
            
            Alert ID: {alert.id}
            
            Metadata: {json.dumps(alert.metadata, indent=2)}
            """
            
            msg.attach(MimeText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email notification sent for alert {alert.id}")
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
    
    async def _send_slack_notification(self, alert: Alert, config: NotificationConfig):
        """Send Slack notification"""
        try:
            if not config.webhook_url:
                logger.warning("Slack webhook URL not configured")
                return
            
            # Create Slack message
            color_map = {
                AlertSeverity.INFO: "#36a64f",
                AlertSeverity.WARNING: "#ff9500",
                AlertSeverity.ERROR: "#ff0000",
                AlertSeverity.CRITICAL: "#8b0000"
            }
            
            slack_message = {
                "attachments": [
                    {
                        "color": color_map.get(alert.severity, "#36a64f"),
                        "title": alert.title,
                        "text": alert.message,
                        "fields": [
                            {
                                "title": "Severity",
                                "value": alert.severity.value.upper(),
                                "short": True
                            },
                            {
                                "title": "Type",
                                "value": alert.type.value,
                                "short": True
                            },
                            {
                                "title": "Source",
                                "value": alert.source,
                                "short": True
                            },
                            {
                                "title": "Alert ID",
                                "value": alert.id,
                                "short": True
                            }
                        ],
                        "footer": "RAG Real Estate System",
                        "ts": int(alert.timestamp.timestamp())
                    }
                ]
            }
            
            # Send to Slack
            async with aiohttp.ClientSession() as session:
                async with session.post(config.webhook_url, json=slack_message) as response:
                    if response.status == 200:
                        logger.info(f"Slack notification sent for alert {alert.id}")
                    else:
                        logger.error(f"Failed to send Slack notification: {response.status}")
            
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")
    
    async def _send_webhook_notification(self, alert: Alert, config: NotificationConfig):
        """Send webhook notification"""
        try:
            if not config.webhook_url:
                logger.warning("Webhook URL not configured")
                return
            
            # Create webhook payload
            payload = {
                "alert_id": alert.id,
                "type": alert.type.value,
                "severity": alert.severity.value,
                "title": alert.title,
                "message": alert.message,
                "timestamp": alert.timestamp.isoformat(),
                "source": alert.source,
                "metadata": alert.metadata
            }
            
            # Send webhook
            async with aiohttp.ClientSession() as session:
                async with session.post(config.webhook_url, json=payload) as response:
                    if response.status == 200:
                        logger.info(f"Webhook notification sent for alert {alert.id}")
                    else:
                        logger.error(f"Failed to send webhook notification: {response.status}")
            
        except Exception as e:
            logger.error(f"Error sending webhook notification: {e}")
    
    async def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert"""
        try:
            if alert_id not in self.active_alerts:
                return False
            
            alert = self.active_alerts[alert_id]
            alert.acknowledged = True
            alert.acknowledged_by = acknowledged_by
            alert.acknowledged_at = datetime.now()
            
            # Update stored alert
            await self._store_alert(alert)
            
            logger.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
            return True
            
        except Exception as e:
            logger.error(f"Error acknowledging alert: {e}")
            return False
    
    async def resolve_alert(self, alert_id: str, resolved_by: str) -> bool:
        """Resolve an alert"""
        try:
            if alert_id not in self.active_alerts:
                return False
            
            alert = self.active_alerts[alert_id]
            alert.resolved = True
            alert.resolved_by = resolved_by
            alert.resolved_at = datetime.now()
            
            # Remove from active alerts
            del self.active_alerts[alert_id]
            
            # Update stored alert
            await self._store_alert(alert)
            
            logger.info(f"Alert {alert_id} resolved by {resolved_by}")
            return True
            
        except Exception as e:
            logger.error(f"Error resolving alert: {e}")
            return False
    
    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get list of active alerts"""
        try:
            alerts = []
            for alert in self.active_alerts.values():
                alert_data = asdict(alert)
                alert_data['timestamp'] = alert.timestamp.isoformat()
                alert_data['type'] = alert.type.value
                alert_data['severity'] = alert.severity.value
                alerts.append(alert_data)
            
            return alerts
            
        except Exception as e:
            logger.error(f"Error getting active alerts: {e}")
            return []
    
    async def get_alert_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get alert summary for the specified time period"""
        try:
            if not self.redis_client:
                return {}
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Get recent alerts
            recent_alerts = self.redis_client.lrange("alerts:recent", 0, 999)
            alerts = []
            
            for alert_json in recent_alerts:
                alert_data = json.loads(alert_json)
                alert_time = datetime.fromisoformat(alert_data['timestamp'])
                if alert_time >= cutoff_time:
                    alerts.append(alert_data)
            
            # Calculate statistics
            total_alerts = len(alerts)
            alerts_by_type = {}
            alerts_by_severity = {}
            active_alerts = 0
            
            for alert in alerts:
                alert_type = alert['type']
                severity = alert['severity']
                resolved = alert.get('resolved', False)
                
                alerts_by_type[alert_type] = alerts_by_type.get(alert_type, 0) + 1
                alerts_by_severity[severity] = alerts_by_severity.get(severity, 0) + 1
                
                if not resolved:
                    active_alerts += 1
            
            return {
                'total_alerts': total_alerts,
                'active_alerts': active_alerts,
                'alerts_by_type': alerts_by_type,
                'alerts_by_severity': alerts_by_severity,
                'time_period_hours': hours,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting alert summary: {e}")
            return {}
    
    def add_notification_config(self, channel: NotificationChannel, config: NotificationConfig):
        """Add or update notification configuration"""
        self.notification_configs[channel] = config
        logger.info(f"Notification config updated for {channel.value}")
    
    def add_alert_rule(self, rule_name: str, rule_config: Dict[str, Any]):
        """Add or update alert rule"""
        self.alert_rules[rule_name] = rule_config
        logger.info(f"Alert rule updated: {rule_name}")
    
    async def evaluate_alert_rules(self, metrics: Dict[str, Any]) -> List[str]:
        """Evaluate alert rules against current metrics"""
        triggered_alerts = []
        
        try:
            for rule_name, rule_config in self.alert_rules.items():
                # Simple condition evaluation (can be enhanced with expression parser)
                condition = rule_config['condition']
                
                # This is a simplified evaluation - in production, use a proper expression parser
                if self._evaluate_condition(condition, metrics):
                    alert_id = await self.create_alert(
                        alert_type=rule_config['type'],
                        severity=rule_config['severity'],
                        title=f"Rule triggered: {rule_name}",
                        message=rule_config['message_template'].format(**metrics),
                        source="alert_rule",
                        metadata={"rule_name": rule_name, "condition": condition}
                    )
                    triggered_alerts.append(alert_id)
            
        except Exception as e:
            logger.error(f"Error evaluating alert rules: {e}")
        
        return triggered_alerts
    
    def _evaluate_condition(self, condition: str, metrics: Dict[str, Any]) -> bool:
        """Evaluate a condition string against metrics"""
        try:
            # Simple condition evaluation - replace with proper expression parser
            if ">" in condition:
                parts = condition.split(">")
                metric_name = parts[0].strip()
                threshold = float(parts[1].strip())
                return metrics.get(metric_name, 0) > threshold
            elif "<" in condition:
                parts = condition.split("<")
                metric_name = parts[0].strip()
                threshold = float(parts[1].strip())
                return metrics.get(metric_name, 0) < threshold
            elif "==" in condition:
                parts = condition.split("==")
                metric_name = parts[0].strip()
                value = parts[1].strip().strip('"')
                return metrics.get(metric_name) == value
            else:
                return False
        except Exception as e:
            logger.error(f"Error evaluating condition '{condition}': {e}")
            return False
