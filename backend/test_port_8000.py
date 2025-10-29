#!/usr/bin/env python3
"""Test script to check the main server on port 8000."""

import requests
import json

def test_server_8000():
    """Test the server running on port 8000."""
    base_url = "http://localhost:8000"
    
    print("🌐 Testing server on port 8000...")
    
    try:
        # Test OpenAPI documentation
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            openapi_data = response.json()
            paths = openapi_data.get("paths", {})
            
            # Count user-related paths
            user_paths = [path for path in paths.keys() if "users" in path]
            print(f"📚 Port 8000 OpenAPI paths with 'users': {len(user_paths)}")
            for path in sorted(user_paths):
                methods = list(paths[path].keys())
                print(f"  {path} - {methods}")
            
            # Check for privacy-related paths
            privacy_paths = [path for path in paths.keys() if "privacy" in path]
            print(f"\n🔒 Privacy-related paths: {len(privacy_paths)}")
            for path in sorted(privacy_paths):
                methods = list(paths[path].keys())
                print(f"  {path} - {methods}")
        else:
            print(f"❌ Failed to get OpenAPI documentation: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Error getting OpenAPI documentation: {e}")
    
    # Test direct endpoint access
    print(f"\n🔍 Testing direct endpoint access...")
    
    endpoints_to_test = [
        "/api/v1/users/profile",
        "/api/v1/users/privacy-settings"
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"  {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"  {endpoint} - Error: {e}")

if __name__ == "__main__":
    test_server_8000()