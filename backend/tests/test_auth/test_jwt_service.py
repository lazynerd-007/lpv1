"""
Tests for JWT authentication service
"""
import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from app.auth.jwt_service import JWTService
from app.models.enums import UserRole


class TestJWTService:
    """Test JWT service functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.jwt_service = JWTService()
        self.test_user_id = uuid4()
        self.test_email = "test@example.com"
        self.test_role = UserRole.USER
        self.test_password = "TestPassword123!"
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        # Hash password
        hashed = self.jwt_service.hash_password(self.test_password)
        
        # Verify correct password
        assert self.jwt_service.verify_password(self.test_password, hashed)
        
        # Verify incorrect password
        assert not self.jwt_service.verify_password("wrong_password", hashed)
    
    def test_create_access_token(self):
        """Test access token creation"""
        token = self.jwt_service.create_access_token(
            user_id=self.test_user_id,
            email=self.test_email,
            role=self.test_role
        )
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token payload
        payload = self.jwt_service.verify_token(token)
        assert payload["sub"] == str(self.test_user_id)
        assert payload["email"] == self.test_email
        assert payload["role"] == self.test_role.value
        assert payload["type"] == "access"
    
    def test_create_refresh_token(self):
        """Test refresh token creation"""
        token = self.jwt_service.create_refresh_token(
            user_id=self.test_user_id,
            email=self.test_email
        )
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token payload
        payload = self.jwt_service.verify_token(token)
        assert payload["sub"] == str(self.test_user_id)
        assert payload["email"] == self.test_email
        assert payload["type"] == "refresh"
    
    def test_token_expiration(self):
        """Test token expiration"""
        # Create token with short expiration
        short_expiry = timedelta(seconds=1)
        token = self.jwt_service.create_access_token(
            user_id=self.test_user_id,
            email=self.test_email,
            role=self.test_role,
            expires_delta=short_expiry
        )
        
        # Token should be valid initially
        assert not self.jwt_service.is_token_expired(token)
        
        # Wait for token to expire
        import time
        time.sleep(2)
        
        # Token should now be expired
        assert self.jwt_service.is_token_expired(token)
    
    def test_get_user_id_from_token(self):
        """Test extracting user ID from token"""
        token = self.jwt_service.create_access_token(
            user_id=self.test_user_id,
            email=self.test_email,
            role=self.test_role
        )
        
        extracted_id = self.jwt_service.get_user_id_from_token(token)
        assert extracted_id == self.test_user_id
    
    def test_get_user_role_from_token(self):
        """Test extracting user role from token"""
        token = self.jwt_service.create_access_token(
            user_id=self.test_user_id,
            email=self.test_email,
            role=self.test_role
        )
        
        extracted_role = self.jwt_service.get_user_role_from_token(token)
        assert extracted_role == self.test_role
    
    def test_invalid_token(self):
        """Test handling of invalid tokens"""
        from fastapi import HTTPException
        
        # Test completely invalid token
        with pytest.raises(HTTPException):
            self.jwt_service.verify_token("invalid_token")
        
        # Test malformed token
        with pytest.raises(HTTPException):
            self.jwt_service.verify_token("header.payload.signature")
    
    def test_refresh_access_token(self):
        """Test refreshing access token"""
        # Create refresh token
        refresh_token = self.jwt_service.create_refresh_token(
            user_id=self.test_user_id,
            email=self.test_email
        )
        
        # Refresh access token
        new_access_token = self.jwt_service.refresh_access_token(refresh_token)
        
        assert isinstance(new_access_token, str)
        assert len(new_access_token) > 0
        
        # Verify new token
        payload = self.jwt_service.verify_token(new_access_token)
        assert payload["sub"] == str(self.test_user_id)
        assert payload["email"] == self.test_email
        assert payload["type"] == "access"
    
    def test_refresh_with_access_token_fails(self):
        """Test that refresh fails with access token"""
        from fastapi import HTTPException
        
        # Create access token
        access_token = self.jwt_service.create_access_token(
            user_id=self.test_user_id,
            email=self.test_email,
            role=self.test_role
        )
        
        # Try to refresh with access token (should fail)
        with pytest.raises(HTTPException):
            self.jwt_service.refresh_access_token(access_token)