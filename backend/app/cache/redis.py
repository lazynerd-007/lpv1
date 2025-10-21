"""
Redis cache configuration and connection management
"""
from typing import Optional, Any, Union
import json
import pickle
from datetime import timedelta
import redis.asyncio as redis
from redis.asyncio import ConnectionPool
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

# Global Redis connection pool
redis_pool: Optional[ConnectionPool] = None
redis_client: Optional[redis.Redis] = None


async def init_redis() -> None:
    """Initialize Redis connection pool and client"""
    global redis_pool, redis_client
    
    try:
        # Create connection pool
        redis_pool = ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=settings.REDIS_POOL_SIZE,
            retry_on_timeout=True,
            socket_keepalive=True,
            socket_keepalive_options={},
            health_check_interval=30,
        )
        
        # Create Redis client
        redis_client = redis.Redis(connection_pool=redis_pool)
        
        # Test connection
        await redis_client.ping()
        
        logger.info("Redis connection initialized successfully")
        
    except Exception as e:
        logger.error("Failed to initialize Redis", error=str(e))
        raise


async def close_redis() -> None:
    """Close Redis connections"""
    global redis_pool, redis_client
    
    if redis_client:
        await redis_client.close()
    
    if redis_pool:
        await redis_pool.disconnect()
    
    logger.info("Redis connections closed")


async def get_redis() -> redis.Redis:
    """
    Get Redis client instance
    
    Returns:
        redis.Redis: Redis client
    """
    if not redis_client:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    
    return redis_client


class CacheService:
    """Redis cache service with TTL and invalidation strategies"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.logger = structlog.get_logger(__name__)
    
    async def get(self, key: str, default: Any = None) -> Any:
        """
        Get value from cache
        
        Args:
            key: Cache key
            default: Default value if key not found
            
        Returns:
            Cached value or default
        """
        try:
            value = await self.redis.get(key)
            if value is None:
                return default
            
            # Try to deserialize as JSON first, then pickle
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return pickle.loads(value)
                
        except Exception as e:
            self.logger.error("Cache get error", key=key, error=str(e))
            return default
    
    async def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[Union[int, timedelta]] = None
    ) -> bool:
        """
        Set value in cache with optional TTL
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live (seconds or timedelta)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Serialize value
            if isinstance(value, (dict, list, str, int, float, bool)):
                serialized_value = json.dumps(value)
            else:
                serialized_value = pickle.dumps(value)
            
            # Set with TTL
            if ttl:
                if isinstance(ttl, timedelta):
                    ttl = int(ttl.total_seconds())
                await self.redis.setex(key, ttl, serialized_value)
            else:
                await self.redis.set(key, serialized_value)
            
            return True
            
        except Exception as e:
            self.logger.error("Cache set error", key=key, error=str(e))
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Delete key from cache
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if key was deleted, False otherwise
        """
        try:
            result = await self.redis.delete(key)
            return result > 0
        except Exception as e:
            self.logger.error("Cache delete error", key=key, error=str(e))
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching pattern
        
        Args:
            pattern: Pattern to match (e.g., "user:*")
            
        Returns:
            Number of keys deleted
        """
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                return await self.redis.delete(*keys)
            return 0
        except Exception as e:
            self.logger.error("Cache delete pattern error", pattern=pattern, error=str(e))
            return 0
    
    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists, False otherwise
        """
        try:
            return await self.redis.exists(key) > 0
        except Exception as e:
            self.logger.error("Cache exists error", key=key, error=str(e))
            return False
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """
        Increment numeric value in cache
        
        Args:
            key: Cache key
            amount: Amount to increment by
            
        Returns:
            New value after increment
        """
        try:
            return await self.redis.incrby(key, amount)
        except Exception as e:
            self.logger.error("Cache increment error", key=key, error=str(e))
            return 0
    
    async def expire(self, key: str, ttl: Union[int, timedelta]) -> bool:
        """
        Set expiration time for existing key
        
        Args:
            key: Cache key
            ttl: Time to live (seconds or timedelta)
            
        Returns:
            True if expiration was set, False otherwise
        """
        try:
            if isinstance(ttl, timedelta):
                ttl = int(ttl.total_seconds())
            return await self.redis.expire(key, ttl)
        except Exception as e:
            self.logger.error("Cache expire error", key=key, error=str(e))
            return False


def cache_key(*args: str) -> str:
    """
    Generate cache key from arguments
    
    Args:
        *args: Key components
        
    Returns:
        Formatted cache key
    """
    return ":".join(str(arg) for arg in args)


# Cache decorators
def cache_result(ttl: Union[int, timedelta] = 300, key_prefix: str = ""):
    """
    Decorator to cache function results
    
    Args:
        ttl: Time to live for cached result
        key_prefix: Prefix for cache key
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [key_prefix or func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
            cache_key_str = cache_key(*key_parts)
            
            # Try to get from cache
            cache_service = CacheService(await get_redis())
            cached_result = await cache_service.get(cache_key_str)
            
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_service.set(cache_key_str, result, ttl)
            
            return result
        
        return wrapper
    return decorator


async def get_cache_service() -> CacheService:
    """
    Dependency to get cache service
    
    Returns:
        CacheService: Cache service instance
    """
    redis_client = await get_redis()
    return CacheService(redis_client)