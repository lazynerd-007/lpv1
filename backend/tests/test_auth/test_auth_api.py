"""
Tests for authentication API endpoints
"""
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from app.main import app
from app.models.user import User
from app.models.enums import UserRole


class TestAuthAPI:
    """Test authentication API endpoints"""
    
    @pytest.mark.asyncio
    async def test_register_endpoint_success(self):
        """Test successful user registration endpoint"""
        registration_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "name": "Test User",
            "bio": "Test bio",
            "location": "Test Location"
        }
        
        # Mock the auth service
        with patch('app.api.v1.auth.auth_service') as mock_auth_service:
            # Mock successful registration
            mock_response = AsyncMock()
            mock_response.user.email = registration_data["email"]
            mock_response.user.name = registration_data["name"]
            mock_response.user.role = UserRole.USER
            mock_response.tokens.access_token = "mock_access_token"
            mock_response.tokens.refresh_token = "mock_refresh_token"
            mock_response.tokens.token_type = "bearer"
            mock_response.tokens.expires_in = 1800
            
            mock_auth_service.register_user.return_value = mock_response
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/v1/auth/register", json=registration_data)
            
            assert response.status_code == 201
            data = response.json()
            assert data["user"]["email"] == registration_data["email"]
            assert data["user"]["name"] == registration_data["name"]
            assert "tokens" in data
            assert data["tokens"]["access_token"] == "mock_access_token"
    
    @pytest.mark.asyncio
    async def test_register_endpoint_invalid_email(self):
        """Test registration with invalid email"""
        registration_data = {
            "email": "invalid_email",  # Invalid email format
            "password": "TestPassword123!",
            "name": "Test User"
        }
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/v1/auth/register", json=registration_data)
        
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_register_endpoint_weak_password(self):
        """Test registration with weak password"""
        registration_data = {
            "email": "test@example.com",
            "password": "weak",  # Weak password
            "name": "Test User"
        }
        
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post("/api/v1/auth/register", json=registration_data)
        
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_login_endpoint_success(self):
        """Test successful login endpoint"""
        login_data = {
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        
        # Mock the auth service
        with patch('app.api.v1.auth.auth_service') as mock_auth_service:
            # Mock successful login
            mock_response = AsyncMock()
            mock_response.user.email = login_data["email"]
            mock_response.user.name = "Test User"
            mock_response.user.role = UserRole.USER
            mock_response.tokens.access_token = "mock_access_token"
            mock_response.tokens.refresh_token = "mock_refresh_token"
            mock_response.tokens.token_type = "bearer"
            mock_response.tokens.expires_in = 1800
            
            mock_auth_service.authenticate_user.return_value = mock_response
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/v1/auth/login", json=login_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["user"]["email"] == login_data["email"]
            assert "tokens" in data
            assert data["tokens"]["access_token"] == "mock_access_token"
    
    @pytest.mark.asyncio
    async def test_login_endpoint_invalid_credentials(self):
        """Test login with invalid credentials"""
        from fastapi import HTTPException
        
        login_data = {
            "email": "test@example.com",
            "password": "wrong_password"
        }
        
        # Mock the auth service to raise exception
        with patch('app.api.v1.auth.auth_service') as mock_auth_service:
            mock_auth_service.authenticate_user.side_effect = HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/v1/auth/login", json=login_data)
            
            assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_refresh_token_endpoint_success(self):
        """Test successful token refresh endpoint"""
        refresh_data = {
            "refresh_token": "valid_refresh_token"
        }
        
        # Mock the auth service
        with patch('app.api.v1.auth.auth_service') as mock_auth_service:
            # Mock successful refresh
            mock_response = AsyncMock()
            mock_response.access_token = "new_access_token"
            mock_response.refresh_token = "valid_refresh_token"
            mock_response.token_type = "bearer"
            mock_response.expires_in = 1800
            
            mock_auth_service.refresh_token.return_value = mock_response
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post("/api/v1/auth/refresh", json=refresh_data)
            
            assert response.status_code == 200
            data = response.json()
            assert data["access_token"] == "new_access_token"
            assert data["refresh_token"] == "valid_refresh_token"
    
    @pytest.mark.asyncio
    async def test_me_endpoint_success(self):
        """Test getting current user info"""
        # Mock user
        mock_user = User(
            id=uuid4(),
            email="test@example.com",
            name="Test User",
            role=UserRole.USER,
            is_verified=True,
            is_active=True
        )
        
        # Mock the dependency
        with patch('app.api.v1.auth.get_current_user') as mock_get_user:
            mock_get_user.return_value = mock_user
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.get(
                    "/api/v1/auth/me",
                    headers={"Authorization": "Bearer mock_token"}
                )
            
            assert response.status_code == 200
            data = response.json()
            assert data["email"] == "test@example.com"
            assert data["name"] == "Test User"
            assert data["role"] == "user"
    
    @pytest.mark.asyncio
    async def test_me_endpoint_unauthorized(self):
        """Test getting current user info without token"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/auth/me")
        
        assert response.status_code == 403  # No authorization header
    
    @pytest.mark.asyncio
    async def test_logout_endpoint(self):
        """Test logout endpoint"""
        # Mock user
        mock_user = User(
            id=uuid4(),
            email="test@example.com",
            name="Test User",
            role=UserRole.USER
        )
        
        # Mock the dependency
        with patch('app.api.v1.auth.get_current_user') as mock_get_user:
            mock_get_user.return_value = mock_user
            
            async with AsyncClient(app=app, base_url="http://test") as client:
                response = await client.post(
                    "/api/v1/auth/logout",
                    headers={"Authorization": "Bearer mock_token"}
                )
            
            assert response.status_code == 200
            data = response.json()
            assert "logged out" in data["message"]