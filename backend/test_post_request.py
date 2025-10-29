#!/usr/bin/env python3
"""
Test POST request to login endpoint
"""
import requests
import json

def test_login_post():
    """Test POST request to login endpoint"""
    url = "http://localhost:8000/api/v1/auth/login"
    
    # Test data
    test_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        print(f"Testing POST request to: {url}")
        print(f"Data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(url, json=test_data)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 405:
            print("\n❌ ERROR: Method Not Allowed - The endpoint doesn't accept POST requests")
            return False
        else:
            print(f"\n✅ SUCCESS: Endpoint accepts POST requests (Status: {response.status_code})")
            return True
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server. Make sure the server is running on localhost:8000")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    test_login_post()