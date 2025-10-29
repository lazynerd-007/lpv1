#!/usr/bin/env python3
"""
Test password verification logic
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from passlib.context import CryptContext

def test_password_verification():
    """Test password hashing and verification"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Test password
    test_password = "TestPassword123!"
    
    print(f"Testing password: {test_password}")
    
    # Hash the password
    hashed = pwd_context.hash(test_password)
    print(f"Hashed password: {hashed}")
    
    # Verify the password
    is_valid = pwd_context.verify(test_password, hashed)
    print(f"Password verification: {is_valid}")
    
    # Test with wrong password
    wrong_password = "WrongPassword123!"
    is_wrong_valid = pwd_context.verify(wrong_password, hashed)
    print(f"Wrong password verification: {is_wrong_valid}")
    
    # Test with the exact password from registration
    # This is the password that should be used during login
    registration_password = "TestPassword123!"
    is_registration_valid = pwd_context.verify(registration_password, hashed)
    print(f"Registration password verification: {is_registration_valid}")
    
    return is_valid and not is_wrong_valid and is_registration_valid

if __name__ == "__main__":
    success = test_password_verification()
    if success:
        print("\n✅ Password verification works correctly")
    else:
        print("\n❌ Password verification failed")
        sys.exit(1)