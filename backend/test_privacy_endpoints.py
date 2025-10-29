#!/usr/bin/env python3
"""
Test script for privacy settings endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_privacy_endpoints():
    """Test the privacy settings endpoints"""
    
    # First, login to get a token
    login_data = {
        "email": "user@test.com",
        "password": "testpassword123"
    }
    
    print("🔐 Logging in...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("✅ Login successful!")
    
    # Test getting privacy settings
    print("\n📋 Testing GET privacy settings...")
    privacy_response = requests.get(f"{BASE_URL}/users/privacy-settings", headers=headers)
    
    if privacy_response.status_code == 200:
        print("✅ GET privacy settings successful!")
        print(f"Current settings: {json.dumps(privacy_response.json(), indent=2)}")
    else:
        print(f"❌ GET privacy settings failed: {privacy_response.status_code}")
        print(privacy_response.text)
        return
    
    # Test updating privacy settings
    print("\n🔧 Testing PUT privacy settings...")
    update_data = {
        "profile_visibility": "friends",
        "watchlist_visibility": "private",
        "analytics_tracking": False,
        "personalized_recommendations": True
    }
    
    update_response = requests.put(f"{BASE_URL}/users/privacy-settings", json=update_data, headers=headers)
    
    if update_response.status_code == 200:
        print("✅ PUT privacy settings successful!")
        print(f"Updated settings: {json.dumps(update_response.json(), indent=2)}")
    else:
        print(f"❌ PUT privacy settings failed: {update_response.status_code}")
        print(update_response.text)
    
    # Test 2FA status
    print("\n🔒 Testing 2FA status...")
    twofa_response = requests.get(f"{BASE_URL}/users/2fa/status", headers=headers)
    
    if twofa_response.status_code == 200:
        print("✅ GET 2FA status successful!")
        print(f"2FA status: {json.dumps(twofa_response.json(), indent=2)}")
    else:
        print(f"❌ GET 2FA status failed: {twofa_response.status_code}")
        print(twofa_response.text)
    
    # Test password change (with wrong current password to avoid actually changing it)
    print("\n🔑 Testing password change (with wrong current password)...")
    password_data = {
        "current_password": "wrongpassword",
        "new_password": "newpassword123"
    }
    
    password_response = requests.post(f"{BASE_URL}/users/change-password", json=password_data, headers=headers)
    
    if password_response.status_code == 400:
        print("✅ Password change correctly rejected wrong current password!")
        print(f"Response: {json.dumps(password_response.json(), indent=2)}")
    else:
        print(f"❌ Password change unexpected response: {password_response.status_code}")
        print(password_response.text)

if __name__ == "__main__":
    test_privacy_endpoints()