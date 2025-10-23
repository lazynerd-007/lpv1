#!/usr/bin/env python3
"""
Simple test for notification system components
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all notification system imports"""
    print("🧪 Testing Notification System Imports...")
    
    # Test enums
    try:
        from app.models.enums import NotificationType
        print(f"✅ NotificationType enum: {[t.value for t in NotificationType]}")
    except Exception as e:
        print(f"❌ NotificationType enum failed: {e}")
        return False
    
    # Test models
    try:
        from app.models.moderation import Notification, NotificationPreference
        print("✅ Notification models imported successfully")
    except Exception as e:
        print(f"❌ Notification models failed: {e}")
        return False
    
    # Test schemas
    try:
        from app.schemas.notification import (
            NotificationResponse, 
            NotificationCreate,
            NotificationPreferenceResponse
        )
        print("✅ Notification schemas imported successfully")
    except Exception as e:
        print(f"❌ Notification schemas failed: {e}")
        return False
    
    # Test services
    try:
        from app.services.notification_service import NotificationService
        from app.services.notification_trigger import NotificationTrigger
        from app.services.notification_broadcaster import NotificationBroadcaster
        print("✅ Notification services imported successfully")
    except Exception as e:
        print(f"❌ Notification services failed: {e}")
        return False
    
    # Test Celery tasks
    try:
        from app.tasks.notification_tasks import (
            send_notification_task,
            send_bulk_notifications_task,
            cleanup_old_notifications_task
        )
        print("✅ Celery notification tasks imported successfully")
    except Exception as e:
        print(f"❌ Celery notification tasks failed: {e}")
        return False
    
    # Test WebSocket components
    try:
        from app.websocket.manager import ConnectionManager, connection_manager
        from app.websocket.endpoints import websocket_endpoint
        print("✅ WebSocket components imported successfully")
    except Exception as e:
        print(f"❌ WebSocket components failed: {e}")
        return False
    
    # Test API router
    try:
        from app.api.v1.notifications import router
        print("✅ Notification API router imported successfully")
    except Exception as e:
        print(f"❌ Notification API router failed: {e}")
        return False
    
    return True


def test_schema_validation():
    """Test schema validation"""
    print("\n📝 Testing Schema Validation...")
    
    try:
        from app.schemas.notification import NotificationCreate, NotificationResponse
        from app.models.enums import NotificationType
        from uuid import uuid4
        from datetime import datetime
        
        # Test NotificationCreate
        create_data = {
            "user_id": uuid4(),
            "type": NotificationType.SYSTEM_ANNOUNCEMENT,
            "title": "Test Notification",
            "message": "This is a test notification"
        }
        
        notification_create = NotificationCreate(**create_data)
        print(f"✅ NotificationCreate validation: {notification_create.title}")
        
        # Test NotificationResponse
        response_data = {
            "id": uuid4(),
            "user_id": uuid4(),
            "type": NotificationType.NEW_FOLLOWER,
            "title": "New Follower",
            "message": "Someone started following you",
            "is_read": False,
            "created_at": datetime.utcnow()
        }
        
        notification_response = NotificationResponse(**response_data)
        print(f"✅ NotificationResponse validation: {notification_response.title}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation failed: {e}")
        return False


def test_service_methods():
    """Test service method signatures"""
    print("\n🔧 Testing Service Methods...")
    
    try:
        from app.services.notification_service import NotificationService
        from app.services.notification_trigger import NotificationTrigger
        from app.services.notification_broadcaster import NotificationBroadcaster
        
        # Test NotificationService methods
        service_methods = [
            'create_notification',
            'get_user_notifications',
            'mark_notification_read',
            'get_unread_count',
            'create_bulk_notifications',
            'cleanup_old_notifications'
        ]
        
        for method in service_methods:
            if hasattr(NotificationService, method):
                print(f"✅ NotificationService.{method}")
            else:
                print(f"❌ NotificationService.{method} missing")
                return False
        
        # Test NotificationTrigger methods
        trigger_methods = [
            'send_review_vote_notification',
            'send_new_follower_notification',
            'send_movie_added_notification',
            'send_system_announcement'
        ]
        
        for method in trigger_methods:
            if hasattr(NotificationTrigger, method):
                print(f"✅ NotificationTrigger.{method}")
            else:
                print(f"❌ NotificationTrigger.{method} missing")
                return False
        
        # Test NotificationBroadcaster methods
        broadcaster_methods = [
            'broadcast_to_user',
            'broadcast_to_users',
            'broadcast_system_announcement',
            'get_connected_users'
        ]
        
        for method in broadcaster_methods:
            if hasattr(NotificationBroadcaster, method):
                print(f"✅ NotificationBroadcaster.{method}")
            else:
                print(f"❌ NotificationBroadcaster.{method} missing")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Service method test failed: {e}")
        return False


def test_websocket_manager():
    """Test WebSocket manager functionality"""
    print("\n🌐 Testing WebSocket Manager...")
    
    try:
        from app.websocket.manager import ConnectionManager, connection_manager
        
        # Test ConnectionManager methods
        manager_methods = [
            'connect',
            'disconnect',
            'send_personal_message',
            'send_notification',
            'send_bulk_notifications',
            'get_connected_users',
            'get_connection_count',
            'is_user_connected'
        ]
        
        for method in manager_methods:
            if hasattr(ConnectionManager, method):
                print(f"✅ ConnectionManager.{method}")
            else:
                print(f"❌ ConnectionManager.{method} missing")
                return False
        
        # Test global instance
        print(f"✅ Global connection_manager: {type(connection_manager).__name__}")
        
        # Test initial state
        connected_users = connection_manager.get_connected_users()
        connection_count = connection_manager.get_connection_count()
        print(f"✅ Initial state - Users: {len(connected_users)}, Connections: {connection_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ WebSocket manager test failed: {e}")
        return False


def test_celery_configuration():
    """Test Celery configuration"""
    print("\n⚙️  Testing Celery Configuration...")
    
    try:
        from app.core.celery_app import celery_app
        
        print(f"✅ Celery app name: {celery_app.main}")
        print(f"✅ Celery broker: {celery_app.conf.broker_url}")
        print(f"✅ Celery backend: {celery_app.conf.result_backend}")
        
        # Test task registration
        registered_tasks = list(celery_app.tasks.keys())
        notification_tasks = [task for task in registered_tasks if 'notification' in task]
        
        if notification_tasks:
            print(f"✅ Registered notification tasks: {notification_tasks}")
        else:
            print("⚠️  No notification tasks found in registry")
        
        return True
        
    except Exception as e:
        print(f"❌ Celery configuration test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 LemonNPie Notification System Test Suite")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_schema_validation,
        test_service_methods,
        test_websocket_manager,
        test_celery_configuration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            print(f"❌ {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All notification system tests passed!")
        print("✅ The notification system is properly configured and ready to use.")
        print("\n📋 Next steps:")
        print("1. Run database migration: alembic upgrade head")
        print("2. Start Redis server for Celery")
        print("3. Start Celery worker: python celery_worker.py worker")
        print("4. Start FastAPI server: python run.py")
        print("5. Test WebSocket connection with a valid JWT token")
        return True
    else:
        print(f"❌ {total - passed} tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)