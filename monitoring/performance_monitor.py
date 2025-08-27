"""
Performance monitoring service for RAG Real Estate System
"""
import asyncio
import time
import psutil
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import logging
from collections import defaultdict, deque
import redis
from prometheus_client import Gauge, Histogram, Counter

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetric:
    """Performance metric data structure"""
    timestamp: datetime
    metric_name: str
    value: float
    labels: Dict[str, str]
    metadata: Dict[str, Any]

class PerformanceMonitor:
    """Comprehensive performance monitoring service"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client
        self.metrics_history = defaultdict(lambda: deque(maxlen=1000))
        self.alert_thresholds = {
            'cpu_usage': 80.0,
            'memory_usage': 85.0,
            'response_time_p95': 2.0,
            'error_rate': 5.0,
            'database_connections': 80,
            'queue_size': 100
        }
        
        # Performance gauges
        self.cpu_gauge = Gauge('system_cpu_usage_percent', 'CPU usage percentage')
        self.memory_gauge = Gauge('system_memory_usage_percent', 'Memory usage percentage')
        self.disk_gauge = Gauge('system_disk_usage_percent', 'Disk usage percentage')
        self.network_gauge = Gauge('system_network_io_bytes', 'Network I/O in bytes')
        
        # Application performance metrics
        self.response_time_gauge = Gauge('app_response_time_seconds', 'Application response time')
        self.error_rate_gauge = Gauge('app_error_rate_percent', 'Application error rate')
        self.active_connections_gauge = Gauge('app_active_connections', 'Active connections')
        
        # RAG-specific metrics
        self.rag_latency_gauge = Gauge('rag_query_latency_seconds', 'RAG query latency')
        self.vector_search_gauge = Gauge('vector_search_duration_seconds', 'Vector search duration')
        self.llm_response_gauge = Gauge('llm_response_time_seconds', 'LLM response time')
        
        self.monitoring_active = False
        self.monitoring_thread = None
    
    async def start_monitoring(self):
        """Start the performance monitoring service"""
        if self.monitoring_active:
            logger.warning("Performance monitoring is already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        logger.info("Performance monitoring started")
    
    async def stop_monitoring(self):
        """Stop the performance monitoring service"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Performance monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                self._collect_system_metrics()
                self._collect_application_metrics()
                self._check_alerts()
                time.sleep(10)  # Collect metrics every 10 seconds
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(30)  # Wait longer on error
    
    def _collect_system_metrics(self):
        """Collect system-level performance metrics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_gauge.set(cpu_percent)
            self._store_metric('cpu_usage', cpu_percent, {'type': 'system'})
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self.memory_gauge.set(memory_percent)
            self._store_metric('memory_usage', memory_percent, {'type': 'system'})
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.disk_gauge.set(disk_percent)
            self._store_metric('disk_usage', disk_percent, {'type': 'system'})
            
            # Network I/O
            network = psutil.net_io_counters()
            network_bytes = network.bytes_sent + network.bytes_recv
            self.network_gauge.set(network_bytes)
            self._store_metric('network_io', network_bytes, {'type': 'system'})
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
    
    def _collect_application_metrics(self):
        """Collect application-level performance metrics"""
        try:
            # Get metrics from Redis if available
            if self.redis_client:
                # Response time
                response_time = self.redis_client.get('metrics:response_time')
                if response_time:
                    self.response_time_gauge.set(float(response_time))
                
                # Error rate
                error_rate = self.redis_client.get('metrics:error_rate')
                if error_rate:
                    self.error_rate_gauge.set(float(error_rate))
                
                # Active connections
                active_connections = self.redis_client.get('metrics:active_connections')
                if active_connections:
                    self.active_connections_gauge.set(int(active_connections))
                
                # RAG metrics
                rag_latency = self.redis_client.get('metrics:rag_latency')
                if rag_latency:
                    self.rag_latency_gauge.set(float(rag_latency))
                
                vector_search_time = self.redis_client.get('metrics:vector_search_time')
                if vector_search_time:
                    self.vector_search_gauge.set(float(vector_search_time))
                
                llm_response_time = self.redis_client.get('metrics:llm_response_time')
                if llm_response_time:
                    self.llm_response_gauge.set(float(llm_response_time))
                    
        except Exception as e:
            logger.error(f"Error collecting application metrics: {e}")
    
    def _check_alerts(self):
        """Check for performance alerts"""
        try:
            alerts = []
            
            # Check CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > self.alert_thresholds['cpu_usage']:
                alerts.append({
                    'severity': 'warning',
                    'metric': 'cpu_usage',
                    'value': cpu_usage,
                    'threshold': self.alert_thresholds['cpu_usage'],
                    'message': f'CPU usage is high: {cpu_usage:.1f}%'
                })
            
            # Check memory usage
            memory = psutil.virtual_memory()
            if memory.percent > self.alert_thresholds['memory_usage']:
                alerts.append({
                    'severity': 'warning',
                    'metric': 'memory_usage',
                    'value': memory.percent,
                    'threshold': self.alert_thresholds['memory_usage'],
                    'message': f'Memory usage is high: {memory.percent:.1f}%'
                })
            
            # Store alerts in Redis if available
            if alerts and self.redis_client:
                for alert in alerts:
                    alert['timestamp'] = datetime.now().isoformat()
                    self.redis_client.lpush('alerts:performance', json.dumps(alert))
                    self.redis_client.ltrim('alerts:performance', 0, 99)  # Keep last 100 alerts
            
            # Log alerts
            for alert in alerts:
                if alert['severity'] == 'critical':
                    logger.critical(alert['message'])
                elif alert['severity'] == 'warning':
                    logger.warning(alert['message'])
                    
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
    
    def _store_metric(self, metric_name: str, value: float, labels: Dict[str, str]):
        """Store a performance metric"""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name=metric_name,
            value=value,
            labels=labels,
            metadata={}
        )
        
        self.metrics_history[metric_name].append(metric)
        
        # Store in Redis if available
        if self.redis_client:
            try:
                metric_data = {
                    'timestamp': metric.timestamp.isoformat(),
                    'value': metric.value,
                    'labels': metric.labels,
                    'metadata': metric.metadata
                }
                self.redis_client.lpush(f'metrics:{metric_name}', json.dumps(metric_data))
                self.redis_client.ltrim(f'metrics:{metric_name}', 0, 999)  # Keep last 1000 metrics
            except Exception as e:
                logger.error(f"Error storing metric in Redis: {e}")
    
    def get_metrics_summary(self, metric_name: str, minutes: int = 60) -> Dict[str, Any]:
        """Get metrics summary for the specified time period"""
        try:
            cutoff_time = datetime.now() - timedelta(minutes=minutes)
            metrics = [
                m for m in self.metrics_history[metric_name]
                if m.timestamp >= cutoff_time
            ]
            
            if not metrics:
                return {
                    'metric_name': metric_name,
                    'count': 0,
                    'min': 0,
                    'max': 0,
                    'avg': 0,
                    'p95': 0,
                    'p99': 0
                }
            
            values = [m.value for m in metrics]
            values.sort()
            
            return {
                'metric_name': metric_name,
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'avg': sum(values) / len(values),
                'p95': values[int(len(values) * 0.95)] if len(values) > 0 else 0,
                'p99': values[int(len(values) * 0.99)] if len(values) > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting metrics summary: {e}")
            return {}
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report"""
        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'system_metrics': {},
                'application_metrics': {},
                'alerts': []
            }
            
            # System metrics
            report['system_metrics'] = {
                'cpu_usage': self.get_metrics_summary('cpu_usage', 5),
                'memory_usage': self.get_metrics_summary('memory_usage', 5),
                'disk_usage': self.get_metrics_summary('disk_usage', 5),
                'network_io': self.get_metrics_summary('network_io', 5)
            }
            
            # Application metrics (if available in Redis)
            if self.redis_client:
                try:
                    # Get recent alerts
                    alerts = self.redis_client.lrange('alerts:performance', 0, 9)
                    report['alerts'] = [json.loads(alert) for alert in alerts]
                    
                    # Get application metrics
                    app_metrics = ['response_time', 'error_rate', 'rag_latency', 'vector_search_time']
                    for metric in app_metrics:
                        metric_data = self.redis_client.lrange(f'metrics:{metric}', 0, 99)
                        if metric_data:
                            values = [json.loads(m)['value'] for m in metric_data]
                            report['application_metrics'][metric] = {
                                'count': len(values),
                                'avg': sum(values) / len(values) if values else 0,
                                'max': max(values) if values else 0
                            }
                except Exception as e:
                    logger.error(f"Error getting application metrics: {e}")
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {}
    
    def set_alert_threshold(self, metric: str, threshold: float):
        """Set alert threshold for a metric"""
        self.alert_thresholds[metric] = threshold
        logger.info(f"Set alert threshold for {metric}: {threshold}")
    
    def get_alert_thresholds(self) -> Dict[str, float]:
        """Get current alert thresholds"""
        return self.alert_thresholds.copy()

class PerformanceAnalyzer:
    """Analyze performance patterns and provide insights"""
    
    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
    
    def analyze_performance_trends(self, metric_name: str, hours: int = 24) -> Dict[str, Any]:
        """Analyze performance trends for a metric"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            metrics = [
                m for m in self.monitor.metrics_history[metric_name]
                if m.timestamp >= cutoff_time
            ]
            
            if len(metrics) < 2:
                return {'trend': 'insufficient_data', 'message': 'Not enough data for trend analysis'}
            
            # Calculate trend
            values = [m.value for m in metrics]
            time_points = [(m.timestamp - cutoff_time).total_seconds() / 3600 for m in metrics]
            
            # Simple linear regression
            n = len(values)
            sum_x = sum(time_points)
            sum_y = sum(values)
            sum_xy = sum(x * y for x, y in zip(time_points, values))
            sum_x2 = sum(x * x for x in time_points)
            
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            
            # Determine trend
            if abs(slope) < 0.01:
                trend = 'stable'
            elif slope > 0:
                trend = 'increasing'
            else:
                trend = 'decreasing'
            
            return {
                'trend': trend,
                'slope': slope,
                'data_points': n,
                'current_value': values[-1],
                'average_value': sum_y / n,
                'min_value': min(values),
                'max_value': max(values)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing performance trends: {e}")
            return {'trend': 'error', 'message': str(e)}
    
    def identify_bottlenecks(self) -> List[Dict[str, Any]]:
        """Identify potential performance bottlenecks"""
        bottlenecks = []
        
        try:
            # Check CPU usage
            cpu_trend = self.analyze_performance_trends('cpu_usage', 1)
            if cpu_trend.get('trend') == 'increasing' and cpu_trend.get('current_value', 0) > 70:
                bottlenecks.append({
                    'type': 'cpu',
                    'severity': 'high' if cpu_trend['current_value'] > 85 else 'medium',
                    'description': f'CPU usage is increasing and currently at {cpu_trend["current_value"]:.1f}%',
                    'recommendation': 'Consider scaling up CPU resources or optimizing CPU-intensive operations'
                })
            
            # Check memory usage
            memory_trend = self.analyze_performance_trends('memory_usage', 1)
            if memory_trend.get('trend') == 'increasing' and memory_trend.get('current_value', 0) > 80:
                bottlenecks.append({
                    'type': 'memory',
                    'severity': 'high' if memory_trend['current_value'] > 90 else 'medium',
                    'description': f'Memory usage is increasing and currently at {memory_trend["current_value"]:.1f}%',
                    'recommendation': 'Check for memory leaks or consider increasing memory allocation'
                })
            
            # Check response time if available
            if 'response_time' in self.monitor.metrics_history:
                response_trend = self.analyze_performance_trends('response_time', 1)
                if response_trend.get('trend') == 'increasing' and response_trend.get('current_value', 0) > 1.0:
                    bottlenecks.append({
                        'type': 'response_time',
                        'severity': 'high' if response_trend['current_value'] > 2.0 else 'medium',
                        'description': f'Response time is increasing and currently at {response_trend["current_value"]:.2f}s',
                        'recommendation': 'Investigate slow database queries or external API calls'
                    })
            
        except Exception as e:
            logger.error(f"Error identifying bottlenecks: {e}")
        
        return bottlenecks
    
    def generate_optimization_recommendations(self) -> List[Dict[str, Any]]:
        """Generate optimization recommendations based on performance data"""
        recommendations = []
        
        try:
            # Analyze system metrics
            cpu_summary = self.monitor.get_metrics_summary('cpu_usage', 60)
            memory_summary = self.monitor.get_metrics_summary('memory_usage', 60)
            
            # CPU recommendations
            if cpu_summary.get('avg', 0) > 70:
                recommendations.append({
                    'category': 'cpu',
                    'priority': 'high' if cpu_summary['avg'] > 85 else 'medium',
                    'title': 'Optimize CPU Usage',
                    'description': f'Average CPU usage is {cpu_summary["avg"]:.1f}%',
                    'actions': [
                        'Review and optimize CPU-intensive operations',
                        'Consider implementing caching strategies',
                        'Scale up CPU resources if necessary'
                    ]
                })
            
            # Memory recommendations
            if memory_summary.get('avg', 0) > 80:
                recommendations.append({
                    'category': 'memory',
                    'priority': 'high' if memory_summary['avg'] > 90 else 'medium',
                    'title': 'Optimize Memory Usage',
                    'description': f'Average memory usage is {memory_summary["avg"]:.1f}%',
                    'actions': [
                        'Check for memory leaks in application code',
                        'Optimize data structures and algorithms',
                        'Consider implementing memory pooling',
                        'Increase memory allocation if necessary'
                    ]
                })
            
        except Exception as e:
            logger.error(f"Error generating optimization recommendations: {e}")
        
        return recommendations
