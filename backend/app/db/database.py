"""
Database configuration and connection management
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

# Global variables for database engine and session maker
engine: AsyncEngine = None
async_session_maker: async_sessionmaker[AsyncSession] = None


class Base(DeclarativeBase):
    """Base class for all database models"""
    pass


async def init_db() -> None:
    """Initialize database engine and session maker"""
    global engine, async_session_maker
    
    try:
        # Create async engine with connection pooling
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,  # Log SQL queries in debug mode
            pool_size=settings.DATABASE_POOL_SIZE,
            max_overflow=settings.DATABASE_MAX_OVERFLOW,
            pool_pre_ping=True,  # Validate connections before use
            pool_recycle=3600,   # Recycle connections every hour
            # Use NullPool for testing to avoid connection issues
            poolclass=NullPool if "test" in settings.DATABASE_URL else None,
        )
        
        # Create session maker
        async_session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        logger.info("Database engine initialized successfully")
        
    except Exception as e:
        logger.error("Failed to initialize database", error=str(e))
        raise


async def close_db() -> None:
    """Close database connections"""
    global engine
    
    if engine:
        await engine.dispose()
        logger.info("Database connections closed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session
    
    Yields:
        AsyncSession: Database session
    """
    if not async_session_maker:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error("Database session error", error=str(e))
            raise
        finally:
            await session.close()


async def create_tables() -> None:
    """Create all database tables"""
    if not engine:
        raise RuntimeError("Database engine not initialized")
    
    async with engine.begin() as conn:
        # Import all models to ensure they are registered
        from app.models import user, movie, review  # noqa
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")


async def drop_tables() -> None:
    """Drop all database tables (for testing)"""
    if not engine:
        raise RuntimeError("Database engine not initialized")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Database tables dropped successfully")