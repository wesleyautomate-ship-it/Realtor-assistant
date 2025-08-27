"""
Performance Optimization and Caching for Dubai Real Estate RAG System
====================================================================

This module implements caching, response streaming, and performance optimizations
to ensure fast response times and cost-effective operation.
"""

import logging
import asyncio
import json
import hashlib
from typing import Dict, List, Any, Optional, AsyncGenerator
from datetime import datetime, timedelta
from dataclasses import dataclass
import time
from collections import OrderedDict
import redis
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime
    expires_at: datetime
    access_count: int = 0
    last_accessed: datetime = None

class PerformanceOptimizer:
    """Performance optimization and caching manager"""
    
    def __init__(self, db_url: str, redis_url: Optional[str] = None):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        
        # Initialize Redis if available
        self.redis_client = None
        if redis_url:
            try:
                self.redis_client = redis.from_url(redis_url)
                self.redis_client.ping()
                logger.info("✅ Redis cache connected")
            except Exception as e:
                logger.warning(f"⚠️ Redis not available: {e}")
        
        # In-memory cache as fallback
        self.memory_cache: OrderedDict = OrderedDict()
        self.max_cache_size = 1000
        self.cache_ttl = 3600  # 1 hour default
        
        # Performance metrics
        self.response_times: List[float] = []
        self.cache_hits = 0
        self.cache_misses = 0
        self.total_requests = 0
        
        # Cost tracking
        self.token_usage = {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_cost": 0.0
        }
    
    async def get_cached_response(self, query_hash: str, user_role: str) -> Optional[Dict]:
        """Get cached response for query"""
        try:
            cache_key = f"response:{user_role}:{query_hash}"
            
            # Try Redis first
            if self.redis_client:
                cached = self.redis_client.get(cache_key)
                if cached:
                    self.cache_hits += 1
                    return json.loads(cached)
            
            # Try memory cache
            if cache_key in self.memory_cache:
                entry = self.memory_cache[cache_key]
                if datetime.now() < entry.expires_at:
                    entry.access_count += 1
                    entry.last_accessed = datetime.now()
                    self.cache_hits += 1
                    return entry.value
            
            self.cache_misses += 1
            return None
            
        except Exception as e:
            logger.error(f"Error getting cached response: {e}")
            return None
    
    async def cache_response(self, query_hash: str, user_role: str, response: Dict, ttl: int = None) -> bool:
        """Cache response for future use"""
        try:
            cache_key = f"response:{user_role}:{query_hash}"
            ttl = ttl or self.cache_ttl
            expires_at = datetime.now() + timedelta(seconds=ttl)
            
            # Cache in Redis
            if self.redis_client:
                self.redis_client.setex(
                    cache_key,
                    ttl,
                    json.dumps(response)
                )
            
            # Cache in memory
            entry = CacheEntry(
                key=cache_key,
                value=response,
                created_at=datetime.now(),
                expires_at=expires_at,
                access_count=1,
                last_accessed=datetime.now()
            )
            
            self.memory_cache[cache_key] = entry
            
            # Maintain cache size
            if len(self.memory_cache) > self.max_cache_size:
                # Remove least recently used
                oldest_key = next(iter(self.memory_cache))
                del self.memory_cache[oldest_key]
            
            return True
            
        except Exception as e:
            logger.error(f"Error caching response: {e}")
            return False
    
    def generate_query_hash(self, query: str, context: Dict) -> str:
        """Generate hash for query caching"""
        query_data = {
            "query": query.lower().strip(),
            "user_role": context.get("user_role", "client"),
            "data_types": sorted(context.get("allowed_data_types", [])),
            "session_id": context.get("session_id", "")
        }
        
        query_string = json.dumps(query_data, sort_keys=True)
        return hashlib.md5(query_string.encode()).hexdigest()
    
    async def stream_response(self, response_generator: AsyncGenerator[str, None]) -> AsyncGenerator[str, None]:
        """Stream response tokens for better UX"""
        try:
            async for token in response_generator:
                yield token
                await asyncio.sleep(0.01)  # Small delay for smooth streaming
                
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            yield "Error: Unable to stream response"
    
    def track_performance(self, start_time: float, end_time: float, 
                         input_tokens: int = 0, output_tokens: int = 0) -> Dict[str, Any]:
        """Track performance metrics"""
        try:
            response_time = end_time - start_time
            self.response_times.append(response_time)
            self.total_requests += 1
            
            # Update token usage
            self.token_usage["input_tokens"] += input_tokens
            self.token_usage["output_tokens"] += output_tokens
            
            # Calculate cost (approximate)
            input_cost = (input_tokens / 1000) * 0.03  # GPT-4 input cost
            output_cost = (output_tokens / 1000) * 0.06  # GPT-4 output cost
            total_cost = input_cost + output_cost
            
            self.token_usage["total_cost"] += total_cost
            
            # Calculate metrics
            avg_response_time = sum(self.response_times[-100:]) / min(len(self.response_times), 100)
            cache_hit_rate = self.cache_hits / max(self.total_requests, 1)
            
            metrics = {
                "response_time": response_time,
                "avg_response_time": avg_response_time,
                "cache_hit_rate": cache_hit_rate,
                "total_requests": self.total_requests,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": total_cost,
                "total_cost": self.token_usage["total_cost"]
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error tracking performance: {e}")
            return {}
    
    async def optimize_prompt(self, prompt: str, user_role: str, context: Dict) -> str:
        """Optimize prompt for better performance and cost"""
        try:
            # Role-specific optimizations
            if user_role == "client":
                # Keep prompts concise for clients
                if len(prompt) > 2000:
                    prompt = prompt[:2000] + "..."
            
            elif user_role == "agent":
                # Include more context for agents
                if "market_analysis" in context.get("allowed_data_types", []):
                    prompt += "\n\nInclude market analysis and comparative data."
            
            elif user_role == "admin":
                # Full context for admins
                prompt += "\n\nInclude all available data and internal insights."
            
            # Add performance hints
            prompt += "\n\nProvide a concise, structured response."
            
            return prompt
            
        except Exception as e:
            logger.error(f"Error optimizing prompt: {e}")
            return prompt
    
    async def get_common_queries_cache(self) -> Dict[str, Any]:
        """Get cache for common queries"""
        try:
            cache_key = "common_queries"
            
            if self.redis_client:
                cached = self.redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            
            # Common queries that can be cached
            common_queries = {
                "market_overview": {
                    "query": "Dubai real estate market overview",
                    "response": "Dubai's real estate market shows strong growth with 15-20% appreciation in 2024...",
                    "ttl": 3600  # 1 hour
                },
                "popular_areas": {
                    "query": "Most popular areas in Dubai",
                    "response": "Top areas include Dubai Marina, Downtown Dubai, Palm Jumeirah...",
                    "ttl": 7200  # 2 hours
                },
                "investment_benefits": {
                    "query": "Dubai investment benefits",
                    "response": "Key benefits include Golden Visa eligibility, 0% income tax...",
                    "ttl": 3600
                }
            }
            
            # Cache in Redis
            if self.redis_client:
                self.redis_client.setex(
                    cache_key,
                    3600,
                    json.dumps(common_queries)
                )
            
            return common_queries
            
        except Exception as e:
            logger.error(f"Error getting common queries cache: {e}")
            return {}
    
    async def clear_expired_cache(self) -> int:
        """Clear expired cache entries"""
        try:
            cleared_count = 0
            current_time = datetime.now()
            
            # Clear memory cache
            expired_keys = []
            for key, entry in self.memory_cache.items():
                if current_time > entry.expires_at:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.memory_cache[key]
                cleared_count += 1
            
            # Redis handles expiration automatically
            
            if cleared_count > 0:
                logger.info(f"Cleared {cleared_count} expired cache entries")
            
            return cleared_count
            
        except Exception as e:
            logger.error(f"Error clearing expired cache: {e}")
            return 0
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        try:
            avg_response_time = sum(self.response_times[-100:]) / min(len(self.response_times), 100) if self.response_times else 0
            cache_hit_rate = self.cache_hits / max(self.total_requests, 1)
            
            return {
                "performance": {
                    "avg_response_time": avg_response_time,
                    "total_requests": self.total_requests,
                    "cache_hit_rate": cache_hit_rate,
                    "cache_hits": self.cache_hits,
                    "cache_misses": self.cache_misses
                },
                "costs": {
                    "total_cost": self.token_usage["total_cost"],
                    "input_tokens": self.token_usage["input_tokens"],
                    "output_tokens": self.token_usage["output_tokens"],
                    "avg_cost_per_request": self.token_usage["total_cost"] / max(self.total_requests, 1)
                },
                "cache": {
                    "memory_cache_size": len(self.memory_cache),
                    "redis_available": self.redis_client is not None
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {}

# Global performance optimizer instance
performance_optimizer = None

def initialize_performance_optimizer(db_url: str, redis_url: Optional[str] = None):
    """Initialize the global performance optimizer"""
    global performance_optimizer
    performance_optimizer = PerformanceOptimizer(db_url, redis_url)
    logger.info("✅ Performance Optimizer initialized successfully")

def get_performance_optimizer() -> PerformanceOptimizer:
    """Get the global performance optimizer instance"""
    if performance_optimizer is None:
        raise RuntimeError("Performance Optimizer not initialized. Call initialize_performance_optimizer() first.")
    return performance_optimizer
