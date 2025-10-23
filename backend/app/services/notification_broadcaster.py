"""
Notification broadcasting service for real-time notifications
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from uuid import UUID

from app.websocket.manager import connection_manager
from app.models.enums import NotificationType

logger = logging.getLogger(__name__)


class NotificationBroadcaster:
    """
    Service for broadcasting real-time notifications
    """
    
    @staticmethod
    async def broadcast_to_user(
        user_id: UUID,
        notification_type: NotificationType,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        notification_id: Optional[UUID] = None
    ):
        """
        Broadcast a notification to a specific user in real-time
        """
        try:
            await connection_manager.send_notification(
                user_id=user_id,
                notification_type=notification_type,
                title=title,
                message=message,
                data=data,
                notification_id=notification_id
            )
            logger.info(f"Broadcasted notification to user {user_id}")
        except Exception as e:
            logger.error(f"Failed to broadcast notification to user {user_id}: {e}")
    
    @staticmethod
    async def broadcast_to_users(
        user_ids: List[UUID],
        notification_type: NotificationType,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Broadcast notifications to multiple users in real-time
        """
        try:
            await connection_manager.send_bulk_notifications(
                user_ids=user_ids,
                notification_type=notification_type,
                title=title,
                message=message,
                data=data
            )
            logger.info(f"Broadcasted notifications to {len(user_ids)} users")
        except Exception as e:
            logger.error(f"Failed to broadcast notifications to users: {e}")
    
    @staticmethod
    async def broadcast_system_announcement(
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Broadcast a system announcement to all connected users
        """
        try:
            system_message = {
                "type": "system_announcement",
                "title": title,
                "message": message,
                "data": data or {},
                "timestamp": asyncio.get_event_loop().time()
            }
            
            await connection_manager.broadcast_system_message(system_message)
            logger.info("Broadcasted system announcement to all connected users")
        except Exception as e:
            logger.error(f"Failed to broadcast system announcement: {e}")
    
    @staticmethod
    async def send_unread_count_update(user_id: UUID, unread_count: int):
        """
        Send updated unread count to a user
        """
        try:
            await connection_manager.send_personal_message(
                user_id=user_id,
                message={
                    "type": "unread_count",
                    "count": unread_count
                }
            )
            logger.debug(f"Sent unread count update to user {user_id}: {unread_count}")
        except Exception as e:
            logger.error(f"Failed to send unread count update to user {user_id}: {e}")
    
    @staticmethod
    def get_connected_users() -> List[UUID]:
        """
        Get list of currently connected users
        """
        return connection_manager.get_connected_users()
    
    @staticmethod
    def get_connection_stats() -> Dict[str, int]:
        """
        Get connection statistics
        """
        return {
            "connected_users": len(connection_manager.get_connected_users()),
            "total_connections": connection_manager.get_connection_count()
        }
    
    @staticmethod
    def is_user_online(user_id: UUID) -> bool:
        """
        Check if a user is currently connected
        """
        return connection_manager.is_user_connected(user_id)