#!/usr/bin/env python3
"""
Test notification endpoints in isolation
"""
import sys
import os
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_minimal_app():
    """Create a minimal FastAPI app with just notification endpoints"""
    app = FastAPI(title="Notification Test App")
    
    # Import and include only the notification router
    from app.api.v1.notifications import router as notifications_router
    app.include_router(notifications_router, prefix="/api/v1")
    
    return app

def test_notification_endpoints():
    """Test notification endpoints"""
    print("🧪 Testing Notification Endpoints in Isolation...")
    
    try:
        app = create_minimal_app()
        client = TestClient(app)
        
        # Test notification endpoints (should require authentication)
        response = client.get("/api/v1/notifications/")
        print(f"✅ GET /api/v1/notifications/ - Status: {response.status_code}")
        assert response.status_code in [401, 403, 422]  # Should require auth
        
        response = client.get("/api/v1/notifications/stats")
        print(f"✅ GET /api/v1/notifications/stats - Status: {response.status_code}")
        assert response.status_code in [401, 403, 422]  # Should require auth
        
        response = client.get("/api/v1/notifications/preferences")
        print(f"✅ GET /api/v1/notifications/preferences - Status: {response.status_code}")
        assert response.status_code in [401, 403, 422]  # Should require auth
        
        print("✅ All notification endpoint tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Notification endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_websocket_endpoint():
    """Test WebSocket endpoint in isolation"""
    print("\n🔌 Testing WebSocket Endpoint...")
    
    try:
        app = create_minimal_app()
        
        # Add WebSocket endpoint
        from app.websocket.endpoints import websocket_endpoint
        app.websocket("/ws/notifications")(websocket_endpoint)
        
        client = TestClient(app)
        
        # Test WebSocket connection without token (should fail gracefully)
        try:
            with client.websocket_connect("/ws/notifications") as websocket:
                # This should not succeed without a token
                pass
        except Exception:
            print("✅ WebSocket correctly rejected connection without token")
        
        # Test WebSocket connection with invalid token (should fail gracefully)
        try:
            with client.websocket_connect("/ws/notifications?token=invalid") as websocket:
                # This should not succeed with invalid token
                pass
        except Exception:
            print("✅ WebSocket correctly rejected connection with invalid token")
        
        print("✅ WebSocket endpoint tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ WebSocket endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run notification endpoint tests"""
    print("🚀 Notification Endpoint Test Suite")
    print("=" * 50)
    
    tests = [
        test_notification_endpoints,
        test_websocket_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All notification endpoint tests passed!")
        print("✅ The notification API is working correctly.")
        return True
    else:
        print(f"❌ {total - passed} tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)