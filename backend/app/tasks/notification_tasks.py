"""
Notification background tasks for LemonNPie Backend API
"""
import asyncio
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging

from celery import current_task
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.celery_app import celery_app
from app.db.database import get_db
from app.models import Notification, NotificationPreference, User
from app.models.enums import NotificationType
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})
def send_notification_task(
    self,
    user_id: str,
    notification_type: str,
    title: str,
    message: str,
    data: Optional[Dict[str, Any]] = None
):
    """
    Background task to send a notification to a user
    """
    try:
        # Convert string back to UUID and enum
        user_uuid = UUID(user_id)
        notification_type_enum = NotificationType(notification_type)
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                _send_notification_async(
                    user_uuid, 
                    notification_type_enum, 
                    title, 
                    message, 
                    data
                )
            )
            return result
        finally:
            loop.close()
            
    except Exception as exc:
        logger.error(f"Failed to send notification: {exc}")
        # Retry the task
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(bind=True, retry_backoff=True, retry_kwargs={'max_retries': 3})
def send_bulk_notifications_task(
    self,
    user_ids: List[str],
    notification_type: str,
    title: str,
    message: str,
    data: Optional[Dict[str, Any]] = None
):
    """
    Background task to send notifications to multiple users
    """
    try:
        # Convert strings back to UUIDs and enum
        user_uuids = [UUID(user_id) for user_id in user_ids]
        notification_type_enum = NotificationType(notification_type)
        
        # Run async function in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                _send_bulk_notifications_async(
                    user_uuids, 
                    notification_type_enum, 
                    title, 
                    message, 
                    data
                )
            )
            return result
        finally:
            loop.close()
            
    except Exception as exc:
        logger.error(f"Failed to send bulk notifications: {exc}")
        # Retry the task
        raise self.retry(exc=exc, countdown=60)


@celery_app.task
def cleanup_old_notifications_task():
    """
    Background task to clean up old read notifications
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(_cleanup_old_notifications_async())
            return result
        finally:
            loop.close()
            
    except Exception as exc:
        logger.error(f"Failed to cleanup old notifications: {exc}")
        return {"error": str(exc)}


async def _send_notification_async(
    user_id: UUID,
    notification_type: NotificationType,
    title: str,
    message: str,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Async helper to send a single notification
    """
    async for session in get_db():
        try:
            notification_service = NotificationService(session)
            
            notification = await notification_service.create_notification(
                user_id=user_id,
                notification_type=notification_type,
                title=title,
                message=message,
                data=data
            )
            
            return {
                "success": True,
                "notification_id": str(notification.id),
                "user_id": str(user_id)
            }
            
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            raise
        finally:
            await session.close()


async def _send_bulk_notifications_async(
    user_ids: List[UUID],
    notification_type: NotificationType,
    title: str,
    message: str,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Async helper to send notifications to multiple users
    """
    async for session in get_db():
        try:
            notification_service = NotificationService(session)
            
            notifications = await notification_service.create_bulk_notifications(
                user_ids=user_ids,
                notification_type=notification_type,
                title=title,
                message=message,
                data=data
            )
            
            return {
                "success": True,
                "notifications_created": len(notifications),
                "user_count": len(user_ids)
            }
            
        except Exception as e:
            logger.error(f"Error creating bulk notifications: {e}")
            raise
        finally:
            await session.close()


async def _cleanup_old_notifications_async() -> Dict[str, Any]:
    """
    Async helper to cleanup old notifications
    """
    async for session in get_db():
        try:
            notification_service = NotificationService(session)
            
            deleted_count = await notification_service.cleanup_old_notifications()
            
            return {
                "success": True,
                "deleted_count": deleted_count
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up notifications: {e}")
            raise
        finally:
            await session.close()