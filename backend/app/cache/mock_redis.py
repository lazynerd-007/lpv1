"""
Mock Redis implementation for testing without Redis server
"""
from typing import Optional, Any, Union, Dict, List
import json
import asyncio
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger(__name__)

class MockRedis:
    """Mock Redis client for testing"""
    
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._expiry: Dict[str, datetime] = {}
    
    async def ping(self) -> bool:
        """Mock ping"""
        return True
    
    async def get(self, key: str) -> Optional[str]:
        """Mock get"""
        if key in self._expiry and datetime.now() > self._expiry[key]:
            del self._data[key]
            del self._expiry[key]
            return None
        return self._data.get(key)
    
    async def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """Mock set"""
        self._data[key] = value
        if ex:
            self._expiry[key] = datetime.now() + timedelta(seconds=ex)
        return True
    
    async def delete(self, *keys: str) -> int:
        """Mock delete"""
        count = 0
        for key in keys:
            if key in self._data:
                del self._data[key]
                if key in self._expiry:
                    del self._expiry[key]
                count += 1
        return count
    
    async def exists(self, key: str) -> bool:
        """Mock exists"""
        if key in self._expiry and datetime.now() > self._expiry[key]:
            del self._data[key]
            del self._expiry[key]
            return False
        return key in self._data
    
    async def expire(self, key: str, seconds: int) -> bool:
        """Mock expire"""
        if key in self._data:
            self._expiry[key] = datetime.now() + timedelta(seconds=seconds)
            return True
        return False
    
    async def keys(self, pattern: str = "*") -> List[str]:
        """Mock keys with simple pattern matching"""
        if pattern == "*":
            return list(self._data.keys())
        
        # Simple pattern matching for patterns ending with *
        if pattern.endswith("*"):
            prefix = pattern[:-1]
            return [key for key in self._data.keys() if key.startswith(prefix)]
        
        return [key for key in self._data.keys() if key == pattern]
    
    async def incrbyfloat(self, key: str, increment: float) -> float:
        """Mock incrbyfloat"""
        current = float(self._data.get(key, 0))
        new_value = current + increment
        self._data[key] = str(new_value)
        return new_value
    
    async def info(self) -> Dict[str, Any]:
        """Mock info"""
        return {
            "connected_clients": 1,
            "used_memory": len(str(self._data)),
            "used_memory_human": f"{len(str(self._data))}B",
            "keyspace_hits": 100,
            "keyspace_misses": 10,
        }
    
    async def close(self):
        """Mock close"""
        pass

# Global mock Redis instance
mock_redis_client: Optional[MockRedis] = None

async def init_mock_redis() -> None:
    """Initialize mock Redis client"""
    global mock_redis_client
    
    try:
        mock_redis_client = MockRedis()
        await mock_redis_client.ping()
        logger.info("Mock Redis initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize mock Redis", error=str(e))
        raise

async def close_mock_redis() -> None:
    """Close mock Redis connections"""
    global mock_redis_client
    
    if mock_redis_client:
        await mock_redis_client.close()
        mock_redis_client = None
        logger.info("Mock Redis connections closed")

def get_mock_redis_client() -> Optional[MockRedis]:
    """Get mock Redis client"""
    return mock_redis_client