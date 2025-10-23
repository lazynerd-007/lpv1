#!/usr/bin/env python3
"""
Simple authentication tests without pytest
"""
import sys
import os
import asyncio
from uuid import uuid4

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Set environment variables for testing
os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
os.environ["DEBUG"] = "true"

def test_jwt_service():
    """Test JWT service functionality"""
    print("Testing JWT Service...")
    
    from app.auth.jwt_service import JWTService
    from app.models.enums import UserRole
    
    jwt_service = JWTService()
    test_user_id = uuid4()
    test_email = "test@example.com"
    test_role = UserRole.USER
    test_password = "TestPassword123!"
    
    # Test password hashing
    print("  ✓ Testing password hashing...")
    hashed = jwt_service.hash_password(test_password)
    assert jwt_service.verify_password(test_password, hashed), "Password verification failed"
    assert not jwt_service.verify_password("wrong_password", hashed), "Wrong password should not verify"
    print("    ✓ Password hashing works correctly")
    
    # Test access token creation
    print("  ✓ Testing access token creation...")
    access_token = jwt_service.create_access_token(
        user_id=test_user_id,
        email=test_email,
        role=test_role
    )
    assert isinstance(access_token, str), "Access token should be a string"
    assert len(access_token) > 0, "Access token should not be empty"
    print("    ✓ Access token created successfully")
    
    # Test token verification
    print("  ✓ Testing token verification...")
    payload = jwt_service.verify_token(access_token)
    assert payload["sub"] == str(test_user_id), "User ID mismatch in token"
    assert payload["email"] == test_email, "Email mismatch in token"
    assert payload["role"] == test_role.value, "Role mismatch in token"
    assert payload["type"] == "access", "Token type should be access"
    print("    ✓ Token verification works correctly")
    
    # Test refresh token creation
    print("  ✓ Testing refresh token creation...")
    refresh_token = jwt_service.create_refresh_token(
        user_id=test_user_id,
        email=test_email
    )
    assert isinstance(refresh_token, str), "Refresh token should be a string"
    assert len(refresh_token) > 0, "Refresh token should not be empty"
    
    refresh_payload = jwt_service.verify_token(refresh_token)
    assert refresh_payload["type"] == "refresh", "Token type should be refresh"
    print("    ✓ Refresh token created successfully")
    
    # Test user ID extraction
    print("  ✓ Testing user ID extraction...")
    extracted_id = jwt_service.get_user_id_from_token(access_token)
    assert extracted_id == test_user_id, "Extracted user ID should match original"
    print("    ✓ User ID extraction works correctly")
    
    # Test role extraction
    print("  ✓ Testing role extraction...")
    extracted_role = jwt_service.get_user_role_from_token(access_token)
    assert extracted_role == test_role, "Extracted role should match original"
    print("    ✓ Role extraction works correctly")
    
    print("✅ JWT Service tests passed!")


def test_security_utils():
    """Test security utilities"""
    print("Testing Security Utils...")
    
    from app.auth.security import SecurityUtils
    
    security_utils = SecurityUtils()
    
    # Test HTML sanitization
    print("  ✓ Testing HTML sanitization...")
    dangerous_html = "<script>alert('xss')</script>Hello World"
    sanitized = security_utils.sanitize_html(dangerous_html)
    assert "<script>" not in sanitized, "Script tags should be removed"
    assert "Hello World" in sanitized, "Safe content should remain"
    print("    ✓ HTML sanitization works correctly")
    
    # Test SQL injection validation
    print("  ✓ Testing SQL injection validation...")
    safe_text = "This is a normal text"
    assert security_utils.validate_no_sql_injection(safe_text), "Safe text should pass validation"
    
    dangerous_sql = "'; DROP TABLE users; --"
    assert not security_utils.validate_no_sql_injection(dangerous_sql), "SQL injection should be detected"
    print("    ✓ SQL injection validation works correctly")
    
    # Test email validation
    print("  ✓ Testing email validation...")
    valid_email = "test@example.com"
    assert security_utils.validate_email_format(valid_email), "Valid email should pass"
    
    invalid_email = "invalid_email"
    assert not security_utils.validate_email_format(invalid_email), "Invalid email should fail"
    print("    ✓ Email validation works correctly")
    
    # Test URL validation
    print("  ✓ Testing URL validation...")
    valid_url = "https://example.com"
    assert security_utils.validate_url(valid_url), "Valid URL should pass"
    
    invalid_url = "javascript:alert('xss')"
    assert not security_utils.validate_url(invalid_url), "Dangerous URL should fail"
    print("    ✓ URL validation works correctly")
    
    # Test password strength validation
    print("  ✓ Testing password strength validation...")
    strong_password = "MySecure123!"
    result = security_utils.validate_password_strength(strong_password)
    assert result["valid"], f"Strong password should be valid. Errors: {result['errors']}"
    assert result["strength"] in ["strong", "very_strong"], "Strong password should have good strength"
    
    weak_password = "weak"
    result = security_utils.validate_password_strength(weak_password)
    assert not result["valid"], "Weak password should be invalid"
    assert len(result["errors"]) > 0, "Weak password should have errors"
    print("    ✓ Password strength validation works correctly")
    
    print("✅ Security Utils tests passed!")


def test_schemas():
    """Test authentication schemas"""
    print("Testing Authentication Schemas...")
    
    from app.schemas.auth import UserRegistration, UserLogin, TokenResponse
    from pydantic import ValidationError
    
    # Test valid user registration
    print("  ✓ Testing user registration schema...")
    valid_registration = {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "name": "Test User",
        "bio": "Test bio",
        "location": "Test Location"
    }
    
    try:
        user_reg = UserRegistration(**valid_registration)
        assert user_reg.email == "test@example.com"
        assert user_reg.name == "Test User"
        print("    ✓ Valid registration data accepted")
    except ValidationError as e:
        print(f"    ❌ Validation error: {e}")
        raise
    
    # Test invalid email
    print("  ✓ Testing invalid email validation...")
    invalid_email_data = valid_registration.copy()
    invalid_email_data["email"] = "invalid_email"
    
    try:
        UserRegistration(**invalid_email_data)
        assert False, "Invalid email should raise validation error"
    except ValidationError:
        print("    ✓ Invalid email correctly rejected")
    
    # Test weak password
    print("  ✓ Testing weak password validation...")
    weak_password_data = valid_registration.copy()
    weak_password_data["password"] = "weak"
    
    try:
        UserRegistration(**weak_password_data)
        assert False, "Weak password should raise validation error"
    except ValidationError:
        print("    ✓ Weak password correctly rejected")
    
    # Test user login schema
    print("  ✓ Testing user login schema...")
    valid_login = {
        "email": "test@example.com",
        "password": "TestPassword123!"
    }
    
    try:
        user_login = UserLogin(**valid_login)
        assert user_login.email == "test@example.com"
        print("    ✓ Valid login data accepted")
    except ValidationError as e:
        print(f"    ❌ Validation error: {e}")
        raise
    
    # Test token response schema
    print("  ✓ Testing token response schema...")
    token_data = {
        "access_token": "mock_access_token",
        "refresh_token": "mock_refresh_token",
        "token_type": "bearer",
        "expires_in": 1800
    }
    
    try:
        token_response = TokenResponse(**token_data)
        assert token_response.access_token == "mock_access_token"
        assert token_response.token_type == "bearer"
        print("    ✓ Token response schema works correctly")
    except ValidationError as e:
        print(f"    ❌ Validation error: {e}")
        raise
    
    print("✅ Authentication Schemas tests passed!")


def main():
    """Run all tests"""
    print("🚀 Running Authentication System Tests\n")
    
    try:
        test_jwt_service()
        print()
        test_security_utils()
        print()
        test_schemas()
        print()
        print("🎉 All authentication tests passed successfully!")
        return 0
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)