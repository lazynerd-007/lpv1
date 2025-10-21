"""
Tests for custom exceptions
"""
import pytest
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    LemonPieException,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    ConflictError,
    RateLimitError,
    lemonnpie_exception_handler,
)


def test_lemonnpie_exception():
    """Test base LemonPieException"""
    exc = LemonPieException("Test error", 500, {"key": "value"})
    
    assert exc.message == "Test error"
    assert exc.status_code == 500
    assert exc.details == {"key": "value"}
    assert str(exc) == "Test error"


def test_authentication_error():
    """Test AuthenticationError"""
    exc = AuthenticationError()
    
    assert exc.message == "Authentication required"
    assert exc.status_code == 401
    assert exc.details == {}
    
    # Test custom message
    exc_custom = AuthenticationError("Invalid token")
    assert exc_custom.message == "Invalid token"


def test_authorization_error():
    """Test AuthorizationError"""
    exc = AuthorizationError()
    
    assert exc.message == "Insufficient permissions"
    assert exc.status_code == 403
    assert exc.details == {}


def test_validation_error():
    """Test ValidationError"""
    details = {"field": "email", "error": "Invalid format"}
    exc = ValidationError("Validation failed", details)
    
    assert exc.message == "Validation failed"
    assert exc.status_code == 422
    assert exc.details == details


def test_not_found_error():
    """Test NotFoundError"""
    exc = NotFoundError("User not found")
    
    assert exc.message == "User not found"
    assert exc.status_code == 404
    assert exc.details == {}


def test_conflict_error():
    """Test ConflictError"""
    exc = ConflictError("Email already exists")
    
    assert exc.message == "Email already exists"
    assert exc.status_code == 409
    assert exc.details == {}


def test_rate_limit_error():
    """Test RateLimitError"""
    exc = RateLimitError("Too many requests")
    
    assert exc.message == "Too many requests"
    assert exc.status_code == 429
    assert exc.details == {}


@pytest.mark.asyncio
async def test_lemonnpie_exception_handler():
    """Test LemonNPie exception handler"""
    # Mock request
    class MockRequest:
        def __init__(self, path: str):
            self.url = type('obj', (object,), {'path': path})()
    
    request = MockRequest("/test")
    exc = ValidationError("Test validation error", {"field": "email"})
    
    response = await lemonnpie_exception_handler(request, exc)
    
    assert isinstance(response, JSONResponse)
    assert response.status_code == 422
    
    # Check response content structure
    content = response.body.decode()
    assert "validation" in content
    assert "Test validation error" in content
    assert "field" in content
    assert "/test" in content