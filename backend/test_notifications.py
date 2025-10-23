#!/usr/bin/env python3
"""
Simple test script for notification system
"""
import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import get_db
from app.services.notification_service import NotificationService
from app.models.enums import NotificationType
from app.models import User
from sqlalchemy import select
import uuid


async def test_notification_system():
    """Test the notification system"""
    print("Testing notification system...")
    
    # Initialize database
    from app.db.database import init_db
    await init_db()
    
    async for session in get_db():
        try:
            notification_service = NotificationService(session)
            
            # Get the first user (if any exists)
            result = await session.execute(select(User).limit(1))
            user = result.scalar_one_or_none()
            
            if not user:
                print("No users found in database. Creating a test user...")
                # Create a test user
                from app.auth.security import get_password_hash
                
                test_user = User(
                    email="test@example.com",
                    password_hash=get_password_hash("testpassword"),
                    name="Test User"
                )
                session.add(test_user)
                await session.commit()
                await session.refresh(test_user)
                user = test_user
                print(f"Created test user: {user.email}")
            
            print(f"Using user: {user.email} (ID: {user.id})")
            
            # Test creating a notification
            notification = await notification_service.create_notification(
                user_id=user.id,
                notification_type=NotificationType.SYSTEM_ANNOUNCEMENT,
                title="Test Notification",
                message="This is a test notification from the notification system",
                data={"test": True}
            )
            
            if notification:
                print(f"✅ Created notification: {notification.id}")
                
                # Test getting notifications
                notifications = await notification_service.get_user_notifications(
                    user_id=user.id,
                    limit=10
                )
                print(f"✅ Retrieved {len(notifications)} notifications")
                
                # Test unread count
                unread_count = await notification_service.get_unread_count(user.id)
                print(f"✅ Unread count: {unread_count}")
                
                # Test marking as read
                read_notification = await notification_service.mark_notification_read(
                    notification_id=notification.id,
                    user_id=user.id
                )
                print(f"✅ Marked notification as read: {read_notification.is_read}")
                
                # Test notification preferences
                preference = await notification_service.update_notification_preference(
                    user_id=user.id,
                    notification_type=NotificationType.SYSTEM_ANNOUNCEMENT,
                    email_enabled=True,
                    push_enabled=False,
                    in_app_enabled=True
                )
                print(f"✅ Created/updated notification preference: {preference.id}")
                
                print("🎉 All notification system tests passed!")
            else:
                print("❌ Failed to create notification")
                
        except Exception as e:
            print(f"❌ Error testing notification system: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await session.close()


if __name__ == "__main__":
    asyncio.run(test_notification_system())