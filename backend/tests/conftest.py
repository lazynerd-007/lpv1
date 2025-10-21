"""
Test configuration and fixtures
"""
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
import redis.asyncio as redis

from app.main import create_app
from app.db.database import Base, get_db
from app.cache.redis import get_redis
from app.core.config import settings


# Test database URL (in-memory SQLite for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Test Redis URL (use a different database for testing)
TEST_REDIS_URL = "redis://localhost:6379/15"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db_engine():
    """Create test database engine"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest.fixture
async def test_db_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    async_session_maker = async_sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session_maker() as session:
        yield session


@pytest.fixture
async def test_redis():
    """Create test Redis client"""
    redis_client = redis.from_url(TEST_REDIS_URL)
    
    # Clear test database
    await redis_client.flushdb()
    
    yield redis_client
    
    # Clean up
    await redis_client.flushdb()
    await redis_client.close()


@pytest.fixture
async def test_app(test_db_session, test_redis):
    """Create test FastAPI application"""
    app = create_app()
    
    # Override dependencies
    app.dependency_overrides[get_db] = lambda: test_db_session
    app.dependency_overrides[get_redis] = lambda: test_redis
    
    yield app
    
    # Clear overrides
    app.dependency_overrides.clear()


@pytest.fixture
async def test_client(test_app) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client"""
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client