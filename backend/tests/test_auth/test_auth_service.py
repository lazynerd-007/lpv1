"""
Tests for authentication service
"""
import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from app.auth.auth_service import AuthService
from app.schemas.auth import UserRegistration, UserLogin
from app.models.user import User
from app.models.enums import UserRole


class TestAuthService:
    """Test authentication service functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.auth_service = AuthService()
        self.test_user_data = UserRegistration(
            email="test@example.com",
            password="TestPassword123!",
            name="Test User",
            bio="Test bio",
            location="Test Location"
        )
        self.test_login_data = UserLogin(
            email="test@example.com",
            password="TestPassword123!"
        )
    
    @pytest.mark.asyncio
    async def test_register_user_success(self):
        """Test successful user registration"""
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock user doesn't exist
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        
        # Mock user creation
        mock_user = User(
            id=uuid4(),
            email=self.test_user_data.email,
            name=self.test_user_data.name,
            role=UserRole.USER,
            is_active=True,
            is_verified=False
        )
        mock_db.refresh = AsyncMock()
        
        with patch('app.auth.auth_service.User', return_value=mock_user):
            response = await self.auth_service.register_user(self.test_user_data, mock_db)
        
        # Verify response
        assert response.user.email == self.test_user_data.email
        assert response.user.name == self.test_user_data.name
        assert response.user.role == UserRole.USER
        assert response.tokens.access_token is not None
        assert response.tokens.refresh_token is not None
        
        # Verify database calls
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_register_user_duplicate_email(self):
        """Test registration with duplicate email"""
        from fastapi import HTTPException
        
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock existing user
        existing_user = User(
            id=uuid4(),
            email=self.test_user_data.email,
            name="Existing User",
            role=UserRole.USER
        )
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = existing_user
        mock_db.execute.return_value = mock_result
        
        # Should raise conflict exception
        with pytest.raises(HTTPException) as exc_info:
            await self.auth_service.register_user(self.test_user_data, mock_db)
        
        assert exc_info.value.status_code == 409
        assert "already exists" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_authenticate_user_success(self):
        """Test successful user authentication"""
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock existing user with hashed password
        from app.auth.jwt_service import jwt_service
        hashed_password = jwt_service.hash_password(self.test_login_data.password)
        
        mock_user = User(
            id=uuid4(),
            email=self.test_login_data.email,
            password_hash=hashed_password,
            name="Test User",
            role=UserRole.USER,
            is_active=True,
            login_attempts=0,
            locked_until=None
        )
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result
        
        response = await self.auth_service.authenticate_user(self.test_login_data, mock_db)
        
        # Verify response
        assert response.user.email == self.test_login_data.email
        assert response.tokens.access_token is not None
        assert response.tokens.refresh_token is not None
    
    @pytest.mark.asyncio
    async def test_authenticate_user_not_found(self):
        """Test authentication with non-existent user"""
        from fastapi import HTTPException
        
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock user not found
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        
        # Should raise unauthorized exception
        with pytest.raises(HTTPException) as exc_info:
            await self.auth_service.authenticate_user(self.test_login_data, mock_db)
        
        assert exc_info.value.status_code == 401
        assert "Invalid email or password" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self):
        """Test authentication with wrong password"""
        from fastapi import HTTPException
        
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock existing user with different password
        from app.auth.jwt_service import jwt_service
        hashed_password = jwt_service.hash_password("different_password")
        
        mock_user = User(
            id=uuid4(),
            email=self.test_login_data.email,
            password_hash=hashed_password,
            name="Test User",
            role=UserRole.USER,
            is_active=True,
            login_attempts=0,
            locked_until=None
        )
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result
        
        # Should raise unauthorized exception
        with pytest.raises(HTTPException) as exc_info:
            await self.auth_service.authenticate_user(self.test_login_data, mock_db)
        
        assert exc_info.value.status_code == 401
        assert "Invalid email or password" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_authenticate_user_inactive(self):
        """Test authentication with inactive user"""
        from fastapi import HTTPException
        
        # Mock database session
        mock_db = AsyncMock()
        
        # Mock inactive user
        from app.auth.jwt_service import jwt_service
        hashed_password = jwt_service.hash_password(self.test_login_data.password)
        
        mock_user = User(
            id=uuid4(),
            email=self.test_login_data.email,
            password_hash=hashed_password,
            name="Test User",
            role=UserRole.USER,
            is_active=False,  # Inactive user
            login_attempts=0,
            locked_until=None
        )
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result
        
        # Should raise unauthorized exception
        with pytest.raises(HTTPException) as exc_info:
            await self.auth_service.authenticate_user(self.test_login_data, mock_db)
        
        assert exc_info.value.status_code == 401
        assert "deactivated" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_refresh_token_success(self):
        """Test successful token refresh"""
        # Mock database session
        mock_db = AsyncMock()
        
        # Create a valid refresh token
        from app.auth.jwt_service import jwt_service
        user_id = uuid4()
        refresh_token = jwt_service.create_refresh_token(
            user_id=user_id,
            email="test@example.com"
        )
        
        # Mock user exists and is active
        mock_user = User(
            id=user_id,
            email="test@example.com",
            name="Test User",
            role=UserRole.USER,
            is_active=True
        )
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result
        
        response = await self.auth_service.refresh_token(refresh_token, mock_db)
        
        # Verify response
        assert response.access_token is not None
        assert response.refresh_token == refresh_token  # Same refresh token
        assert response.token_type == "bearer"
    
    @pytest.mark.asyncio
    async def test_refresh_token_user_not_found(self):
        """Test token refresh with non-existent user"""
        from fastapi import HTTPException
        
        # Mock database session
        mock_db = AsyncMock()
        
        # Create a valid refresh token
        from app.auth.jwt_service import jwt_service
        user_id = uuid4()
        refresh_token = jwt_service.create_refresh_token(
            user_id=user_id,
            email="test@example.com"
        )
        
        # Mock user not found
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        
        # Should raise unauthorized exception
        with pytest.raises(HTTPException) as exc_info:
            await self.auth_service.refresh_token(refresh_token, mock_db)
        
        assert exc_info.value.status_code == 401
        assert "not found or inactive" in exc_info.value.detail