#!/usr/bin/env python3
"""Test script to check the correct paths with double prefix."""

import requests

def test_correct_paths():
    """Test the correct paths based on OpenAPI documentation."""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing correct endpoint paths...")
    
    endpoints_to_test = [
        "/api/v1/users/users/profile",
        "/api/v1/users/users/privacy-settings"
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"  {endpoint} - Status: {response.status_code}")
            if response.status_code != 404:
                print(f"    Response: {response.text[:100]}...")
        except Exception as e:
            print(f"  {endpoint} - Error: {e}")

if __name__ == "__main__":
    test_correct_paths()