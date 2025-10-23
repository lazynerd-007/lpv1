"""
Test configuration and fixtures
"""
import pytest
import pytest_asyncio
import asyncio
import os
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
import redis.asyncio as redis

# Set test environment variables before importing app modules
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["DEBUG"] = "true"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["REDIS_URL"] = "redis://localhost:6379/15"

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


@pytest_asyncio.fixture
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


@pytest_asyncio.fixture
async def test_db_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    async_session_maker = async_sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def test_redis():
    """Create test Redis client or mock if Redis is not available"""
    try:
        redis_client = redis.from_url(TEST_REDIS_URL)
        # Test connection
        await redis_client.ping()
        # Clear test database
        await redis_client.flushdb()
        
        yield redis_client
        
        # Clean up
        await redis_client.flushdb()
        await redis_client.close()
    except Exception:
        # Redis not available, use mock
        from unittest.mock import AsyncMock
        mock_redis = AsyncMock()
        mock_redis.get.return_value = None
        mock_redis.set.return_value = True
        mock_redis.delete.return_value = True
        mock_redis.flushdb.return_value = True
        mock_redis.ping.return_value = True
        
        yield mock_redis


@pytest_asyncio.fixture
async def test_app(test_db_session, test_redis):
    """Create test FastAPI application"""
    app = create_app()
    
    # Override dependencies
    app.dependency_overrides[get_db] = lambda: test_db_session
    app.dependency_overrides[get_redis] = lambda: test_redis
    
    yield app
    
    # Clear overrides
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def async_client(test_app) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client"""
    from httpx import ASGITransport
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def admin_token(test_db_session: AsyncSession) -> str:
    """Create admin user and return JWT token"""
    from app.models.user import User, UserRole
    from app.auth.jwt_service import JWTService
    
    # Create admin user
    admin_user = User(
        email="admin@example.com",
        password_hash="hashed_password",
        name="Admin User",
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True
    )
    test_db_session.add(admin_user)
    await test_db_session.commit()
    await test_db_session.refresh(admin_user)
    
    # Generate JWT token
    jwt_service = JWTService()
    token = jwt_service.create_access_token(admin_user.id, admin_user.email, admin_user.role)
    return token