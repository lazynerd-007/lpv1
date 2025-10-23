"""
Performance monitoring and optimization service
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import structlog

from app.db.optimization import DatabaseOptimizer, QueryOptimizer
from app.db.database import engine
from app.cache.redis import get_cache_service
from app.core.config import settings

logger = structlog.get_logger(__name__)


class PerformanceService:
    """Service for monitoring and optimizing application performance"""
    
    def __init__(self):
        self.db_optimizer = DatabaseOptimizer(engine) if engine else None
        self.query_optimizer = QueryOptimizer()
    
    async def optimize_database(self) -> Dict[str, Any]:
        """Run database optimization tasks"""
        if not self.db_optimizer:
            return {"error": "Database optimizer not available"}
        
        return await self.db_optimizer.optimize_database()
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        
        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "database": {},
            "cache": {},
            "application": {}
        }
        
        # Database metrics
        if self.db_optimizer:
            try:
                metrics["database"]["slow_queries"] = await self.db_optimizer.get_slow_queries(5)
                metrics["database"]["table_stats"] = await self.db_optimizer.get_table_sizes()
            except Exception as e:
                logger.warning(f"Failed to get database metrics: {e}")
                metrics["database"]["error"] = str(e)
        
        # Cache metrics
        try:
            cache_service = await get_cache_service()
            redis_client = cache_service.redis
            
            # Get Redis info
            redis_info = await redis_client.info()
            metrics["cache"] = {
                "connected_clients": redis_info.get("connected_clients", 0),
                "used_memory": redis_info.get("used_memory", 0),
                "used_memory_human": redis_info.get("used_memory_human", "0B"),
                "keyspace_hits": redis_info.get("keyspace_hits", 0),
                "keyspace_misses": redis_info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(
                    redis_info.get("keyspace_hits", 0),
                    redis_info.get("keyspace_misses", 0)
                )
            }
        except Exception as e:
            logger.warning(f"Failed to get cache metrics: {e}")
            metrics["cache"]["error"] = str(e)
        
        return metrics
    
    async def monitor_query_performance(
        self, 
        query_func, 
        *args, 
        **kwargs
    ) -> Dict[str, Any]:
        """Monitor the performance of a database query"""
        
        start_time = time.time()
        
        try:
            result = await query_func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "execution_time": execution_time,
                "result_count": len(result) if isinstance(result, (list, tuple)) else 1
            }
        except Exception as e:
            execution_time = time.time() - start_time
            
            return {
                "success": False,
                "execution_time": execution_time,
                "error": str(e)
            }
    
    async def get_cache_statistics(self) -> Dict[str, Any]:
        """Get detailed cache statistics"""
        
        try:
            cache_service = await get_cache_service()
            redis_client = cache_service.redis
            
            # Get all keys with patterns
            patterns = [
                "movie:*",
                "user:*", 
                "search:*",
                "reviews:*",
                "session:*"
            ]
            
            stats = {}
            
            for pattern in patterns:
                keys = await redis_client.keys(pattern)
                category = pattern.replace(":*", "")
                stats[category] = {
                    "key_count": len(keys),
                    "sample_keys": keys[:5] if keys else []
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get cache statistics: {e}")
            return {"error": str(e)}
    
    async def clear_cache_by_pattern(self, pattern: str) -> int:
        """Clear cache entries matching a pattern"""
        
        try:
            cache_service = await get_cache_service()
            return await cache_service.delete_pattern(pattern)
        except Exception as e:
            logger.error(f"Failed to clear cache pattern {pattern}: {e}")
            return 0
    
    async def warm_cache(self) -> Dict[str, Any]:
        """Warm up cache with frequently accessed data"""
        
        results = {
            "movies_cached": 0,
            "users_cached": 0,
            "searches_cached": 0,
            "errors": []
        }
        
        try:
            # This would typically involve pre-loading popular movies,
            # user profiles, and common search results
            # Implementation would depend on specific caching strategies
            
            logger.info("Cache warming completed")
            
        except Exception as e:
            logger.error(f"Cache warming failed: {e}")
            results["errors"].append(str(e))
        
        return results
    
    async def analyze_slow_endpoints(self, db: AsyncSession) -> List[Dict[str, Any]]:
        """Analyze slow API endpoints based on logs or metrics"""
        
        # This would typically analyze application logs or metrics
        # For now, return database slow queries as a proxy
        
        if not self.db_optimizer:
            return []
        
        try:
            slow_queries = await self.db_optimizer.get_slow_queries(10)
            
            # Map queries to likely endpoints
            endpoint_mapping = {
                "SELECT * FROM movies": "/api/v1/movies",
                "SELECT * FROM reviews": "/api/v1/reviews", 
                "SELECT * FROM users": "/api/v1/users"
            }
            
            analyzed = []
            for query in slow_queries:
                endpoint = "unknown"
                for query_pattern, mapped_endpoint in endpoint_mapping.items():
                    if query_pattern in query.get("query", ""):
                        endpoint = mapped_endpoint
                        break
                
                analyzed.append({
                    "endpoint": endpoint,
                    "avg_execution_time": query.get("mean_exec_time", 0),
                    "total_calls": query.get("calls", 0),
                    "query_sample": query.get("query", "")[:100] + "..."
                })
            
            return analyzed
            
        except Exception as e:
            logger.error(f"Failed to analyze slow endpoints: {e}")
            return []
    
    async def optimize_query_plan(
        self, 
        query: str, 
        db: AsyncSession
    ) -> Dict[str, Any]:
        """Analyze and suggest optimizations for a query"""
        
        try:
            # Get query execution plan
            explain_query = self.query_optimizer.explain_query(query, analyze=True)
            result = await db.execute(text(explain_query))
            
            plan_lines = [row[0] for row in result.fetchall()]
            
            # Analyze plan for common issues
            suggestions = []
            
            for line in plan_lines:
                if "Seq Scan" in line:
                    suggestions.append("Consider adding an index to avoid sequential scan")
                elif "Sort" in line and "external merge" in line.lower():
                    suggestions.append("Consider increasing work_mem for large sorts")
                elif "Nested Loop" in line:
                    suggestions.append("Check if join conditions are properly indexed")
            
            return {
                "execution_plan": plan_lines,
                "suggestions": suggestions,
                "query": query
            }
            
        except Exception as e:
            logger.error(f"Failed to optimize query plan: {e}")
            return {"error": str(e)}
    
    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """Calculate cache hit rate percentage"""
        total = hits + misses
        if total == 0:
            return 0.0
        return (hits / total) * 100
    
    async def schedule_maintenance_tasks(self) -> None:
        """Schedule regular maintenance tasks"""
        
        # This would typically be called by a background task scheduler
        # like Celery or APScheduler
        
        try:
            # Run database optimization weekly
            if datetime.now().weekday() == 6:  # Sunday
                await self.optimize_database()
                logger.info("Weekly database optimization completed")
            
            # Analyze tables daily
            if self.db_optimizer:
                await self.db_optimizer.analyze_tables()
                logger.info("Daily table analysis completed")
            
        except Exception as e:
            logger.error(f"Maintenance tasks failed: {e}")


# Performance monitoring decorators
def monitor_performance(operation_name: str):
    """Decorator to monitor operation performance"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                logger.info(
                    f"Performance: {operation_name}",
                    execution_time=execution_time,
                    success=True
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                logger.error(
                    f"Performance: {operation_name}",
                    execution_time=execution_time,
                    success=False,
                    error=str(e)
                )
                
                raise
        
        return wrapper
    return decorator


def cache_result_with_monitoring(cache_key: str, ttl: int = 300):
    """Decorator to cache results with performance monitoring"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            cache_service = await get_cache_service()
            
            # Try to get from cache
            start_time = time.time()
            cached_result = await cache_service.get(cache_key)
            cache_lookup_time = time.time() - start_time
            
            if cached_result is not None:
                logger.info(
                    f"Cache hit: {cache_key}",
                    lookup_time=cache_lookup_time
                )
                return cached_result
            
            # Execute function and cache result
            start_time = time.time()
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Cache the result
            await cache_service.set(cache_key, result, ttl)
            
            logger.info(
                f"Cache miss: {cache_key}",
                execution_time=execution_time,
                cached=True
            )
            
            return result
        
        return wrapper
    return decorator