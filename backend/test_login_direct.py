#!/usr/bin/env python3
"""
Test login endpoint directly
"""
import requests
import json

def test_login_direct():
    """Test login endpoint with exact credentials"""
    url = "http://localhost:8000/api/v1/auth/login"
    
    # Use the exact email from the logs
    login_data = {
        "email": "john.doe.test.1737998968@example.com",
        "password": "TestPassword123!"
    }
    
    print(f"Testing login with:")
    print(f"Email: {login_data['email']}")
    print(f"Password: {login_data['password']}")
    print(f"URL: {url}")
    
    try:
        response = requests.post(url, json=login_data)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            data = response.json()
            print(f"User: {data.get('user', {}).get('email')}")
            print(f"Access Token: {data.get('tokens', {}).get('access_token', 'N/A')[:50]}...")
        else:
            print("❌ Login failed!")
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Error text: {response.text}")
        
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_login_direct()
    if not success:
        print("\n❌ Login test failed")
    else:
        print("\n✅ Login test passed")