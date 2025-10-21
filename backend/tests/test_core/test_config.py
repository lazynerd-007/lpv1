"""
Tests for core configuration
"""
import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_settings_default_values():
    """Test default configuration values"""
    settings = Settings()
    
    assert settings.APP_NAME == "LemonNPie Backend API"
    assert settings.APP_VERSION == "1.0.0"
    assert settings.DEBUG is False
    assert settings.HOST == "0.0.0.0"
    assert settings.PORT == 8000
    assert settings.DATABASE_POOL_SIZE == 20
    assert settings.REDIS_POOL_SIZE == 10
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
    assert settings.LOG_LEVEL == "INFO"


def test_settings_cors_origins_parsing():
    """Test CORS origins parsing from string"""
    settings = Settings(ALLOWED_ORIGINS="http://localhost:3000,http://localhost:5173")
    
    assert len(settings.ALLOWED_ORIGINS) == 2
    assert "http://localhost:3000" in settings.ALLOWED_ORIGINS
    assert "http://localhost:5173" in settings.ALLOWED_ORIGINS


def test_settings_secret_key_validation():
    """Test secret key validation"""
    # Should raise error for default secret key
    with pytest.raises(ValidationError) as exc_info:
        Settings(SECRET_KEY="your-secret-key-change-in-production")
    
    assert "Please change the SECRET_KEY in production" in str(exc_info.value)
    
    # Should work with custom secret key
    settings = Settings(SECRET_KEY="my-custom-secret-key")
    assert settings.SECRET_KEY == "my-custom-secret-key"


def test_settings_database_url():
    """Test database URL configuration"""
    custom_db_url = "postgresql+asyncpg://user:pass@localhost:5432/testdb"
    settings = Settings(DATABASE_URL=custom_db_url)
    
    assert settings.DATABASE_URL == custom_db_url


def test_settings_redis_url():
    """Test Redis URL configuration"""
    custom_redis_url = "redis://localhost:6379/1"
    settings = Settings(REDIS_URL=custom_redis_url)
    
    assert settings.REDIS_URL == custom_redis_url


def test_settings_environment_variables(monkeypatch):
    """Test settings from environment variables"""
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("PORT", "9000")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    
    settings = Settings()
    
    assert settings.DEBUG is True
    assert settings.PORT == 9000
    assert settings.LOG_LEVEL == "DEBUG"
    assert settings.SECRET_KEY == "test-secret-key"