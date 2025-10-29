#!/usr/bin/env python3
"""
Test script to verify frontend integration with backend API
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

# Global variable to store test email
test_email = ""

def test_registration():
    """Test user registration"""
    print("Testing user registration...")
    
    # Use timestamp to ensure unique email
    timestamp = int(time.time())
    email = f"frontend{timestamp}@test.com"
    
    registration_data = {
        "name": "Frontend Test User",
        "email": email,
        "password": "Test123!",
        "bio": "Testing frontend integration",
        "location": "Test City"
    }
    
    # Store email for login test
    global test_email
    test_email = email
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=registration_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Registration Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Registration successful!")
            print(f"User ID: {data['user']['id']}")
            print(f"User Name: {data['user']['name']}")
            print(f"User Email: {data['user']['email']}")
            print(f"Access Token: {data['tokens']['access_token'][:20]}...")
            return data['tokens']['access_token']
        else:
            print(f"❌ Registration failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_login():
    """Test user login"""
    print("\nTesting user login...")
    
    login_data = {
        "email": test_email,
        "password": "Test123!"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"User ID: {data['user']['id']}")
            print(f"User Name: {data['user']['name']}")
            print(f"User Email: {data['user']['email']}")
            print(f"Access Token: {data['tokens']['access_token'][:20]}...")
            return data['tokens']['access_token']
        else:
            print(f"❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_user_profile(access_token):
    """Test getting user profile"""
    print("\nTesting user profile retrieval...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )
        
        print(f"Profile Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Profile retrieval successful!")
            print(f"User ID: {data['id']}")
            print(f"User Name: {data['name']}")
            print(f"User Email: {data['email']}")
            print(f"User Bio: {data.get('bio', 'N/A')}")
            print(f"User Location: {data.get('location', 'N/A')}")
            return True
        else:
            print(f"❌ Profile retrieval failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Profile retrieval error: {e}")
        return False

def main():
    print("🧪 Frontend Integration Test")
    print("=" * 40)
    
    # Test registration
    access_token = test_registration()
    
    if access_token:
        # Test profile retrieval with registration token
        test_user_profile(access_token)
        
        # Wait a moment
        time.sleep(1)
        
        # Test login
        login_token = test_login()
        
        if login_token:
            # Test profile retrieval with login token
            test_user_profile(login_token)
            print("\n✅ All tests passed! Frontend should work correctly.")
        else:
            print("\n❌ Login test failed.")
    else:
        print("\n❌ Registration test failed.")

if __name__ == "__main__":
    main()