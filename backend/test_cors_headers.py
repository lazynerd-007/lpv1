#!/usr/bin/env python3
"""
Test CORS headers from the server
"""
import requests

def test_cors_headers():
    """Test if CORS headers are being sent properly"""
    base_url = "http://localhost:8000"
    
    print("Testing CORS headers...")
    
    # Test OPTIONS request (preflight)
    print("\n1. Testing OPTIONS request (preflight):")
    try:
        response = requests.options(
            f"{base_url}/api/v1/auth/login",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type"
            }
        )
        print(f"Status Code: {response.status_code}")
        print("Response Headers:")
        for header, value in response.headers.items():
            if "access-control" in header.lower() or "cors" in header.lower():
                print(f"  {header}: {value}")
    except Exception as e:
        print(f"OPTIONS request failed: {e}")
    
    # Test simple GET request
    print("\n2. Testing GET request to root:")
    try:
        response = requests.get(
            f"{base_url}/",
            headers={"Origin": "http://localhost:5173"}
        )
        print(f"Status Code: {response.status_code}")
        print("CORS Headers:")
        for header, value in response.headers.items():
            if "access-control" in header.lower():
                print(f"  {header}: {value}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"GET request failed: {e}")
    
    # Test POST request with minimal data
    print("\n3. Testing POST request:")
    try:
        response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json={"email": "test@test.com", "password": "test"},
            headers={
                "Origin": "http://localhost:5173",
                "Content-Type": "application/json"
            }
        )
        print(f"Status Code: {response.status_code}")
        print("CORS Headers:")
        for header, value in response.headers.items():
            if "access-control" in header.lower():
                print(f"  {header}: {value}")
        
        if response.status_code != 200:
            print(f"Response Text: {response.text[:500]}")
    except Exception as e:
        print(f"POST request failed: {e}")

if __name__ == "__main__":
    test_cors_headers()