"""
Redis cache configuration and connection management
"""
from typing import Optional, Any, Union, Dict, List
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
        logger.warning("Failed to initialize Redis - falling back to mock Redis", error=str(e))
        # Don't raise the exception, just log the warning and continue without Redis
        redis_pool = None
        redis_client = None
        
        # Initialize mock Redis as fallback
        try:
            from app.cache.mock_redis import init_mock_redis
            await init_mock_redis()
            logger.info("Mock Redis initialized successfully as fallback")
        except Exception as mock_error:
            logger.error("Failed to initialize mock Redis fallback", error=str(mock_error))
            # Continue without any Redis - the application should handle this gracefully


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
        redis.Redis: Redis client or mock Redis client
    """
    # If Redis client is available, use it
    if redis_client:
        return redis_client
    
    # Check if mock Redis is available (for testing or when Redis is not available)
    try:
        from app.cache.mock_redis import get_mock_redis_client
        mock_client = get_mock_redis_client()
        if mock_client:
            logger.info("Using mock Redis client")
            return mock_client
    except ImportError:
        pass
    
    # If neither real nor mock Redis is available, raise an error
    raise RuntimeError("Redis not initialized and mock Redis not available. Call init_redis() first.")


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


def get_redis_client() -> redis.Redis:
    """
    Get Redis client instance (synchronous version for rate limiter)
    
    Returns:
        redis.Redis: Redis client
    """
    if not redis_client:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    
    return redis_client


async def get_cache_service() -> CacheService:
    """
    Dependency to get cache service
    
    Returns:
        CacheService: Cache service instance
    """
    redis_client = await get_redis()
    return CacheService(redis_client)


class MovieCacheService:
    """Specialized cache service for movie-related data"""
    
    def __init__(self, cache_service: CacheService):
        self.cache = cache_service
        self.logger = structlog.get_logger(__name__)
    
    async def get_movie(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """Get cached movie data"""
        key = cache_key("movie", movie_id)
        return await self.cache.get(key)
    
    async def set_movie(self, movie_id: str, movie_data: Dict[str, Any], ttl: int = 3600) -> bool:
        """Cache movie data for 1 hour by default"""
        key = cache_key("movie", movie_id)
        return await self.cache.set(key, movie_data, ttl)
    
    async def get_movie_stats(self, movie_id: str) -> Optional[Dict[str, Any]]:
        """Get cached movie statistics"""
        key = cache_key("movie", movie_id, "stats")
        return await self.cache.get(key)
    
    async def set_movie_stats(self, movie_id: str, stats_data: Dict[str, Any], ttl: int = 300) -> bool:
        """Cache movie statistics for 5 minutes"""
        key = cache_key("movie", movie_id, "stats")
        return await self.cache.set(key, stats_data, ttl)
    
    async def get_trending_movies(self) -> Optional[List[Dict[str, Any]]]:
        """Get cached trending movies"""
        key = cache_key("movies", "trending")
        return await self.cache.get(key)
    
    async def set_trending_movies(self, movies_data: List[Dict[str, Any]], ttl: int = 900) -> bool:
        """Cache trending movies for 15 minutes"""
        key = cache_key("movies", "trending")
        return await self.cache.set(key, movies_data, ttl)
    
    async def get_featured_movies(self) -> Optional[List[Dict[str, Any]]]:
        """Get cached featured movies"""
        key = cache_key("movies", "featured")
        return await self.cache.get(key)
    
    async def set_featured_movies(self, movies_data: List[Dict[str, Any]], ttl: int = 1800) -> bool:
        """Cache featured movies for 30 minutes"""
        key = cache_key("movies", "featured")
        return await self.cache.set(key, movies_data, ttl)
    
    async def get_movie_reviews(self, movie_id: str, page: int, limit: int) -> Optional[Dict[str, Any]]:
        """Get cached movie reviews"""
        key = cache_key("movie", movie_id, "reviews", f"p{page}", f"l{limit}")
        return await self.cache.get(key)
    
    async def set_movie_reviews(self, movie_id: str, page: int, limit: int, reviews_data: Dict[str, Any], ttl: int = 600) -> bool:
        """Cache movie reviews for 10 minutes"""
        key = cache_key("movie", movie_id, "reviews", f"p{page}", f"l{limit}")
        return await self.cache.set(key, reviews_data, ttl)
    
    async def invalidate_movie(self, movie_id: str) -> int:
        """Invalidate all cached data for a movie"""
        pattern = cache_key("movie", movie_id, "*")
        return await self.cache.delete_pattern(pattern)
    
    async def invalidate_movie_lists(self) -> int:
        """Invalidate cached movie lists (trending, featured, etc.)"""
        patterns = [
            cache_key("movies", "trending"),
            cache_key("movies", "featured"),
            cache_key("movies", "search", "*")
        ]
        total_deleted = 0
        for pattern in patterns:
            total_deleted += await self.cache.delete_pattern(pattern)
        return total_deleted


class UserCacheService:
    """Specialized cache service for user-related data"""
    
    def __init__(self, cache_service: CacheService):
        self.cache = cache_service
        self.logger = structlog.get_logger(__name__)
    
    async def get_user_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get cached user session data"""
        key = cache_key("session", user_id)
        return await self.cache.get(key)
    
    async def set_user_session(self, user_id: str, session_data: Dict[str, Any], ttl: int = 3600) -> bool:
        """Cache user session for 1 hour"""
        key = cache_key("session", user_id)
        return await self.cache.set(key, session_data, ttl)
    
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get cached user profile"""
        key = cache_key("user", user_id, "profile")
        return await self.cache.get(key)
    
    async def set_user_profile(self, user_id: str, profile_data: Dict[str, Any], ttl: int = 1800) -> bool:
        """Cache user profile for 30 minutes"""
        key = cache_key("user", user_id, "profile")
        return await self.cache.set(key, profile_data, ttl)
    
    async def get_user_stats(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get cached user statistics"""
        key = cache_key("user", user_id, "stats")
        return await self.cache.get(key)
    
    async def set_user_stats(self, user_id: str, stats_data: Dict[str, Any], ttl: int = 600) -> bool:
        """Cache user statistics for 10 minutes"""
        key = cache_key("user", user_id, "stats")
        return await self.cache.set(key, stats_data, ttl)
    
    async def get_user_watchlist(self, user_id: str, page: int, limit: int) -> Optional[Dict[str, Any]]:
        """Get cached user watchlist"""
        key = cache_key("user", user_id, "watchlist", f"p{page}", f"l{limit}")
        return await self.cache.get(key)
    
    async def set_user_watchlist(self, user_id: str, page: int, limit: int, watchlist_data: Dict[str, Any], ttl: int = 600) -> bool:
        """Cache user watchlist for 10 minutes"""
        key = cache_key("user", user_id, "watchlist", f"p{page}", f"l{limit}")
        return await self.cache.set(key, watchlist_data, ttl)
    
    async def get_user_favorites(self, user_id: str, page: int, limit: int) -> Optional[Dict[str, Any]]:
        """Get cached user favorites"""
        key = cache_key("user", user_id, "favorites", f"p{page}", f"l{limit}")
        return await self.cache.get(key)
    
    async def set_user_favorites(self, user_id: str, page: int, limit: int, favorites_data: Dict[str, Any], ttl: int = 600) -> bool:
        """Cache user favorites for 10 minutes"""
        key = cache_key("user", user_id, "favorites", f"p{page}", f"l{limit}")
        return await self.cache.set(key, favorites_data, ttl)
    
    async def get_activity_feed(self, user_id: str, page: int, limit: int) -> Optional[Dict[str, Any]]:
        """Get cached user activity feed"""
        key = cache_key("user", user_id, "feed", f"p{page}", f"l{limit}")
        return await self.cache.get(key)
    
    async def set_activity_feed(self, user_id: str, page: int, limit: int, feed_data: Dict[str, Any], ttl: int = 300) -> bool:
        """Cache activity feed for 5 minutes"""
        key = cache_key("user", user_id, "feed", f"p{page}", f"l{limit}")
        return await self.cache.set(key, feed_data, ttl)
    
    async def invalidate_user(self, user_id: str) -> int:
        """Invalidate all cached data for a user"""
        pattern = cache_key("user", user_id, "*")
        return await self.cache.delete_pattern(pattern)
    
    async def invalidate_user_session(self, user_id: str) -> bool:
        """Invalidate user session"""
        key = cache_key("session", user_id)
        return await self.cache.delete(key)
    
    async def invalidate_user_lists(self, user_id: str) -> int:
        """Invalidate user's cached lists (watchlist, favorites, feed)"""
        patterns = [
            cache_key("user", user_id, "watchlist", "*"),
            cache_key("user", user_id, "favorites", "*"),
            cache_key("user", user_id, "feed", "*")
        ]
        total_deleted = 0
        for pattern in patterns:
            total_deleted += await self.cache.delete_pattern(pattern)
        return total_deleted


class SearchCacheService:
    """Specialized cache service for search-related data"""
    
    def __init__(self, cache_service: CacheService):
        self.cache = cache_service
        self.logger = structlog.get_logger(__name__)
    
    async def get_search_results(self, query_hash: str) -> Optional[List[Dict[str, Any]]]:
        """Get cached search results"""
        key = cache_key("search", "movies", query_hash)
        return await self.cache.get(key)
    
    async def set_search_results(self, query_hash: str, results: List[Dict[str, Any]], ttl: int = 1800) -> bool:
        """Cache search results for 30 minutes"""
        key = cache_key("search", "movies", query_hash)
        return await self.cache.set(key, results, ttl)
    
    async def get_search_suggestions(self, partial_query: str) -> Optional[List[str]]:
        """Get cached search suggestions"""
        key = cache_key("search", "suggestions", partial_query.lower())
        return await self.cache.get(key)
    
    async def set_search_suggestions(self, partial_query: str, suggestions: List[str], ttl: int = 3600) -> bool:
        """Cache search suggestions for 1 hour"""
        key = cache_key("search", "suggestions", partial_query.lower())
        return await self.cache.set(key, suggestions, ttl)
    
    async def get_popular_searches(self) -> Optional[List[str]]:
        """Get cached popular searches"""
        key = cache_key("search", "popular")
        return await self.cache.get(key)
    
    async def set_popular_searches(self, searches: List[str], ttl: int = 3600) -> bool:
        """Cache popular searches for 1 hour"""
        key = cache_key("search", "popular")
        return await self.cache.set(key, searches, ttl)
    
    async def invalidate_search_cache(self) -> int:
        """Invalidate all search cache"""
        pattern = cache_key("search", "*")
        return await self.cache.delete_pattern(pattern)


class ReviewCacheService:
    """Specialized cache service for review-related data"""
    
    def __init__(self, cache_service: CacheService):
        self.cache = cache_service
        self.logger = structlog.get_logger(__name__)
    
    async def get_trending_reviews(self) -> Optional[List[Dict[str, Any]]]:
        """Get cached trending reviews"""
        key = cache_key("reviews", "trending")
        return await self.cache.get(key)
    
    async def set_trending_reviews(self, reviews: List[Dict[str, Any]], ttl: int = 600) -> bool:
        """Cache trending reviews for 10 minutes"""
        key = cache_key("reviews", "trending")
        return await self.cache.set(key, reviews, ttl)
    
    async def get_user_reviews(self, user_id: str, page: int, limit: int) -> Optional[Dict[str, Any]]:
        """Get cached user reviews"""
        key = cache_key("user", user_id, "reviews", f"p{page}", f"l{limit}")
        return await self.cache.get(key)
    
    async def set_user_reviews(self, user_id: str, page: int, limit: int, reviews_data: Dict[str, Any], ttl: int = 600) -> bool:
        """Cache user reviews for 10 minutes"""
        key = cache_key("user", user_id, "reviews", f"p{page}", f"l{limit}")
        return await self.cache.set(key, reviews_data, ttl)
    
    async def invalidate_review_caches(self, user_id: str = None, movie_id: str = None) -> int:
        """Invalidate review-related caches"""
        patterns = [cache_key("reviews", "trending")]
        
        if user_id:
            patterns.append(cache_key("user", user_id, "reviews", "*"))
        
        if movie_id:
            patterns.append(cache_key("movie", movie_id, "reviews", "*"))
            patterns.append(cache_key("movie", movie_id, "stats"))
        
        total_deleted = 0
        for pattern in patterns:
            total_deleted += await self.cache.delete_pattern(pattern)
        return total_deleted


# Cache service factory functions
async def get_movie_cache_service() -> MovieCacheService:
    """Get movie cache service instance"""
    cache_service = await get_cache_service()
    return MovieCacheService(cache_service)


async def get_user_cache_service() -> UserCacheService:
    """Get user cache service instance"""
    cache_service = await get_cache_service()
    return UserCacheService(cache_service)


async def get_search_cache_service() -> SearchCacheService:
    """Get search cache service instance"""
    cache_service = await get_cache_service()
    return SearchCacheService(cache_service)


async def get_review_cache_service() -> ReviewCacheService:
    """Get review cache service instance"""
    cache_service = await get_cache_service()
    return ReviewCacheService(cache_service)