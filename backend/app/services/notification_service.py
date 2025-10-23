"""
Notification service for LemonNPie Backend API
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, or_, func
from sqlalchemy.orm import selectinload

from app.models import Notification, NotificationPreference, User
from app.models.enums import NotificationType
from app.core.exceptions import NotFoundError, ValidationError

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_notification(
        self,
        user_id: UUID,
        notification_type: NotificationType,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        expires_at: Optional[datetime] = None
    ) -> Notification:
        """
        Create a new notification for a user
        """
        # Check if user exists
        user_result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()
        if not user:
            raise NotFoundError(f"User with id {user_id} not found")

        # Check user's notification preferences
        if not await self._should_send_notification(user_id, notification_type):
            logger.info(f"Notification {notification_type} disabled for user {user_id}")
            return None

        # Create notification
        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
            data=data or {},
            expires_at=expires_at
        )

        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)

        # Send real-time notification if user is connected
        try:
            from app.websocket.manager import connection_manager
            await connection_manager.send_notification(
                user_id=user_id,
                notification_type=notification_type,
                title=title,
                message=message,
                data=data,
                notification_id=notification.id
            )
        except Exception as e:
            logger.warning(f"Failed to send real-time notification: {e}")

        logger.info(f"Created notification {notification.id} for user {user_id}")
        return notification

    async def create_bulk_notifications(
        self,
        user_ids: List[UUID],
        notification_type: NotificationType,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        expires_at: Optional[datetime] = None
    ) -> List[Notification]:
        """
        Create notifications for multiple users
        """
        notifications = []
        
        # Get users who should receive this notification type
        eligible_users = await self._get_eligible_users(user_ids, notification_type)
        
        for user_id in eligible_users:
            notification = Notification(
                user_id=user_id,
                type=notification_type,
                title=title,
                message=message,
                data=data or {},
                expires_at=expires_at
            )
            notifications.append(notification)

        if notifications:
            self.db.add_all(notifications)
            await self.db.commit()
            
            # Refresh all notifications
            for notification in notifications:
                await self.db.refresh(notification)
            
            # Send real-time notifications to connected users
            try:
                from app.websocket.manager import connection_manager
                await connection_manager.send_bulk_notifications(
                    user_ids=eligible_users,
                    notification_type=notification_type,
                    title=title,
                    message=message,
                    data=data
                )
            except Exception as e:
                logger.warning(f"Failed to send real-time bulk notifications: {e}")

        logger.info(f"Created {len(notifications)} bulk notifications of type {notification_type}")
        return notifications

    async def get_user_notifications(
        self,
        user_id: UUID,
        unread_only: bool = False,
        limit: int = 50,
        offset: int = 0
    ) -> List[Notification]:
        """
        Get notifications for a user
        """
        query = select(Notification).where(Notification.user_id == user_id)
        
        if unread_only:
            query = query.where(Notification.is_read == False)
        
        # Filter out expired notifications
        query = query.where(
            or_(
                Notification.expires_at.is_(None),
                Notification.expires_at > datetime.utcnow()
            )
        )
        
        query = query.order_by(Notification.created_at.desc())
        query = query.offset(offset).limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()

    async def mark_notification_read(
        self,
        notification_id: UUID,
        user_id: UUID
    ) -> Notification:
        """
        Mark a notification as read
        """
        result = await self.db.execute(
            select(Notification).where(
                and_(
                    Notification.id == notification_id,
                    Notification.user_id == user_id
                )
            )
        )
        notification = result.scalar_one_or_none()
        
        if not notification:
            raise NotFoundError("Notification not found")
        
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(notification)
            
            # Send updated unread count
            try:
                from app.services.notification_broadcaster import NotificationBroadcaster
                unread_count = await self.get_unread_count(user_id)
                await NotificationBroadcaster.send_unread_count_update(user_id, unread_count)
            except Exception as e:
                logger.warning(f"Failed to send unread count update: {e}")
        
        return notification

    async def mark_all_notifications_read(self, user_id: UUID) -> int:
        """
        Mark all notifications as read for a user
        """
        # Update all unread notifications
        result = await self.db.execute(
            select(Notification).where(
                and_(
                    Notification.user_id == user_id,
                    Notification.is_read == False
                )
            )
        )
        notifications = result.scalars().all()
        
        count = 0
        for notification in notifications:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            count += 1
        
        if count > 0:
            await self.db.commit()
            
            # Send updated unread count (should be 0 now)
            try:
                from app.services.notification_broadcaster import NotificationBroadcaster
                await NotificationBroadcaster.send_unread_count_update(user_id, 0)
            except Exception as e:
                logger.warning(f"Failed to send unread count update: {e}")
        
        return count

    async def delete_notification(
        self,
        notification_id: UUID,
        user_id: UUID
    ) -> bool:
        """
        Delete a notification
        """
        result = await self.db.execute(
            delete(Notification).where(
                and_(
                    Notification.id == notification_id,
                    Notification.user_id == user_id
                )
            )
        )
        
        if result.rowcount > 0:
            await self.db.commit()
            return True
        
        return False

    async def get_unread_count(self, user_id: UUID) -> int:
        """
        Get count of unread notifications for a user
        """
        result = await self.db.execute(
            select(func.count(Notification.id)).where(
                and_(
                    Notification.user_id == user_id,
                    Notification.is_read == False,
                    or_(
                        Notification.expires_at.is_(None),
                        Notification.expires_at > datetime.utcnow()
                    )
                )
            )
        )
        return result.scalar() or 0

    async def cleanup_old_notifications(self, days_old: int = 30) -> int:
        """
        Clean up old read notifications
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        result = await self.db.execute(
            delete(Notification).where(
                and_(
                    Notification.is_read == True,
                    Notification.created_at < cutoff_date
                )
            )
        )
        
        deleted_count = result.rowcount
        await self.db.commit()
        
        logger.info(f"Cleaned up {deleted_count} old notifications")
        return deleted_count

    async def get_notification_preferences(
        self, 
        user_id: UUID
    ) -> List[NotificationPreference]:
        """
        Get notification preferences for a user
        """
        result = await self.db.execute(
            select(NotificationPreference).where(
                NotificationPreference.user_id == user_id
            )
        )
        return result.scalars().all()

    async def update_notification_preference(
        self,
        user_id: UUID,
        notification_type: NotificationType,
        email_enabled: Optional[bool] = None,
        push_enabled: Optional[bool] = None,
        in_app_enabled: Optional[bool] = None
    ) -> NotificationPreference:
        """
        Update or create notification preference for a user
        """
        # Try to get existing preference
        result = await self.db.execute(
            select(NotificationPreference).where(
                and_(
                    NotificationPreference.user_id == user_id,
                    NotificationPreference.notification_type == notification_type
                )
            )
        )
        preference = result.scalar_one_or_none()
        
        if preference:
            # Update existing preference
            if email_enabled is not None:
                preference.email_enabled = email_enabled
            if push_enabled is not None:
                preference.push_enabled = push_enabled
            if in_app_enabled is not None:
                preference.in_app_enabled = in_app_enabled
            preference.updated_at = datetime.utcnow()
        else:
            # Create new preference
            preference = NotificationPreference(
                user_id=user_id,
                notification_type=notification_type,
                email_enabled=email_enabled if email_enabled is not None else True,
                push_enabled=push_enabled if push_enabled is not None else True,
                in_app_enabled=in_app_enabled if in_app_enabled is not None else True
            )
            self.db.add(preference)
        
        await self.db.commit()
        await self.db.refresh(preference)
        
        return preference

    async def _should_send_notification(
        self, 
        user_id: UUID, 
        notification_type: NotificationType
    ) -> bool:
        """
        Check if a notification should be sent based on user preferences
        """
        result = await self.db.execute(
            select(NotificationPreference).where(
                and_(
                    NotificationPreference.user_id == user_id,
                    NotificationPreference.notification_type == notification_type
                )
            )
        )
        preference = result.scalar_one_or_none()
        
        # If no preference exists, default to enabled
        if not preference:
            return True
        
        # Check if in-app notifications are enabled (we're creating in-app notifications)
        return preference.in_app_enabled

    async def _get_eligible_users(
        self, 
        user_ids: List[UUID], 
        notification_type: NotificationType
    ) -> List[UUID]:
        """
        Filter users who should receive the notification based on preferences
        """
        # Get users with preferences for this notification type
        result = await self.db.execute(
            select(NotificationPreference).where(
                and_(
                    NotificationPreference.user_id.in_(user_ids),
                    NotificationPreference.notification_type == notification_type,
                    NotificationPreference.in_app_enabled == True
                )
            )
        )
        preferences = result.scalars().all()
        users_with_enabled_prefs = {pref.user_id for pref in preferences}
        
        # Get users without preferences (default to enabled)
        result = await self.db.execute(
            select(NotificationPreference.user_id).where(
                and_(
                    NotificationPreference.user_id.in_(user_ids),
                    NotificationPreference.notification_type == notification_type
                )
            )
        )
        users_with_prefs = {row[0] for row in result.fetchall()}
        users_without_prefs = set(user_ids) - users_with_prefs
        
        # Combine users with enabled preferences and users without preferences
        eligible_users = list(users_with_enabled_prefs | users_without_prefs)
        
        return eligible_users