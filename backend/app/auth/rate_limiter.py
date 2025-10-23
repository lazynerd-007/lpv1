"""
Rate limiting service for API endpoints
"""
from typing import Optional, Dict, Any
import time
import json
from datetime import datetime, timedelta

from fastapi import Request, HTTPException, status
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from redis import Redis

from app.core.config import settings
from app.cache.redis import get_redis_client


class RateLimiter:
    """Custom rate limiter with Redis backend"""
    
    def __init__(self, redis_client: Optional[Redis] = None):
        self._redis_client = redis_client
        self._redis = None
        self.default_rate = f"{settings.RATE_LIMIT_PER_MINUTE}/minute"
    
    @property
    def redis(self):
        """Lazy initialization of Redis client"""
        if self._redis is None:
            if self._redis_client:
                self._redis = self._redis_client
            else:
                try:
                    self._redis = get_redis_client()
                except RuntimeError:
                    # Redis not initialized, return None for testing
                    return None
        return self._redis
    
    async def is_allowed(
        self, 
        key: str, 
        limit: int, 
        window_seconds: int
    ) -> tuple[bool, Dict[str, Any]]:
        """
        Check if request is allowed based on rate limit
        
        Returns:
            (is_allowed, info_dict)
        """
        # If Redis is not available, allow all requests (for testing)
        if self.redis is None:
            info = {
                "limit": limit,
                "remaining": limit - 1,
                "reset_time": int(time.time()) + window_seconds,
                "retry_after": None
            }
            return True, info
        
        current_time = int(time.time())
        window_start = current_time - window_seconds
        
        # Use Redis sorted set to track requests in time window
        pipe = self.redis.pipeline()
        
        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)
        
        # Count current requests in window
        pipe.zcard(key)
        
        # Add current request
        pipe.zadd(key, {str(current_time): current_time})
        
        # Set expiration
        pipe.expire(key, window_seconds)
        
        results = pipe.execute()
        current_requests = results[1]
        
        is_allowed = current_requests < limit
        
        info = {
            "limit": limit,
            "remaining": max(0, limit - current_requests - 1),
            "reset_time": current_time + window_seconds,
            "retry_after": window_seconds if not is_allowed else None
        }
        
        return is_allowed, info
    
    async def check_rate_limit(
        self, 
        request: Request, 
        limit: int = None, 
        window_seconds: int = 60,
        key_func: callable = None
    ) -> Dict[str, Any]:
        """
        Check rate limit for a request
        
        Args:
            request: FastAPI request object
            limit: Number of requests allowed in window
            window_seconds: Time window in seconds
            key_func: Function to generate rate limit key
        
        Returns:
            Rate limit info dictionary
        
        Raises:
            HTTPException: If rate limit exceeded
        """
        if limit is None:
            limit = settings.RATE_LIMIT_PER_MINUTE
        
        # Generate rate limit key
        if key_func:
            key = key_func(request)
        else:
            key = self._get_default_key(request)
        
        is_allowed, info = await self.is_allowed(key, limit, window_seconds)
        
        if not is_allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": info["limit"],
                    "retry_after": info["retry_after"]
                },
                headers={
                    "X-RateLimit-Limit": str(info["limit"]),
                    "X-RateLimit-Remaining": str(info["remaining"]),
                    "X-RateLimit-Reset": str(info["reset_time"]),
                    "Retry-After": str(info["retry_after"])
                }
            )
        
        return info
    
    def _get_default_key(self, request: Request) -> str:
        """Generate default rate limit key based on IP and user"""
        ip_address = get_remote_address(request)
        
        # If user is authenticated, use user ID
        user_id = getattr(request.state, 'user_id', None)
        if user_id:
            return f"rate_limit:user:{user_id}"
        
        # Otherwise use IP address
        return f"rate_limit:ip:{ip_address}"
    
    def get_user_key(self, request: Request) -> str:
        """Generate rate limit key for authenticated user"""
        user_id = getattr(request.state, 'user_id', None)
        if user_id:
            return f"rate_limit:user:{user_id}"
        
        # Fallback to IP
        ip_address = get_remote_address(request)
        return f"rate_limit:ip:{ip_address}"
    
    def get_ip_key(self, request: Request) -> str:
        """Generate rate limit key for IP address"""
        ip_address = get_remote_address(request)
        return f"rate_limit:ip:{ip_address}"
    
    def get_endpoint_key(self, request: Request) -> str:
        """Generate rate limit key for specific endpoint"""
        ip_address = get_remote_address(request)
        endpoint = f"{request.method}:{request.url.path}"
        return f"rate_limit:endpoint:{endpoint}:ip:{ip_address}"


# Global rate limiter instance
rate_limiter = RateLimiter()


# SlowAPI limiter for decorator-based rate limiting
def get_limiter_key(request: Request) -> str:
    """Key function for SlowAPI limiter"""
    return rate_limiter._get_default_key(request)


limiter = Limiter(key_func=get_limiter_key)


# Rate limit decorators for different scenarios
def rate_limit_per_user(limit: str = "60/minute"):
    """Rate limit per authenticated user"""
    def key_func(request: Request) -> str:
        return rate_limiter.get_user_key(request)
    
    return limiter.limit(limit, key_func=key_func)


def rate_limit_per_ip(limit: str = "100/minute"):
    """Rate limit per IP address"""
    def key_func(request: Request) -> str:
        return rate_limiter.get_ip_key(request)
    
    return limiter.limit(limit, key_func=key_func)


def rate_limit_per_endpoint(limit: str = "30/minute"):
    """Rate limit per endpoint per IP"""
    def key_func(request: Request) -> str:
        return rate_limiter.get_endpoint_key(request)
    
    return limiter.limit(limit, key_func=key_func)


# Specific rate limits for different endpoint types
rate_limit_auth = rate_limit_per_ip("5/minute")  # Strict for auth endpoints
rate_limit_api = rate_limit_per_user("60/minute")  # Standard for API
rate_limit_search = rate_limit_per_user("30/minute")  # Moderate for search
rate_limit_upload = rate_limit_per_user("10/minute")  # Conservative for uploads