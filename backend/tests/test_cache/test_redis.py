"""
Tests for Redis cache service
"""
import pytest
from datetime import timedelta
import json

from app.cache.redis import CacheService, cache_key, cache_result


@pytest.mark.asyncio
async def test_cache_service_basic_operations(test_redis):
    """Test basic cache operations"""
    cache = CacheService(test_redis)
    
    # Test set and get
    await cache.set("test_key", "test_value")
    value = await cache.get("test_key")
    assert value == "test_value"
    
    # Test get with default
    value = await cache.get("nonexistent_key", "default")
    assert value == "default"
    
    # Test exists
    assert await cache.exists("test_key") is True
    assert await cache.exists("nonexistent_key") is False
    
    # Test delete
    assert await cache.delete("test_key") is True
    assert await cache.get("test_key") is None


@pytest.mark.asyncio
async def test_cache_service_ttl(test_redis):
    """Test cache TTL functionality"""
    cache = CacheService(test_redis)
    
    # Test with integer TTL
    await cache.set("ttl_key", "ttl_value", ttl=1)
    assert await cache.get("ttl_key") == "ttl_value"
    
    # Test with timedelta TTL
    await cache.set("timedelta_key", "timedelta_value", ttl=timedelta(seconds=1))
    assert await cache.get("timedelta_key") == "timedelta_value"


@pytest.mark.asyncio
async def test_cache_service_data_types(test_redis):
    """Test caching different data types"""
    cache = CacheService(test_redis)
    
    # Test string
    await cache.set("string_key", "string_value")
    assert await cache.get("string_key") == "string_value"
    
    # Test integer
    await cache.set("int_key", 42)
    assert await cache.get("int_key") == 42
    
    # Test float
    await cache.set("float_key", 3.14)
    assert await cache.get("float_key") == 3.14
    
    # Test boolean
    await cache.set("bool_key", True)
    assert await cache.get("bool_key") is True
    
    # Test list
    test_list = [1, 2, 3, "four"]
    await cache.set("list_key", test_list)
    assert await cache.get("list_key") == test_list
    
    # Test dictionary
    test_dict = {"key1": "value1", "key2": 42, "key3": [1, 2, 3]}
    await cache.set("dict_key", test_dict)
    assert await cache.get("dict_key") == test_dict


@pytest.mark.asyncio
async def test_cache_service_increment(test_redis):
    """Test cache increment functionality"""
    cache = CacheService(test_redis)
    
    # Test increment new key
    result = await cache.increment("counter")
    assert result == 1
    
    # Test increment existing key
    result = await cache.increment("counter", 5)
    assert result == 6
    
    # Test increment by 1 (default)
    result = await cache.increment("counter")
    assert result == 7


@pytest.mark.asyncio
async def test_cache_service_pattern_delete(test_redis):
    """Test pattern-based deletion"""
    cache = CacheService(test_redis)
    
    # Set multiple keys with pattern
    await cache.set("user:1:profile", "profile1")
    await cache.set("user:2:profile", "profile2")
    await cache.set("user:1:settings", "settings1")
    await cache.set("other:key", "other_value")
    
    # Delete keys matching pattern
    deleted_count = await cache.delete_pattern("user:*")
    assert deleted_count == 3
    
    # Verify pattern keys are deleted
    assert await cache.get("user:1:profile") is None
    assert await cache.get("user:2:profile") is None
    assert await cache.get("user:1:settings") is None
    
    # Verify other keys remain
    assert await cache.get("other:key") == "other_value"


@pytest.mark.asyncio
async def test_cache_service_expire(test_redis):
    """Test setting expiration on existing keys"""
    cache = CacheService(test_redis)
    
    # Set key without TTL
    await cache.set("expire_test", "value")
    
    # Set expiration
    result = await cache.expire("expire_test", 1)
    assert result is True
    
    # Key should still exist immediately
    assert await cache.get("expire_test") == "value"


def test_cache_key_generation():
    """Test cache key generation utility"""
    key = cache_key("user", "123", "profile")
    assert key == "user:123:profile"
    
    key = cache_key("movie", 456, "reviews")
    assert key == "movie:456:reviews"


@pytest.mark.asyncio
async def test_cache_result_decorator(test_redis):
    """Test cache result decorator"""
    call_count = 0
    
    @cache_result(ttl=60, key_prefix="test_func")
    async def expensive_function(x, y):
        nonlocal call_count
        call_count += 1
        return x + y
    
    # First call should execute function
    result1 = await expensive_function(1, 2)
    assert result1 == 3
    assert call_count == 1
    
    # Second call should use cache
    result2 = await expensive_function(1, 2)
    assert result2 == 3
    assert call_count == 1  # Should not increment
    
    # Different arguments should execute function again
    result3 = await expensive_function(2, 3)
    assert result3 == 5
    assert call_count == 2


@pytest.mark.asyncio
async def test_cache_service_error_handling(test_redis):
    """Test cache service error handling"""
    cache = CacheService(test_redis)
    
    # Close Redis connection to simulate error
    await test_redis.close()
    
    # Operations should return default values/False instead of raising
    assert await cache.get("test_key", "default") == "default"
    assert await cache.set("test_key", "value") is False
    assert await cache.delete("test_key") is False
    assert await cache.exists("test_key") is False
    assert await cache.increment("counter") == 0
    assert await cache.expire("test_key", 60) is False
    assert await cache.delete_pattern("test:*") == 0