#!/usr/bin/env python3
"""
Simple test to verify infrastructure components work
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
    
    print("✅ Configuration test passed")

async def test_exceptions():
    """Test custom exceptions"""
    print("🧪 Testing exceptions...")
    
    from app.core.exceptions import (
        AuthenticationError, 
        ValidationError, 
        NotFoundError
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
    
    print("✅ Exceptions test passed")

async def test_fastapi_app():
    """Test FastAPI application creation"""
    print("🧪 Testing FastAPI application...")
    
    from app.main import create_app
    
    app = create_app()
    
    assert app.title == "LemonNPie Backend API"
    assert app.version == "1.0.0"
    assert "Backend API for LemonNPie" in app.description
    
    print("✅ FastAPI application test passed")

async def test_cache_key_generation():
    """Test cache key generation"""
    print("🧪 Testing cache utilities...")
    
    from app.cache.redis import cache_key
    
    key = cache_key("user", "123", "profile")
    assert key == "user:123:profile"
    
    key = cache_key("movie", 456, "reviews")
    assert key == "movie:456:reviews"
    
    print("✅ Cache utilities test passed")

async def main():
    """Run all tests"""
    print("🚀 Running LemonNPie Backend Infrastructure Tests\n")
    
    try:
        await test_config()
        await test_exceptions()
        await test_fastapi_app()
        await test_cache_key_generation()
        
        print("\n🎉 All tests passed! Infrastructure is working correctly.")
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)