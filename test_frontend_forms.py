#!/usr/bin/env python3
"""
Frontend Forms Integration Test
Tests the complete user registration and login flow to verify frontend integration.
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000/api/v1"
FRONTEND_URL = "http://localhost:5173"

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    print("🌐 Testing Frontend Accessibility")
    print("=" * 50)
    
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            print(f"✅ Frontend accessible at {FRONTEND_URL}")
            print(f"Status: {response.status_code}")
            return True
        else:
            print(f"❌ Frontend returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend not accessible: {e}")
        return False

def test_backend_accessibility():
    """Test if backend is accessible"""
    print("\n🔧 Testing Backend Accessibility")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Backend accessible at {BACKEND_URL}")
            print(f"Status: {response.status_code}")
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_registration_flow():
    """Test complete registration flow"""
    print("\n📝 Testing Registration Flow")
    print("=" * 50)
    
    # Generate unique test data
    timestamp = int(time.time())
    test_data = {
        "email": f"testuser{timestamp}@example.com",
        "password": "TestPassword123!",
        "name": "Test User",
        "bio": "This is a test user for frontend integration",
        "location": "Test City, Test Country"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/register",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Registration Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registration successful!")
            print(f"User ID: {data.get('user', {}).get('id')}")
            print(f"User Name: {data.get('user', {}).get('name')}")
            print(f"User Email: {data.get('user', {}).get('email')}")
            print(f"Access Token: {data.get('access_token', 'N/A')[:20]}...")
            return test_data, data
        else:
            print(f"❌ Registration failed: {response.text}")
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Registration request failed: {e}")
        return None, None

def test_login_flow(test_data):
    """Test complete login flow"""
    print("\n🔐 Testing Login Flow")
    print("=" * 50)
    
    if not test_data:
        print("❌ No test data available for login test")
        return None
    
    login_data = {
        "email": test_data["email"],
        "password": test_data["password"]
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"User ID: {data.get('user', {}).get('id')}")
            print(f"User Name: {data.get('user', {}).get('name')}")
            print(f"User Email: {data.get('user', {}).get('email')}")
            print(f"Access Token: {data.get('access_token', 'N/A')[:20]}...")
            return data
        else:
            print(f"❌ Login failed: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Login request failed: {e}")
        return None

def test_authenticated_request(auth_data):
    """Test authenticated request to verify token works"""
    print("\n👤 Testing Authenticated Request")
    print("=" * 50)
    
    if not auth_data or 'access_token' not in auth_data:
        print("❌ No authentication data available")
        return False
    
    headers = {
        "Authorization": f"Bearer {auth_data['access_token']}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/users/me",
            headers=headers,
            timeout=10
        )
        
        print(f"Profile Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Authenticated request successful!")
            print(f"User ID: {data.get('id')}")
            print(f"User Name: {data.get('name')}")
            print(f"User Email: {data.get('email')}")
            print(f"User Bio: {data.get('bio')}")
            print(f"User Location: {data.get('location')}")
            return True
        else:
            print(f"❌ Authenticated request failed: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Authenticated request failed: {e}")
        return False

def main():
    """Run all frontend integration tests"""
    print("🧪 Frontend Forms Integration Test")
    print("=" * 60)
    
    # Test accessibility
    frontend_ok = test_frontend_accessibility()
    backend_ok = test_backend_accessibility()
    
    if not frontend_ok or not backend_ok:
        print("\n❌ Prerequisites not met. Cannot proceed with form tests.")
        return False
    
    # Test registration flow
    test_data, reg_data = test_registration_flow()
    if not test_data or not reg_data:
        print("\n❌ Registration flow failed. Cannot proceed with login test.")
        return False
    
    # Test login flow
    login_data = test_login_flow(test_data)
    if not login_data:
        print("\n❌ Login flow failed.")
        return False
    
    # Test authenticated request
    auth_ok = test_authenticated_request(login_data)
    if not auth_ok:
        print("\n❌ Authenticated request failed.")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All frontend form integration tests passed!")
    print("✅ Registration form should work correctly")
    print("✅ Login form should work correctly")
    print("✅ Authentication flow is working end-to-end")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)