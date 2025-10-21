#!/usr/bin/env python3
"""
Core infrastructure test without database dependencies
"""
import os
import asyncio

# Set test environment
os.environ['SECRET_KEY'] = 'test-secret-key-for-testing'
os.environ['DEBUG'] = 'true'

async def test_config():
    """Test configuration loading"""
    print("🧪 Testing configuration...")
    
    from app.core.config import Settings
    settings = Settings()
    
    assert settings.APP_NAME == "LemonNPie Backend API"
    assert settings.DEBUG is True
    assert settings.SECRET_KEY == "test-secret-key-for-testing"
    assert settings.PORT == 8000
    assert settings.HOST == "0.0.0.0"
    
    print("✅ Configuration test passed")

async def test_exceptions():
    """Test custom exceptions"""
    print("🧪 Testing exceptions...")
    
    from app.core.exceptions import (
        AuthenticationError, 
        ValidationError, 
        NotFoundError,
        ConflictError,
        RateLimitError
    )
    
    # Test AuthenticationError
    auth_error = AuthenticationError("Invalid token")
    assert auth_error.status_code == 401
    assert auth_error.message == "Invalid token"
    
    # Test ValidationError
    validation_error = ValidationError("Invalid data", {"field": "email"})
    assert validation_error.status_code == 422
    assert validation_error.details["field"] == "email"
    
    # Test NotFoundError
    not_found_error = NotFoundError("User not found")
    assert not_found_error.status_code == 404
    
    # Test ConflictError
    conflict_error = ConflictError("Email already exists")
    assert conflict_error.status_code == 409
    
    # Test RateLimitError
    rate_limit_error = RateLimitError()
    assert rate_limit_error.status_code == 429
    
    print("✅ Exceptions test passed")

async def test_logging():
    """Test logging configuration"""
    print("🧪 Testing logging...")
    
    from app.core.logging import get_logger, configure_logging
    
    # Configure logging
    configure_logging()
    
    # Get logger
    logger = get_logger("test")
    
    # Test logging (should not raise errors)
    logger.info("Test log message", test_key="test_value")
    
    print("✅ Logging test passed")

async def test_cache_utilities():
    """Test cache utilities without Redis connection"""
    print("🧪 Testing cache utilities...")
    
    from app.cache.redis import cache_key
    
    # Test cache key generation
    key = cache_key("user", "123", "profile")
    assert key == "user:123:profile"
    
    key = cache_key("movie", 456, "reviews")
    assert key == "movie:456:reviews"
    
    key = cache_key("review", "abc", "votes", "helpful")
    assert key == "review:abc:votes:helpful"
    
    print("✅ Cache utilities test passed")

async def test_model_enums():
    """Test model enums without database connection"""
    print("🧪 Testing model enums...")
    
    from app.models.enums import UserRole, ContentType, ModerationStatus
    
    # Test UserRole enum
    assert UserRole.USER == "user"
    assert UserRole.CRITIC == "critic"
    assert UserRole.MODERATOR == "moderator"
    assert UserRole.ADMIN == "admin"
    
    # Test ContentType enum
    assert ContentType.MOVIE == "movie"
    assert ContentType.SERIES == "series"
    
    # Test ModerationStatus enum
    assert ModerationStatus.PENDING == "pending"
    assert ModerationStatus.APPROVED == "approved"
    assert ModerationStatus.REJECTED == "rejected"
    
    print("✅ Model enums test passed")

async def test_config_validation():
    """Test configuration validation"""
    print("🧪 Testing configuration validation...")
    
    from app.core.config import Settings
    from pydantic import ValidationError
    
    # Test valid configuration
    settings = Settings(SECRET_KEY="valid-secret-key")
    assert settings.SECRET_KEY == "valid-secret-key"
    
    # Test CORS origins parsing
    settings = Settings(
        SECRET_KEY="test-key",
        ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
    )
    assert len(settings.ALLOWED_ORIGINS) == 2
    assert "http://localhost:3000" in settings.ALLOWED_ORIGINS
    
    print("✅ Configuration validation test passed")

async def main():
    """Run all core tests"""
    print("🚀 Running LemonNPie Backend Core Infrastructure Tests\n")
    
    try:
        await test_config()
        await test_exceptions()
        await test_logging()
        await test_cache_utilities()
        await test_model_enums()
        await test_config_validation()
        
        print("\n🎉 All core infrastructure tests passed!")
        print("✅ Configuration system working")
        print("✅ Exception handling working")
        print("✅ Logging system working")
        print("✅ Cache utilities working")
        print("✅ Model enums working")
        print("✅ Validation working")
        
        print("\n📝 Note: Database and Redis tests require running services.")
        print("   Use 'docker-compose up postgres redis' to start them.")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)