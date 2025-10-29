#!/usr/bin/env python3
"""
Test script to check existing users and test registration functionality
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_existing_users():
    """Check if there are any existing users (if there's an endpoint for this)"""
    print("=== Checking for existing users ===")
    
    # Try to get users (this might not exist, but let's try)
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users/")
        print(f"GET /api/v1/users/ - Status: {response.status_code}")
        if response.status_code == 200:
            users = response.json()
            print(f"Found {len(users)} users")
            for user in users:
                print(f"  - {user.get('email', 'No email')} (ID: {user.get('id', 'No ID')})")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error checking users: {e}")

def test_registration():
    """Test user registration"""
    print("\n=== Testing Registration ===")
    
    # Test user data - simple password to avoid bcrypt issues
    test_user = {
        "email": "test@example.com",
        "password": "Test123!",  # Simple but valid password
        "name": "Test User",  # Required field
        "bio": "Test user",  # Optional field
        "location": "Test City"  # Optional field
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"POST /api/v1/auth/register - Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return test_user
        elif response.status_code == 400:
            print("⚠️  User might already exist or validation error")
        else:
            print("❌ Registration failed")
            
    except Exception as e:
        print(f"Error during registration: {e}")
    
    return None

def test_login(user_data):
    """Test user login"""
    print("\n=== Testing Login ===")
    
    if not user_data:
        print("No user data provided, skipping login test")
        return
    
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"POST /api/v1/auth/login - Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            data = response.json()
            if "access_token" in data:
                print(f"Access token received: {data['access_token'][:20]}...")
        elif response.status_code == 401:
            print("❌ Invalid credentials")
        else:
            print("❌ Login failed")
            
    except Exception as e:
        print(f"Error during login: {e}")

def main():
    print("Testing Authentication System")
    print("=" * 40)
    
    # Check existing users
    test_existing_users()
    
    # Test registration
    user_data = test_registration()
    
    # Test login with the registered user
    test_login(user_data)

if __name__ == "__main__":
    main()