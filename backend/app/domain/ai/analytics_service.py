"""
Performance Analytics Service - Real-Time Insights & Metrics

This service provides comprehensive analytics capabilities including:
- Agent performance metrics
- Market performance indicators
- Client analytics
- Business intelligence
- Real-time dashboards
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import json
import pandas as pd
import numpy as np
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Types of performance metrics"""
    COUNT = "count"
    PERCENTAGE = "percentage"
    CURRENCY = "currency"
    DURATION = "duration"
    RATIO = "ratio"
    SCORE = "score"

class TimePeriod(Enum):
    """Time periods for analytics"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class PerformanceAnalyticsService:
    """Service for performance analytics and business intelligence"""
    
    def __init__(self):
        self.metrics_data = {}
        self.goals_data = {}
        self.performance_history = []
        self.analytics_cache = {}
        
    async def get_agent_performance_metrics(
        self,
        user_id: int,
        period: str = "monthly",
        include_comparison: bool = True
    ) -> Dict[str, Any]:
        """Get comprehensive agent performance metrics"""
        try:
            logger.info(f"Getting performance metrics for user {user_id} for {period}")
            
            # Get current period metrics
            current_metrics = await self._calculate_agent_metrics(user_id, period)
            
            # Get comparison metrics if requested
            comparison_metrics = None
            if include_comparison:
                comparison_metrics = await self._get_comparison_metrics(user_id, period)
            
            # Calculate performance scores
            performance_scores = await self._calculate_performance_scores(current_metrics)
            
            # Get goal progress
            goal_progress = await self._get_goal_progress(user_id, period)
            
            # Compile comprehensive report
            performance_report = {
                'user_id': user_id,
                'period': period,
                'report_date': datetime.now().isoformat(),
                'current_metrics': current_metrics,
                'comparison_metrics': comparison_metrics,
                'performance_scores': performance_scores,
                'goal_progress': goal_progress,
                'insights': await self._generate_performance_insights(current_metrics, comparison_metrics),
                'recommendations': await self._generate_performance_recommendations(current_metrics, goal_progress)
            }
            
            return performance_report
            
        except Exception as e:
            logger.error(f"Error getting agent performance metrics: {e}")
            raise
    
    async def get_market_performance_indicators(
        self,
        location: str = "Dubai",
        property_type: str = "all",
        period: str = "monthly"
    ) -> Dict[str, Any]:
        """Get market performance indicators"""
        try:
            logger.info(f"Getting market performance for {location} {property_type} for {period}")
            
            # Calculate market metrics
            market_metrics = await self._calculate_market_metrics(location, property_type, period)
            
            # Get market trends
            market_trends = await self._analyze_market_trends(location, property_type, period)
            
            # Get market insights
            market_insights = await self._generate_market_insights(market_metrics, market_trends)
            
            return {
                'location': location,
                'property_type': property_type,
                'period': period,
                'report_date': datetime.now().isoformat(),
                'market_metrics': market_metrics,
                'market_trends': market_trends,
                'market_insights': market_insights,
                'market_score': await self._calculate_market_score(market_metrics)
            }
            
        except Exception as e:
            logger.error(f"Error getting market performance indicators: {e}")
            raise
    
    async def get_client_analytics(
        self,
        user_id: int,
        period: str = "monthly",
        include_behavior: bool = True
    ) -> Dict[str, Any]:
        """Get client analytics and behavior insights"""
        try:
            logger.info(f"Getting client analytics for user {user_id} for {period}")
            
            # Get client metrics
            client_metrics = await self._calculate_client_metrics(user_id, period)
            
            # Get client behavior if requested
            client_behavior = None
            if include_behavior:
                client_behavior = await self._analyze_client_behavior(user_id, period)
            
            # Get client insights
            client_insights = await self._generate_client_insights(client_metrics, client_behavior)
            
            return {
                'user_id': user_id,
                'period': period,
                'report_date': datetime.now().isoformat(),
                'client_metrics': client_metrics,
                'client_behavior': client_behavior,
                'client_insights': client_insights,
                'client_satisfaction_score': await self._calculate_client_satisfaction(client_metrics)
            }
            
        except Exception as e:
            logger.error(f"Error getting client analytics: {e}")
            raise
    
    async def get_business_intelligence_dashboard(
        self,
        user_id: int,
        include_team: bool = False
    ) -> Dict[str, Any]:
        """Get comprehensive business intelligence dashboard"""
        try:
            logger.info(f"Getting business intelligence dashboard for user {user_id}")
            
            # Get key performance indicators
            kpis = await self._get_key_performance_indicators(user_id)
            
            # Get business metrics
            business_metrics = await self._get_business_metrics(user_id)
            
            # Get team performance if requested
            team_performance = None
            if include_team:
                team_performance = await self._get_team_performance(user_id)
            
            # Get strategic insights
            strategic_insights = await self._generate_strategic_insights(kpis, business_metrics)
            
            return {
                'user_id': user_id,
                'report_date': datetime.now().isoformat(),
                'kpis': kpis,
                'business_metrics': business_metrics,
                'team_performance': team_performance,
                'strategic_insights': strategic_insights,
                'business_health_score': await self._calculate_business_health_score(kpis, business_metrics)
            }
            
        except Exception as e:
            logger.error(f"Error getting business intelligence dashboard: {e}")
            raise
    
    async def _calculate_agent_metrics(self, user_id: int, period: str) -> Dict[str, Any]:
        """Calculate agent performance metrics"""
        try:
            # This would typically query the database for actual metrics
            # For now, generate sample metrics
            
            metrics = {
                'leads_generated': np.random.randint(20, 100),
                'properties_viewed': np.random.randint(50, 200),
                'deals_closed': np.random.randint(5, 25),
                'revenue_generated': np.random.uniform(50000, 500000),
                'client_meetings': np.random.randint(30, 80),
                'follow_ups_completed': np.random.randint(100, 300),
                'response_time_minutes': np.random.uniform(15, 120),
                'client_satisfaction_score': np.random.uniform(4.0, 5.0),
                'deal_cycle_days': np.random.uniform(30, 90),
                'conversion_rate': np.random.uniform(0.15, 0.35)
            }
            
            # Calculate derived metrics
            metrics['average_deal_value'] = metrics['revenue_generated'] / metrics['deals_closed'] if metrics['deals_closed'] > 0 else 0
            metrics['lead_to_deal_rate'] = metrics['deals_closed'] / metrics['leads_generated'] if metrics['leads_generated'] > 0 else 0
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating agent metrics: {e}")
            return {}
    
    async def _get_comparison_metrics(self, user_id: int, period: str) -> Dict[str, Any]:
        """Get comparison metrics for the previous period"""
        try:
            # This would typically query historical data
            # For now, generate sample comparison data
            
            comparison = {
                'previous_period': f"previous_{period}",
                'leads_generated_change': np.random.uniform(-0.2, 0.3),
                'deals_closed_change': np.random.uniform(-0.15, 0.25),
                'revenue_change': np.random.uniform(-0.1, 0.4),
                'conversion_rate_change': np.random.uniform(-0.05, 0.1),
                'response_time_change': np.random.uniform(-0.3, 0.2)
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error getting comparison metrics: {e}")
            return {}
    
    async def _calculate_performance_scores(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance scores based on metrics"""
        try:
            scores = {}
            
            # Lead generation score (0-100)
            if metrics.get('leads_generated', 0) >= 80:
                scores['lead_generation'] = 100
            elif metrics.get('leads_generated', 0) >= 60:
                scores['lead_generation'] = 80
            elif metrics.get('leads_generated', 0) >= 40:
                scores['lead_generation'] = 60
            else:
                scores['lead_generation'] = 40
            
            # Deal closing score (0-100)
            if metrics.get('deals_closed', 0) >= 20:
                scores['deal_closing'] = 100
            elif metrics.get('deals_closed', 0) >= 15:
                scores['deal_closing'] = 80
            elif metrics.get('deals_closed', 0) >= 10:
                scores['deal_closing'] = 60
            else:
                scores['deal_closing'] = 40
            
            # Revenue performance score (0-100)
            if metrics.get('revenue_generated', 0) >= 400000:
                scores['revenue_performance'] = 100
            elif metrics.get('revenue_generated', 0) >= 300000:
                scores['revenue_performance'] = 80
            elif metrics.get('revenue_generated', 0) >= 200000:
                scores['revenue_performance'] = 60
            else:
                scores['revenue_performance'] = 40
            
            # Client satisfaction score (0-100)
            satisfaction = metrics.get('client_satisfaction_score', 0)
            scores['client_satisfaction'] = int(satisfaction * 20)  # Convert 5.0 scale to 100
            
            # Overall performance score
            scores['overall_performance'] = int(np.mean(list(scores.values())))
            
            return scores
            
        except Exception as e:
            logger.error(f"Error calculating performance scores: {e}")
            return {}
    
    async def _get_goal_progress(self, user_id: int, period: str) -> Dict[str, Any]:
        """Get goal progress for the current period"""
        try:
            # This would typically query goal data from database
            # For now, generate sample goal data
            
            goals = {
                'leads_target': 80,
                'deals_target': 20,
                'revenue_target': 400000,
                'satisfaction_target': 4.5
            }
            
            # Get current metrics for comparison
            current_metrics = await self._calculate_agent_metrics(user_id, period)
            
            # Calculate progress percentages
            progress = {
                'leads_progress': min(100, (current_metrics.get('leads_generated', 0) / goals['leads_target']) * 100),
                'deals_progress': min(100, (current_metrics.get('deals_closed', 0) / goals['deals_target']) * 100),
                'revenue_progress': min(100, (current_metrics.get('revenue_generated', 0) / goals['revenue_target']) * 100),
                'satisfaction_progress': min(100, (current_metrics.get('client_satisfaction_score', 0) / goals['satisfaction_target']) * 100)
            }
            
            # Calculate overall progress
            progress['overall_progress'] = np.mean(list(progress.values()))
            
            return {
                'goals': goals,
                'progress': progress,
                'status': 'on_track' if progress['overall_progress'] >= 80 else 'needs_attention'
            }
            
        except Exception as e:
            logger.error(f"Error getting goal progress: {e}")
            return {}
    
    async def _calculate_market_metrics(self, location: str, property_type: str, period: str) -> Dict[str, Any]:
        """Calculate market performance metrics"""
        try:
            # This would typically query market data
            # For now, generate sample market metrics
            
            metrics = {
                'total_properties': np.random.randint(500, 2000),
                'average_price': np.random.uniform(800000, 3000000),
                'price_change_percentage': np.random.uniform(-0.15, 0.25),
                'days_on_market': np.random.uniform(30, 120),
                'inventory_level': np.random.uniform(0.8, 1.5),
                'demand_score': np.random.uniform(0.6, 0.95),
                'supply_score': np.random.uniform(0.4, 0.9),
                'market_activity': np.random.uniform(0.5, 0.9)
            }
            
            # Calculate derived metrics
            metrics['price_per_sqft'] = metrics['average_price'] / np.random.uniform(800, 2000)
            metrics['market_balance'] = metrics['demand_score'] / metrics['supply_score'] if metrics['supply_score'] > 0 else 0
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating market metrics: {e}")
            return {}
    
    async def _analyze_market_trends(self, location: str, property_type: str, period: str) -> Dict[str, Any]:
        """Analyze market trends"""
        try:
            trends = {
                'price_trend': 'increasing' if np.random.random() > 0.5 else 'decreasing',
                'demand_trend': 'strong' if np.random.random() > 0.4 else 'moderate',
                'supply_trend': 'balanced' if np.random.random() > 0.5 else 'constrained',
                'market_volatility': np.random.uniform(0.1, 0.4),
                'seasonal_pattern': 'peak' if np.random.random() > 0.6 else 'normal',
                'forecast_confidence': np.random.uniform(0.7, 0.95)
            }
            
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing market trends: {e}")
            return {}
    
    async def _calculate_client_metrics(self, user_id: int, period: str) -> Dict[str, Any]:
        """Calculate client-related metrics"""
        try:
            metrics = {
                'total_clients': np.random.randint(50, 200),
                'active_clients': np.random.randint(30, 120),
                'new_clients': np.random.randint(10, 40),
                'client_retention_rate': np.random.uniform(0.7, 0.95),
                'average_client_value': np.random.uniform(50000, 200000),
                'client_satisfaction': np.random.uniform(4.0, 5.0),
                'response_time_hours': np.random.uniform(2, 24),
                'client_engagement_score': np.random.uniform(0.6, 0.95)
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating client metrics: {e}")
            return {}
    
    async def _analyze_client_behavior(self, user_id: int, period: str) -> Dict[str, Any]:
        """Analyze client behavior patterns"""
        try:
            behavior = {
                'preferred_contact_method': np.random.choice(['email', 'phone', 'whatsapp', 'in_person']),
                'average_decision_time_days': np.random.uniform(15, 60),
                'property_viewing_preference': np.random.choice(['virtual', 'in_person', 'both']),
                'price_sensitivity': np.random.uniform(0.3, 0.8),
                'location_preference': np.random.choice(['downtown', 'suburban', 'waterfront', 'mixed']),
                'property_type_preference': np.random.choice(['apartment', 'villa', 'townhouse', 'mixed'])
            }
            
            return behavior
            
        except Exception as e:
            logger.error(f"Error analyzing client behavior: {e}")
            return {}
    
    async def _get_key_performance_indicators(self, user_id: int) -> Dict[str, Any]:
        """Get key performance indicators"""
        try:
            kpis = {
                'revenue_growth': np.random.uniform(0.05, 0.35),
                'client_acquisition_cost': np.random.uniform(2000, 8000),
                'lifetime_client_value': np.random.uniform(50000, 300000),
                'deal_win_rate': np.random.uniform(0.2, 0.5),
                'average_deal_size': np.random.uniform(80000, 400000),
                'client_satisfaction_score': np.random.uniform(4.2, 5.0),
                'market_share_percentage': np.random.uniform(0.5, 3.0),
                'operational_efficiency': np.random.uniform(0.7, 0.95)
            }
            
            return kpis
            
        except Exception as e:
            logger.error(f"Error getting KPIs: {e}")
            return {}
    
    async def _get_business_metrics(self, user_id: int) -> Dict[str, Any]:
        """Get business metrics"""
        try:
            metrics = {
                'total_revenue': np.random.uniform(500000, 2000000),
                'operating_expenses': np.random.uniform(100000, 500000),
                'profit_margin': np.random.uniform(0.15, 0.35),
                'cash_flow': np.random.uniform(50000, 300000),
                'roi_percentage': np.random.uniform(0.2, 0.6),
                'market_position': np.random.choice(['leader', 'challenger', 'niche', 'emerging']),
                'competitive_advantage': np.random.choice(['technology', 'service', 'location', 'price', 'expertise'])
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting business metrics: {e}")
            return {}
    
    async def _get_team_performance(self, user_id: int) -> Dict[str, Any]:
        """Get team performance metrics"""
        try:
            team_metrics = {
                'team_size': np.random.randint(5, 25),
                'team_productivity': np.random.uniform(0.7, 0.95),
                'collaboration_score': np.random.uniform(0.6, 0.9),
                'skill_diversity': np.random.uniform(0.5, 0.9),
                'training_completion_rate': np.random.uniform(0.8, 1.0),
                'team_satisfaction': np.random.uniform(3.5, 5.0)
            }
            
            return team_metrics
            
        except Exception as e:
            logger.error(f"Error getting team performance: {e}")
            return {}
    
    async def _generate_performance_insights(
        self,
        current_metrics: Dict[str, Any],
        comparison_metrics: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Generate performance insights"""
        try:
            insights = []
            
            # Analyze current performance
            if current_metrics.get('leads_generated', 0) >= 80:
                insights.append("Excellent lead generation performance - exceeding targets")
            elif current_metrics.get('leads_generated', 0) < 40:
                insights.append("Lead generation needs improvement - consider new strategies")
            
            if current_metrics.get('conversion_rate', 0) >= 0.25:
                insights.append("Strong conversion rate - effective lead qualification")
            elif current_metrics.get('conversion_rate', 0) < 0.15:
                insights.append("Low conversion rate - review lead quality and follow-up process")
            
            if current_metrics.get('response_time_minutes', 0) <= 30:
                insights.append("Fast response time - excellent client service")
            elif current_metrics.get('response_time_minutes', 0) > 60:
                insights.append("Slow response time - consider automation and prioritization")
            
            # Add comparison insights if available
            if comparison_metrics:
                if comparison_metrics.get('revenue_change', 0) > 0.2:
                    insights.append("Strong revenue growth compared to previous period")
                elif comparison_metrics.get('revenue_change', 0) < -0.1:
                    insights.append("Revenue decline - investigate market conditions and strategies")
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating performance insights: {e}")
            return []
    
    async def _generate_performance_recommendations(
        self,
        current_metrics: Dict[str, Any],
        goal_progress: Dict[str, Any]
    ) -> List[str]:
        """Generate performance recommendations"""
        try:
            recommendations = []
            
            # Lead generation recommendations
            if current_metrics.get('leads_generated', 0) < 60:
                recommendations.append("Increase lead generation through digital marketing and networking")
            
            # Conversion rate recommendations
            if current_metrics.get('conversion_rate', 0) < 0.2:
                recommendations.append("Improve lead qualification and follow-up processes")
            
            # Response time recommendations
            if current_metrics.get('response_time_minutes', 0) > 45:
                recommendations.append("Implement automated responses and prioritize urgent inquiries")
            
            # Goal-specific recommendations
            if goal_progress.get('progress', {}).get('leads_progress', 0) < 70:
                recommendations.append("Focus on lead generation activities to meet monthly targets")
            
            if goal_progress.get('progress', {}).get('revenue_progress', 0) < 75:
                recommendations.append("Prioritize high-value deals and improve closing techniques")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating performance recommendations: {e}")
            return []
    
    async def _generate_market_insights(
        self,
        market_metrics: Dict[str, Any],
        market_trends: Dict[str, Any]
    ) -> List[str]:
        """Generate market insights"""
        try:
            insights = []
            
            # Price trend insights
            if market_metrics.get('price_change_percentage', 0) > 0.1:
                insights.append("Strong price appreciation - favorable selling conditions")
            elif market_metrics.get('price_change_percentage', 0) < -0.05:
                insights.append("Price correction - potential buying opportunities")
            
            # Market balance insights
            if market_metrics.get('market_balance', 0) > 1.2:
                insights.append("High demand relative to supply - competitive market")
            elif market_metrics.get('market_balance', 0) < 0.8:
                insights.append("Supply exceeds demand - buyer's market conditions")
            
            # Activity insights
            if market_metrics.get('market_activity', 0) > 0.8:
                insights.append("High market activity - good time for transactions")
            elif market_metrics.get('market_activity', 0) < 0.5:
                insights.append("Low market activity - consider timing strategies")
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating market insights: {e}")
            return []
    
    async def _generate_client_insights(
        self,
        client_metrics: Dict[str, Any],
        client_behavior: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Generate client insights"""
        try:
            insights = []
            
            # Client retention insights
            if client_metrics.get('client_retention_rate', 0) > 0.9:
                insights.append("Excellent client retention - strong relationships and service")
            elif client_metrics.get('client_retention_rate', 0) < 0.8:
                insights.append("Client retention needs improvement - review service quality")
            
            # Client satisfaction insights
            if client_metrics.get('client_satisfaction', 0) > 4.5:
                insights.append("High client satisfaction - maintain service standards")
            elif client_metrics.get('client_satisfaction', 0) < 4.0:
                insights.append("Client satisfaction below target - implement feedback system")
            
            # Response time insights
            if client_metrics.get('response_time_hours', 0) < 4:
                insights.append("Fast response times - excellent client service")
            elif client_metrics.get('response_time_hours', 0) > 12:
                insights.append("Slow response times - implement service level agreements")
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating client insights: {e}")
            return []
    
    async def _generate_strategic_insights(
        self,
        kpis: Dict[str, Any],
        business_metrics: Dict[str, Any]
    ) -> List[str]:
        """Generate strategic business insights"""
        try:
            insights = []
            
            # Revenue growth insights
            if kpis.get('revenue_growth', 0) > 0.2:
                insights.append("Strong revenue growth - consider expansion opportunities")
            elif kpis.get('revenue_growth', 0) < 0.05:
                insights.append("Slow revenue growth - review business strategy and market positioning")
            
            # Profitability insights
            if business_metrics.get('profit_margin', 0) > 0.25:
                insights.append("Healthy profit margins - good pricing and cost control")
            elif business_metrics.get('profit_margin', 0) < 0.15:
                insights.append("Low profit margins - review pricing strategy and cost structure")
            
            # Market position insights
            if business_metrics.get('market_position') == 'leader':
                insights.append("Market leadership position - leverage for premium pricing")
            elif business_metrics.get('market_position') == 'emerging':
                insights.append("Emerging market position - focus on differentiation and growth")
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating strategic insights: {e}")
            return []
    
    async def _calculate_market_score(self, market_metrics: Dict[str, Any]) -> float:
        """Calculate overall market score"""
        try:
            # Weighted scoring based on key metrics
            weights = {
                'demand_score': 0.3,
                'supply_score': 0.2,
                'market_activity': 0.25,
                'price_change_percentage': 0.15,
                'inventory_level': 0.1
            }
            
            score = 0
            for metric, weight in weights.items():
                value = market_metrics.get(metric, 0)
                if metric == 'inventory_level':
                    # Lower inventory is better (closer to 1.0)
                    normalized_value = max(0, 1 - abs(value - 1.0))
                elif metric == 'price_change_percentage':
                    # Moderate positive change is best
                    normalized_value = max(0, 1 - abs(value - 0.1))
                else:
                    normalized_value = value
                
                score += normalized_value * weight
            
            return min(100, score * 100)
            
        except Exception as e:
            logger.error(f"Error calculating market score: {e}")
            return 0.0
    
    async def _calculate_client_satisfaction(self, client_metrics: Dict[str, Any]) -> float:
        """Calculate client satisfaction score"""
        try:
            # Weighted scoring based on client metrics
            weights = {
                'client_satisfaction': 0.4,
                'client_engagement_score': 0.3,
                'client_retention_rate': 0.3
            }
            
            score = 0
            for metric, weight in weights.items():
                value = client_metrics.get(metric, 0)
                if metric == 'client_satisfaction':
                    # Convert 5.0 scale to percentage
                    normalized_value = value / 5.0
                else:
                    normalized_value = value
                
                score += normalized_value * weight
            
            return min(100, score * 100)
            
        except Exception as e:
            logger.error(f"Error calculating client satisfaction: {e}")
            return 0.0
    
    async def _calculate_business_health_score(
        self,
        kpis: Dict[str, Any],
        business_metrics: Dict[str, Any]
    ) -> float:
        """Calculate overall business health score"""
        try:
            # Weighted scoring based on business metrics
            weights = {
                'revenue_growth': 0.25,
                'profit_margin': 0.25,
                'roi_percentage': 0.2,
                'operational_efficiency': 0.2,
                'deal_win_rate': 0.1
            }
            
            score = 0
            for metric, weight in weights.items():
                value = kpis.get(metric, 0) if metric in kpis else business_metrics.get(metric, 0)
                
                # Normalize different metric types
                if metric in ['revenue_growth', 'roi_percentage']:
                    normalized_value = min(1.0, max(0, value))
                elif metric in ['profit_margin', 'deal_win_rate', 'operational_efficiency']:
                    normalized_value = min(1.0, max(0, value))
                else:
                    normalized_value = value
                
                score += normalized_value * weight
            
            return min(100, score * 100)
            
        except Exception as e:
            logger.error(f"Error calculating business health score: {e}")
            return 0.0

# Initialize service
performance_analytics_service = PerformanceAnalyticsService()
