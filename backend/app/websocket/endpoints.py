"""
WebSocket endpoints for real-time notifications
"""
import json
import logging
from typing import Optional

from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.websocket.manager import connection_manager
from app.auth.jwt_service import JWTService
from app.db.database import get_db
from app.models import User
from app.services.notification_service import NotificationService

logger = logging.getLogger(__name__)


async def get_user_from_websocket_token(
    websocket: WebSocket,
    db: AsyncSession
) -> Optional[User]:
    """
    Extract and validate user from WebSocket connection token
    """
    try:
        # Get token from query parameters
        token = websocket.query_params.get("token")
        
        if not token:
            logger.warning("No token provided in WebSocket connection")
            return None
        
        # Validate token
        jwt_service = JWTService()
        payload = jwt_service.decode_token(token)
        
        if not payload:
            logger.warning("Invalid token in WebSocket connection")
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            logger.warning("No user ID in token payload")
            return None
        
        # Get user from database
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            logger.warning(f"User {user_id} not found or inactive")
            return None
        
        return user
        
    except Exception as e:
        logger.error(f"Error validating WebSocket token: {e}")
        return None


async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time notifications
    """
    user = None
    
    try:
        # Get database session
        async for db in get_db():
            try:
                # Authenticate user
                user = await get_user_from_websocket_token(websocket, db)
                
                if not user:
                    await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                
                # Connect user
                await connection_manager.connect(websocket, user.id)
                
                # Send initial unread count
                notification_service = NotificationService(db)
                unread_count = await notification_service.get_unread_count(user.id)
                
                await connection_manager.send_personal_message(
                    user_id=user.id,
                    message={
                        "type": "unread_count",
                        "count": unread_count
                    }
                )
                
                # Listen for messages
                while True:
                    try:
                        # Receive message from client
                        data = await websocket.receive_text()
                        message = json.loads(data)
                        
                        # Handle different message types
                        await handle_websocket_message(
                            user=user,
                            message=message,
                            websocket=websocket,
                            db=db
                        )
                        
                    except WebSocketDisconnect:
                        logger.info(f"WebSocket disconnected for user {user.id}")
                        break
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON received from user {user.id}")
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": "Invalid JSON format"
                        }))
                    except Exception as e:
                        logger.error(f"Error handling WebSocket message: {e}")
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "message": "Internal server error"
                        }))
                        
            finally:
                await db.close()
                
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        if user:
            connection_manager.disconnect(websocket)


async def handle_websocket_message(
    user: User,
    message: dict,
    websocket: WebSocket,
    db: AsyncSession
):
    """
    Handle incoming WebSocket messages from clients
    """
    message_type = message.get("type")
    
    if message_type == "ping":
        # Respond to ping with pong
        await websocket.send_text(json.dumps({
            "type": "pong",
            "timestamp": message.get("timestamp")
        }))
        
    elif message_type == "mark_read":
        # Mark notification as read
        notification_id = message.get("notification_id")
        if notification_id:
            try:
                notification_service = NotificationService(db)
                await notification_service.mark_notification_read(
                    notification_id=notification_id,
                    user_id=user.id
                )
                
                # Send updated unread count
                unread_count = await notification_service.get_unread_count(user.id)
                await websocket.send_text(json.dumps({
                    "type": "unread_count",
                    "count": unread_count
                }))
                
            except Exception as e:
                logger.error(f"Error marking notification as read: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Failed to mark notification as read"
                }))
    
    elif message_type == "get_unread_count":
        # Send current unread count
        try:
            notification_service = NotificationService(db)
            unread_count = await notification_service.get_unread_count(user.id)
            await websocket.send_text(json.dumps({
                "type": "unread_count",
                "count": unread_count
            }))
        except Exception as e:
            logger.error(f"Error getting unread count: {e}")
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Failed to get unread count"
            }))
    
    else:
        # Unknown message type
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": f"Unknown message type: {message_type}"
        }))