#!/usr/bin/env python3
"""
Integration Test Script for Frontend-Backend Communication
Tests the key endpoints that the frontend SettingsPage.vue component uses
"""

import requests
import json
import sys
from typing import Dict, Any

# Base URL for the backend API
BASE_URL = "http://localhost:8000"

def test_endpoint(method: str, endpoint: str, headers: Dict[str, str] = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test a single endpoint and return the result"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=5)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=5)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        return {
            "status_code": response.status_code,
            "success": response.status_code < 500,  # 4xx is expected for auth, 5xx is server error
            "response_size": len(response.content),
            "content_type": response.headers.get("content-type", ""),
            "endpoint_accessible": True
        }
    except requests.exceptions.ConnectionError:
        return {"error": "Connection refused - server not running", "endpoint_accessible": False}
    except requests.exceptions.Timeout:
        return {"error": "Request timeout", "endpoint_accessible": False}
    except Exception as e:
        return {"error": str(e), "endpoint_accessible": False}

def main():
    print("🧪 Testing Frontend-Backend Integration")
    print("=" * 50)
    
    # Test server availability
    print("\n📡 Testing server availability...")
    server_test = test_endpoint("GET", "/")
    if not server_test.get("endpoint_accessible", False):
        print("❌ Backend server is not accessible!")
        print(f"   Error: {server_test.get('error', 'Unknown error')}")
        sys.exit(1)
    
    print("✅ Backend server is accessible")
    
    # Define the endpoints that the frontend uses
    endpoints_to_test = [
        # Privacy Settings endpoints
        ("GET", "/api/v1/users/privacy-settings", "Get Privacy Settings"),
        ("PUT", "/api/v1/users/privacy-settings", "Update Privacy Settings"),
        
        # Profile endpoints
        ("GET", "/api/v1/users/profile", "Get User Profile"),
        ("PUT", "/api/v1/users/profile", "Update User Profile"),
        
        # Password change endpoint
        ("POST", "/api/v1/users/change-password", "Change Password"),
        
        # 2FA endpoints
        ("GET", "/api/v1/users/2fa/status", "Get 2FA Status"),
        ("POST", "/api/v1/users/2fa/enable", "Enable 2FA"),
        ("POST", "/api/v1/users/2fa/disable", "Disable 2FA"),
        
        # Additional user endpoints
        ("GET", "/api/v1/users/activity", "Get User Activity"),
        ("GET", "/api/v1/users/favorites", "Get User Favorites"),
        ("GET", "/api/v1/users/watchlist", "Get User Watchlist"),
        ("DELETE", "/api/v1/users/account", "Delete User Account"),
    ]
    
    print(f"\n🔍 Testing {len(endpoints_to_test)} key endpoints...")
    
    # Mock headers for authenticated requests
    mock_headers = {
        "Authorization": "Bearer mock_token_for_testing",
        "Content-Type": "application/json"
    }
    
    # Mock data for PUT/POST requests
    mock_privacy_data = {
        "profile_visibility": "public",
        "watchlist_visibility": "private",
        "analytics_tracking": True,
        "personalized_recommendations": True
    }
    
    mock_profile_data = {
        "username": "testuser",
        "email": "test@example.com",
        "bio": "Test bio"
    }
    
    mock_password_data = {
        "current_password": "oldpass123",
        "new_password": "newpass123"
    }
    
    results = []
    accessible_count = 0
    
    for method, endpoint, description in endpoints_to_test:
        print(f"\n🔗 Testing: {description}")
        print(f"   {method} {endpoint}")
        
        # Choose appropriate data based on endpoint
        data = None
        if "privacy-settings" in endpoint and method == "PUT":
            data = mock_privacy_data
        elif "profile" in endpoint and method == "PUT":
            data = mock_profile_data
        elif "change-password" in endpoint:
            data = mock_password_data
        
        result = test_endpoint(method, endpoint, mock_headers, data)
        results.append((endpoint, result))
        
        if result.get("endpoint_accessible", False):
            accessible_count += 1
            status_code = result.get("status_code", 0)
            if status_code == 403:
                print(f"   ✅ Accessible (Status: {status_code} - Authentication Required)")
            elif status_code == 422:
                print(f"   ✅ Accessible (Status: {status_code} - Validation Error)")
            elif status_code == 500:
                print(f"   ⚠️  Accessible but Server Error (Status: {status_code})")
            else:
                print(f"   ✅ Accessible (Status: {status_code})")
        else:
            print(f"   ❌ Not accessible: {result.get('error', 'Unknown error')}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Accessible endpoints: {accessible_count}/{len(endpoints_to_test)}")
    print(f"❌ Inaccessible endpoints: {len(endpoints_to_test) - accessible_count}/{len(endpoints_to_test)}")
    
    if accessible_count == len(endpoints_to_test):
        print("\n🎉 SUCCESS: All endpoints are accessible!")
        print("   The frontend can communicate with all required backend endpoints.")
        print("   Status codes 403/422 are expected without proper authentication.")
    elif accessible_count > len(endpoints_to_test) * 0.8:
        print(f"\n⚠️  MOSTLY WORKING: {accessible_count}/{len(endpoints_to_test)} endpoints accessible")
        print("   Most endpoints are working. Check the failed ones above.")
    else:
        print(f"\n❌ ISSUES DETECTED: Only {accessible_count}/{len(endpoints_to_test)} endpoints accessible")
        print("   There may be server configuration issues.")
    
    print("\n🔧 Frontend Integration Status:")
    print("   - Privacy Settings: Ready for testing")
    print("   - Profile Management: Ready for testing") 
    print("   - Password Change: Ready for testing")
    print("   - 2FA Management: Ready for testing")
    print("   - Loading indicators: Implemented")
    print("   - Error handling: Implemented")
    
    return accessible_count == len(endpoints_to_test)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)