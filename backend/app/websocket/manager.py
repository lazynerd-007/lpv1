"""
WebSocket connection manager for real-time notifications
"""
import json
import logging
from typing import Dict, List, Set, Optional, Any
from uuid import UUID
import asyncio

from fastapi import WebSocket, WebSocketDisconnect
from app.models.enums import NotificationType

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections for real-time notifications
    """
    
    def __init__(self):
        # Store active connections by user_id
        self.active_connections: Dict[UUID, Set[WebSocket]] = {}
        # Store user_id by websocket for quick lookup
        self.connection_users: Dict[WebSocket, UUID] = {}
        
    async def connect(self, websocket: WebSocket, user_id: UUID):
        """
        Accept a new WebSocket connection and associate it with a user
        """
        await websocket.accept()
        
        # Add connection to user's set
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        self.connection_users[websocket] = user_id
        
        logger.info(f"WebSocket connected for user {user_id}")
        
        # Send connection confirmation
        await self.send_personal_message(
            user_id=user_id,
            message={
                "type": "connection_established",
                "message": "Connected to notification service",
                "timestamp": asyncio.get_event_loop().time()
            }
        )
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection
        """
        user_id = self.connection_users.get(websocket)
        
        if user_id:
            # Remove from user's connections
            if user_id in self.active_connections:
                self.active_connections[user_id].discard(websocket)
                
                # Remove user entry if no more connections
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
            
            # Remove from connection lookup
            del self.connection_users[websocket]
            
            logger.info(f"WebSocket disconnected for user {user_id}")
    
    async def send_personal_message(self, user_id: UUID, message: Dict[str, Any]):
        """
        Send a message to all connections for a specific user
        """
        if user_id not in self.active_connections:
            logger.debug(f"No active connections for user {user_id}")
            return
        
        # Get all connections for this user
        connections = self.active_connections[user_id].copy()
        
        # Send message to all user's connections
        disconnected_connections = []
        
        for connection in connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.warning(f"Failed to send message to connection: {e}")
                disconnected_connections.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected_connections:
            self.disconnect(connection)
    
    async def send_notification(
        self, 
        user_id: UUID, 
        notification_type: NotificationType,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        notification_id: Optional[UUID] = None
    ):
        """
        Send a real-time notification to a user
        """
        notification_message = {
            "type": "notification",
            "notification_type": notification_type.value,
            "title": title,
            "message": message,
            "data": data or {},
            "timestamp": asyncio.get_event_loop().time()
        }
        
        if notification_id:
            notification_message["notification_id"] = str(notification_id)
        
        await self.send_personal_message(user_id, notification_message)
        logger.info(f"Sent real-time notification to user {user_id}: {notification_type}")
    
    async def send_bulk_notifications(
        self,
        user_ids: List[UUID],
        notification_type: NotificationType,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Send notifications to multiple users
        """
        tasks = []
        
        for user_id in user_ids:
            task = self.send_notification(
                user_id=user_id,
                notification_type=notification_type,
                title=title,
                message=message,
                data=data
            )
            tasks.append(task)
        
        # Send all notifications concurrently
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(f"Sent bulk notifications to {len(user_ids)} users: {notification_type}")
    
    async def broadcast_system_message(self, message: Dict[str, Any]):
        """
        Broadcast a message to all connected users
        """
        if not self.active_connections:
            logger.debug("No active connections for broadcast")
            return
        
        tasks = []
        
        for user_id in self.active_connections.keys():
            task = self.send_personal_message(user_id, message)
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info(f"Broadcasted system message to {len(self.active_connections)} users")
    
    def get_connected_users(self) -> List[UUID]:
        """
        Get list of currently connected user IDs
        """
        return list(self.active_connections.keys())
    
    def get_connection_count(self) -> int:
        """
        Get total number of active connections
        """
        return sum(len(connections) for connections in self.active_connections.values())
    
    def is_user_connected(self, user_id: UUID) -> bool:
        """
        Check if a user has any active connections
        """
        return user_id in self.active_connections and len(self.active_connections[user_id]) > 0


# Global connection manager instance
connection_manager = ConnectionManager()