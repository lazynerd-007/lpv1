#!/usr/bin/env python3
"""
Debug script to test privacy endpoint directly
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def debug_router():
    """Debug the router directly"""
    print("🔍 Testing router import and endpoints...")
    
    try:
        from app.api.v1.users import router
        print(f"✅ Router imported successfully")
        print(f"📊 Router has {len(router.routes)} routes")
        
        print("\n📋 All routes in users router:")
        for i, route in enumerate(router.routes):
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                print(f"  {i+1}. {route.path} - {list(route.methods)}")
            else:
                print(f"  {i+1}. {route} - {type(route)}")
                
        # Check for privacy routes specifically
        privacy_routes = [route for route in router.routes 
                         if hasattr(route, 'path') and 'privacy' in route.path]
        print(f"\n🔒 Privacy routes found: {len(privacy_routes)}")
        for route in privacy_routes:
            print(f"  - {route.path} - {list(route.methods)}")
            
    except Exception as e:
        print(f"❌ Error importing router: {e}")
        import traceback
        traceback.print_exc()

def debug_endpoint():
    """Debug the privacy settings endpoint"""
    
    # First, login to get a token
    login_data = {
        "email": "user@test.com",
        "password": "testpassword123"
    }
    
    print("\n🔐 Logging in...")
    try:
        login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            print(login_response.text)
            return
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        print("✅ Login successful!")
        
        # Test the OpenAPI docs to see available endpoints
        print(f"\n📚 Checking all available user endpoints...")
        docs_response = requests.get(f"{BASE_URL}/openapi.json")
        if docs_response.status_code == 200:
            openapi_data = docs_response.json()
            paths = openapi_data.get("paths", {})
            user_paths = [path for path in paths.keys() if "users" in path]
            print(f"All user paths in OpenAPI:")
            for path in sorted(user_paths):
                methods = list(paths[path].keys())
                print(f"  {path} - {methods}")
            
            # Check for privacy specifically
            privacy_paths = [path for path in paths.keys() if "privacy" in path.lower()]
            print(f"\nPrivacy-related paths: {privacy_paths}")
            
        else:
            print(f"❌ Failed to get OpenAPI docs: {docs_response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

def test_running_server():
    """Test the currently running server"""
    import requests
    
    base_url = "http://localhost:8000"
    
    print("🌐 Testing currently running server...")
    
    try:
        # Test OpenAPI docs endpoint
        response = requests.get(f"{base_url}/openapi.json")
        if response.status_code == 200:
            data = response.json()
            paths = data.get("paths", {})
            user_paths = [path for path in paths.keys() if "users" in path]
            print(f"📚 Running server OpenAPI paths with 'users': {len(user_paths)}")
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
        print(f"❌ Error testing running server: {e}")

if __name__ == "__main__":
    print("🔍 Testing endpoint availability...")
    debug_endpoint()
    print("\n" + "="*50)
    debug_router()
    print("\n" + "="*50)
    
    # Test running server
    test_running_server()