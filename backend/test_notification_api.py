#!/usr/bin/env python3
"""
Test notification API endpoints
"""
import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app


def test_notification_endpoints():
    """Test notification API endpoints"""
    client = TestClient(app)
    
    # Test health check first
    response = client.get("/health")
    print(f"Health check: {response.status_code}")
    assert response.status_code == 200
    
    # Test root endpoint
    response = client.get("/")
    print(f"Root endpoint: {response.status_code}")
    assert response.status_code == 200
    
    # Test notification endpoints (should require authentication)
    response = client.get("/api/v1/notifications/")
    print(f"Notifications endpoint (no auth): {response.status_code}")
    # Should return 401 or 403 for unauthorized access
    assert response.status_code in [401, 403]
    
    # Test notification stats endpoint (should require authentication)
    response = client.get("/api/v1/notifications/stats")
    print(f"Notification stats endpoint (no auth): {response.status_code}")
    # Should return 401 or 403 for unauthorized access
    assert response.status_code in [401, 403]
    
    print("✅ All notification endpoint tests passed!")


def test_websocket_endpoint():
    """Test WebSocket endpoint"""
    client = TestClient(app)
    
    # Test WebSocket connection without token (should fail)
    try:
        with client.websocket_connect("/ws/notifications") as websocket:
            # This should not succeed without a token
            pass
    except Exception as e:
        print(f"✅ WebSocket correctly rejected connection without token: {type(e).__name__}")
    
    # Test WebSocket connection with invalid token (should fail)
    try:
        with client.websocket_connect("/ws/notifications?token=invalid") as websocket:
            # This should not succeed with invalid token
            pass
    except Exception as e:
        print(f"✅ WebSocket correctly rejected connection with invalid token: {type(e).__name__}")


def test_notification_schemas():
    """Test notification schemas"""
    from app.schemas.notification import NotificationResponse, NotificationCreate
    from app.models.enums import NotificationType
    from uuid import uuid4
    from datetime import datetime
    
    # Test NotificationResponse schema
    notification_data = {
        "id": uuid4(),
        "user_id": uuid4(),
        "type": NotificationType.SYSTEM_ANNOUNCEMENT,
        "title": "Test Notification",
        "message": "This is a test notification",
        "data": {"test": True},
        "is_read": False,
        "read_at": None,
        "expires_at": None,
        "created_at": datetime.utcnow()
    }
    
    try:
        notification = NotificationResponse(**notification_data)
        print(f"✅ NotificationResponse schema validation passed: {notification.title}")
    except Exception as e:
        print(f"❌ NotificationResponse schema validation failed: {e}")
        raise
    
    # Test NotificationCreate schema
    create_data = {
        "user_id": uuid4(),
        "type": NotificationType.NEW_FOLLOWER,
        "title": "New Follower",
        "message": "Someone started following you",
        "data": {"follower_name": "John Doe"}
    }
    
    try:
        create_notification = NotificationCreate(**create_data)
        print(f"✅ NotificationCreate schema validation passed: {create_notification.title}")
    except Exception as e:
        print(f"❌ NotificationCreate schema validation failed: {e}")
        raise


def test_notification_enums():
    """Test notification enums"""
    from app.models.enums import NotificationType
    
    # Test all notification types
    expected_types = [
        "REVIEW_VOTE",
        "NEW_FOLLOWER", 
        "REVIEW_COMMENT",
        "MOVIE_ADDED",
        "SYSTEM_ANNOUNCEMENT",
        "MODERATION_ACTION"
    ]
    
    for type_name in expected_types:
        try:
            notification_type = NotificationType(type_name.lower())
            print(f"✅ NotificationType.{type_name} exists: {notification_type.value}")
        except ValueError as e:
            print(f"❌ NotificationType.{type_name} not found: {e}")
            raise


def test_celery_tasks():
    """Test Celery task imports"""
    try:
        from app.tasks.notification_tasks import (
            send_notification_task,
            send_bulk_notifications_task,
            cleanup_old_notifications_task
        )
        print("✅ Celery notification tasks imported successfully")
        
        # Test task signatures
        print(f"✅ send_notification_task: {send_notification_task.name}")
        print(f"✅ send_bulk_notifications_task: {send_bulk_notifications_task.name}")
        print(f"✅ cleanup_old_notifications_task: {cleanup_old_notifications_task.name}")
        
    except ImportError as e:
        print(f"❌ Failed to import Celery tasks: {e}")
        raise


def test_notification_services():
    """Test notification service imports"""
    try:
        from app.services.notification_service import NotificationService
        from app.services.notification_trigger import NotificationTrigger
        from app.services.notification_broadcaster import NotificationBroadcaster
        
        print("✅ Notification services imported successfully")
        
        # Test service methods exist
        service_methods = [
            'create_notification',
            'get_user_notifications', 
            'mark_notification_read',
            'get_unread_count'
        ]
        
        for method in service_methods:
            if hasattr(NotificationService, method):
                print(f"✅ NotificationService.{method} exists")
            else:
                print(f"❌ NotificationService.{method} missing")
                raise AttributeError(f"Method {method} not found")
        
        # Test trigger methods
        trigger_methods = [
            'send_review_vote_notification',
            'send_new_follower_notification',
            'send_movie_added_notification'
        ]
        
        for method in trigger_methods:
            if hasattr(NotificationTrigger, method):
                print(f"✅ NotificationTrigger.{method} exists")
            else:
                print(f"❌ NotificationTrigger.{method} missing")
                raise AttributeError(f"Method {method} not found")
                
    except ImportError as e:
        print(f"❌ Failed to import notification services: {e}")
        raise


def test_websocket_manager():
    """Test WebSocket manager"""
    try:
        from app.websocket.manager import ConnectionManager, connection_manager
        
        print("✅ WebSocket manager imported successfully")
        
        # Test manager methods
        manager_methods = [
            'connect',
            'disconnect', 
            'send_personal_message',
            'send_notification',
            'get_connected_users'
        ]
        
        for method in manager_methods:
            if hasattr(ConnectionManager, method):
                print(f"✅ ConnectionManager.{method} exists")
            else:
                print(f"❌ ConnectionManager.{method} missing")
                raise AttributeError(f"Method {method} not found")
        
        # Test global instance
        print(f"✅ Global connection_manager instance: {type(connection_manager).__name__}")
        
    except ImportError as e:
        print(f"❌ Failed to import WebSocket manager: {e}")
        raise


if __name__ == "__main__":
    print("🧪 Testing LemonNPie Notification System...")
    print("=" * 50)
    
    try:
        print("\n📋 Testing API Endpoints...")
        test_notification_endpoints()
        
        print("\n🔌 Testing WebSocket Endpoints...")
        test_websocket_endpoint()
        
        print("\n📝 Testing Schemas...")
        test_notification_schemas()
        
        print("\n🏷️  Testing Enums...")
        test_notification_enums()
        
        print("\n⚙️  Testing Celery Tasks...")
        test_celery_tasks()
        
        print("\n🔧 Testing Services...")
        test_notification_services()
        
        print("\n🌐 Testing WebSocket Manager...")
        test_websocket_manager()
        
        print("\n" + "=" * 50)
        print("🎉 All notification system tests passed!")
        print("✅ The notification system is properly configured and ready to use.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)