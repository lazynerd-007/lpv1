#!/usr/bin/env python3
"""
Test the server running on port 8001
"""
import requests

def test_server_8001():
    """Test the server on port 8001"""
    base_url = "http://localhost:8001"
    
    print("🌐 Testing server on port 8001...")
    
    try:
        # Test OpenAPI docs endpoint
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            data = response.json()
            paths = data.get("paths", {})
            user_paths = [path for path in paths.keys() if "users" in path]
            print(f"📚 Port 8001 OpenAPI paths with 'users': {len(user_paths)}")
            for path in sorted(user_paths):
                methods = list(paths[path].keys())
                print(f"  {path} - {methods}")
            
            # Check specifically for privacy settings
            privacy_paths = [path for path in paths.keys() if "privacy" in path]
            print(f"\n🔒 Privacy-related paths: {len(privacy_paths)}")
            for path in privacy_paths:
                methods = list(paths[path].keys())
                print(f"  {path} - {methods}")
        else:
            print(f"❌ Failed to get OpenAPI schema: {response.status_code}")
            
        # Test direct endpoint access
        print(f"\n🔍 Testing direct endpoint access...")
        test_endpoints = [
            "/api/v1/users/profile",
            "/api/v1/users/privacy-settings"
        ]
        
        for endpoint in test_endpoints:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"  {endpoint} - Status: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Error testing server: {e}")

if __name__ == "__main__":
    test_server_8001()