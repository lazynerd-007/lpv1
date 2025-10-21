"""
Tests for main FastAPI application
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(test_client: AsyncClient):
    """Test health check endpoint"""
    response = await test_client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert data["service"] == "LemonNPie Backend API"
    assert data["version"] == "1.0.0"


@pytest.mark.asyncio
async def test_root_endpoint(test_client: AsyncClient):
    """Test root endpoint"""
    response = await test_client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "Welcome to LemonNPie Backend API" in data["message"]
    assert data["version"] == "1.0.0"
    assert "docs" in data


@pytest.mark.asyncio
async def test_cors_headers(test_client: AsyncClient):
    """Test CORS headers are present"""
    response = await test_client.options("/health")
    
    # Should have CORS headers
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers


@pytest.mark.asyncio
async def test_404_error_handling(test_client: AsyncClient):
    """Test 404 error handling"""
    response = await test_client.get("/nonexistent-endpoint")
    
    assert response.status_code == 404
    data = response.json()
    
    assert data["error"] == "http_error"
    assert "Not Found" in data["message"]
    assert "timestamp" in data
    assert "path" in data


@pytest.mark.asyncio
async def test_method_not_allowed(test_client: AsyncClient):
    """Test method not allowed error handling"""
    response = await test_client.post("/health")
    
    assert response.status_code == 405
    data = response.json()
    
    assert data["error"] == "http_error"
    assert "Method Not Allowed" in data["message"]


@pytest.mark.asyncio
async def test_application_startup():
    """Test application can be created without errors"""
    from app.main import create_app
    
    app = create_app()
    
    assert app.title == "LemonNPie Backend API"
    assert app.version == "1.0.0"
    assert "Backend API for LemonNPie" in app.description


@pytest.mark.asyncio
async def test_middleware_configuration():
    """Test middleware is properly configured"""
    from app.main import create_app
    
    app = create_app()
    
    # Check that middleware is added
    middleware_classes = [middleware.cls.__name__ for middleware in app.user_middleware]
    
    assert "CORSMiddleware" in middleware_classes
    assert "LoggingMiddleware" in middleware_classes


@pytest.mark.asyncio
async def test_exception_handlers():
    """Test exception handlers are registered"""
    from app.main import create_app
    from app.core.exceptions import LemonPieException
    from fastapi import HTTPException
    
    app = create_app()
    
    # Check exception handlers are registered
    assert LemonPieException in app.exception_handlers
    assert HTTPException in app.exception_handlers
    assert Exception in app.exception_handlers