"""
Notification API endpoints for LemonNPie Backend API
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.auth.dependencies import get_current_user, require_role
from app.models import User
from app.models.enums import UserRole, NotificationType
from app.services.notification_service import NotificationService
from app.schemas.notification import (
    NotificationResponse,
    NotificationListResponse,
    NotificationStats,
    NotificationPreferenceResponse,
    NotificationPreferenceUpdate,
    NotificationBulkCreate
)
from app.core.exceptions import NotFoundError, ValidationError

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/", response_model=NotificationListResponse)
async def get_notifications(
    unread_only: bool = Query(False, description="Get only unread notifications"),
    limit: int = Query(50, ge=1, le=100, description="Number of notifications to return"),
    offset: int = Query(0, ge=0, description="Number of notifications to skip"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get notifications for the current user
    """
    notification_service = NotificationService(db)
    
    notifications = await notification_service.get_user_notifications(
        user_id=current_user.id,
        unread_only=unread_only,
        limit=limit,
        offset=offset
    )
    
    unread_count = await notification_service.get_unread_count(current_user.id)
    
    return NotificationListResponse(
        notifications=[NotificationResponse.from_orm(n) for n in notifications],
        total=len(notifications),
        unread_count=unread_count,
        has_more=len(notifications) == limit
    )


@router.get("/stats", response_model=NotificationStats)
async def get_notification_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get notification statistics for the current user
    """
    notification_service = NotificationService(db)
    
    unread_count = await notification_service.get_unread_count(current_user.id)
    
    # Get total notifications (we'll implement this if needed)
    all_notifications = await notification_service.get_user_notifications(
        user_id=current_user.id,
        unread_only=False,
        limit=1000  # Large limit to get all
    )
    
    total_notifications = len(all_notifications)
    read_count = total_notifications - unread_count
    
    return NotificationStats(
        total_notifications=total_notifications,
        unread_count=unread_count,
        read_count=read_count
    )


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark a notification as read
    """
    notification_service = NotificationService(db)
    
    try:
        notification = await notification_service.mark_notification_read(
            notification_id=notification_id,
            user_id=current_user.id
        )
        return NotificationResponse.from_orm(notification)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Notification not found")


@router.patch("/read-all")
async def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Mark all notifications as read for the current user
    """
    notification_service = NotificationService(db)
    
    count = await notification_service.mark_all_notifications_read(current_user.id)
    
    return {"message": f"Marked {count} notifications as read"}


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a notification
    """
    notification_service = NotificationService(db)
    
    success = await notification_service.delete_notification(
        notification_id=notification_id,
        user_id=current_user.id
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"message": "Notification deleted successfully"}


@router.get("/preferences", response_model=List[NotificationPreferenceResponse])
async def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get notification preferences for the current user
    """
    notification_service = NotificationService(db)
    
    preferences = await notification_service.get_notification_preferences(current_user.id)
    
    return [NotificationPreferenceResponse.from_orm(pref) for pref in preferences]


@router.patch("/preferences/{notification_type}", response_model=NotificationPreferenceResponse)
async def update_notification_preference(
    notification_type: NotificationType,
    preference_update: NotificationPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update notification preference for a specific notification type
    """
    notification_service = NotificationService(db)
    
    preference = await notification_service.update_notification_preference(
        user_id=current_user.id,
        notification_type=notification_type,
        email_enabled=preference_update.email_enabled,
        push_enabled=preference_update.push_enabled,
        in_app_enabled=preference_update.in_app_enabled
    )
    
    return NotificationPreferenceResponse.from_orm(preference)


# Admin endpoints
@router.post("/bulk", response_model=dict)
async def send_bulk_notifications(
    bulk_notification: NotificationBulkCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Send bulk notifications to multiple users (Admin only)
    """
    from app.tasks.notification_tasks import send_bulk_notifications_task
    
    # Convert UUIDs to strings for Celery
    user_id_strings = [str(user_id) for user_id in bulk_notification.user_ids]
    
    # Queue the task
    task = send_bulk_notifications_task.delay(
        user_ids=user_id_strings,
        notification_type=bulk_notification.type.value,
        title=bulk_notification.title,
        message=bulk_notification.message,
        data=bulk_notification.data
    )
    
    return {
        "message": "Bulk notification task queued",
        "task_id": task.id,
        "user_count": len(bulk_notification.user_ids)
    }


@router.post("/cleanup")
async def cleanup_old_notifications(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Cleanup old notifications (Admin only)
    """
    from app.tasks.notification_tasks import cleanup_old_notifications_task
    
    # Queue the cleanup task
    task = cleanup_old_notifications_task.delay()
    
    return {
        "message": "Cleanup task queued",
        "task_id": task.id
    }


@router.get("/websocket/stats")
async def get_websocket_stats(
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """
    Get WebSocket connection statistics (Admin only)
    """
    from app.services.notification_broadcaster import NotificationBroadcaster
    
    stats = NotificationBroadcaster.get_connection_stats()
    connected_users = NotificationBroadcaster.get_connected_users()
    
    return {
        "stats": stats,
        "connected_user_ids": [str(user_id) for user_id in connected_users]
    }


@router.post("/websocket/broadcast")
async def broadcast_system_announcement(
    title: str,
    message: str,
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """
    Broadcast a system announcement to all connected users (Admin only)
    """
    from app.services.notification_broadcaster import NotificationBroadcaster
    
    await NotificationBroadcaster.broadcast_system_announcement(
        title=title,
        message=message,
        data={"sender": current_user.name}
    )
    
    return {
        "message": "System announcement broadcasted",
        "title": title,
        "recipients": len(NotificationBroadcaster.get_connected_users())
    }