# LemonNPie Notification System

## Overview

The LemonNPie notification system provides both persistent and real-time notifications to users. It consists of several components working together to deliver notifications efficiently.

## Components

### 1. Database Models

- **Notification**: Stores persistent notifications with metadata
- **NotificationPreference**: User preferences for different notification types
- **NotificationType**: Enum defining available notification types

### 2. Background Tasks (Celery)

- **send_notification_task**: Sends individual notifications
- **send_bulk_notifications_task**: Sends notifications to multiple users
- **cleanup_old_notifications_task**: Cleans up old read notifications

### 3. Real-time WebSocket

- **WebSocket Manager**: Manages active WebSocket connections
- **Connection Manager**: Handles user connections and message broadcasting
- **WebSocket Endpoints**: Provides real-time notification delivery

### 4. Services

- **NotificationService**: Core notification CRUD operations
- **NotificationTrigger**: Helper service to trigger notifications from other services
- **NotificationBroadcaster**: Real-time notification broadcasting

## Notification Types

1. **REVIEW_VOTE**: When someone votes on a user's review
2. **NEW_FOLLOWER**: When someone follows a user
3. **REVIEW_COMMENT**: When someone comments on a review (future feature)
4. **MOVIE_ADDED**: When new movies are added to the platform
5. **SYSTEM_ANNOUNCEMENT**: System-wide announcements
6. **MODERATION_ACTION**: When moderation actions are taken on user content

## API Endpoints

### REST API

- `GET /api/v1/notifications/` - Get user notifications
- `GET /api/v1/notifications/stats` - Get notification statistics
- `PATCH /api/v1/notifications/{id}/read` - Mark notification as read
- `PATCH /api/v1/notifications/read-all` - Mark all notifications as read
- `DELETE /api/v1/notifications/{id}` - Delete notification
- `GET /api/v1/notifications/preferences` - Get notification preferences
- `PATCH /api/v1/notifications/preferences/{type}` - Update notification preference

### Admin Endpoints

- `POST /api/v1/notifications/bulk` - Send bulk notifications
- `POST /api/v1/notifications/cleanup` - Cleanup old notifications
- `GET /api/v1/notifications/websocket/stats` - Get WebSocket statistics
- `POST /api/v1/notifications/websocket/broadcast` - Broadcast system announcement

### WebSocket

- `ws://localhost:8000/ws/notifications?token={jwt_token}` - Real-time notifications

## WebSocket Message Types

### Client to Server

```json
{
  "type": "ping",
  "timestamp": 1234567890
}
```

```json
{
  "type": "mark_read",
  "notification_id": "uuid"
}
```

```json
{
  "type": "get_unread_count"
}
```

### Server to Client

```json
{
  "type": "notification",
  "notification_type": "review_vote",
  "title": "Your review received a helpful vote",
  "message": "John found your review of 'Movie Title' helpful",
  "data": {
    "review_id": "uuid",
    "voter_name": "John",
    "movie_title": "Movie Title",
    "vote_type": "helpful"
  },
  "notification_id": "uuid",
  "timestamp": 1234567890
}
```

```json
{
  "type": "unread_count",
  "count": 5
}
```

## Usage Examples

### Triggering Notifications from Services

```python
from app.services.notification_trigger import NotificationTrigger

# Send review vote notification
NotificationTrigger.send_review_vote_notification(
    review_author_id=user_id,
    voter_name="John Doe",
    movie_title="The Wedding Party",
    vote_type="helpful",
    review_id=review_id
)

# Send new follower notification
NotificationTrigger.send_new_follower_notification(
    followed_user_id=user_id,
    follower_name="Jane Doe",
    follower_id=follower_id
)
```

### Real-time Broadcasting

```python
from app.services.notification_broadcaster import NotificationBroadcaster

# Broadcast to specific user
await NotificationBroadcaster.broadcast_to_user(
    user_id=user_id,
    notification_type=NotificationType.SYSTEM_ANNOUNCEMENT,
    title="System Maintenance",
    message="The system will be down for maintenance at 2 AM UTC"
)

# Broadcast system announcement
await NotificationBroadcaster.broadcast_system_announcement(
    title="New Feature Released",
    message="Check out our new movie recommendation engine!"
)
```

## Setup and Configuration

### 1. Database Migration

```bash
cd backend
alembic upgrade head
```

### 2. Start Redis (required for Celery)

```bash
docker run -d -p 6379:6379 redis:7-alpine
```

### 3. Start Celery Worker

```bash
cd backend
python celery_worker.py worker --loglevel=info --queues=notifications
```

### 4. Start FastAPI Server

```bash
cd backend
python run.py
```

## Testing

### Test Notification System

```bash
cd backend
python test_notifications.py
```

### Test WebSocket Connection

1. Get a JWT token by logging in through the API
2. Update the token in `test_websocket.py`
3. Run the WebSocket test:

```bash
cd backend
python test_websocket.py
```

## Configuration

### Environment Variables

- `REDIS_URL`: Redis connection URL for Celery broker
- `DATABASE_URL`: PostgreSQL connection URL
- `SECRET_KEY`: JWT secret key for WebSocket authentication

### Notification Preferences

Users can configure their notification preferences for each notification type:

- `email_enabled`: Receive email notifications (future feature)
- `push_enabled`: Receive push notifications (future feature)
- `in_app_enabled`: Receive in-app notifications

## Performance Considerations

1. **WebSocket Connections**: The system can handle multiple connections per user
2. **Background Tasks**: Notifications are processed asynchronously via Celery
3. **Caching**: Frequently accessed data is cached in Redis
4. **Cleanup**: Old read notifications are automatically cleaned up

## Security

1. **WebSocket Authentication**: JWT tokens are required for WebSocket connections
2. **Rate Limiting**: API endpoints are rate-limited to prevent abuse
3. **Input Validation**: All notification data is validated before processing
4. **User Isolation**: Users can only access their own notifications

## Future Enhancements

1. **Email Notifications**: Send notifications via email
2. **Push Notifications**: Mobile push notification support
3. **Notification Templates**: Customizable notification templates
4. **Advanced Filtering**: More sophisticated notification filtering options
5. **Notification Scheduling**: Schedule notifications for future delivery