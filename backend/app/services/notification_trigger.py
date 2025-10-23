"""
Notification trigger service for LemonNPie Backend API
This service provides easy methods to trigger notifications from other services
"""
from typing import Dict, Any, List, Optional
from uuid import UUID

from app.models.enums import NotificationType
from app.tasks.notification_tasks import send_notification_task, send_bulk_notifications_task


class NotificationTrigger:
    """
    Service to trigger notifications from other parts of the application
    """
    
    @staticmethod
    def send_review_vote_notification(
        review_author_id: UUID,
        voter_name: str,
        movie_title: str,
        vote_type: str,
        review_id: UUID
    ):
        """
        Send notification when someone votes on a review
        """
        title = f"Your review received a {vote_type} vote"
        message = f"{voter_name} found your review of '{movie_title}' {vote_type}"
        
        data = {
            "review_id": str(review_id),
            "voter_name": voter_name,
            "movie_title": movie_title,
            "vote_type": vote_type
        }
        
        send_notification_task.delay(
            user_id=str(review_author_id),
            notification_type=NotificationType.REVIEW_VOTE.value,
            title=title,
            message=message,
            data=data
        )
    
    @staticmethod
    def send_new_follower_notification(
        followed_user_id: UUID,
        follower_name: str,
        follower_id: UUID
    ):
        """
        Send notification when someone follows a user
        """
        title = "New follower"
        message = f"{follower_name} started following you"
        
        data = {
            "follower_id": str(follower_id),
            "follower_name": follower_name
        }
        
        send_notification_task.delay(
            user_id=str(followed_user_id),
            notification_type=NotificationType.NEW_FOLLOWER.value,
            title=title,
            message=message,
            data=data
        )
    
    @staticmethod
    def send_movie_added_notification(
        user_ids: List[UUID],
        movie_title: str,
        movie_id: UUID
    ):
        """
        Send notification to users when a new movie is added
        """
        title = "New movie added"
        message = f"'{movie_title}' has been added to LemonNPie"
        
        data = {
            "movie_id": str(movie_id),
            "movie_title": movie_title
        }
        
        user_id_strings = [str(user_id) for user_id in user_ids]
        
        send_bulk_notifications_task.delay(
            user_ids=user_id_strings,
            notification_type=NotificationType.MOVIE_ADDED.value,
            title=title,
            message=message,
            data=data
        )
    
    @staticmethod
    def send_system_announcement(
        user_ids: List[UUID],
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Send system announcement to users
        """
        user_id_strings = [str(user_id) for user_id in user_ids]
        
        send_bulk_notifications_task.delay(
            user_ids=user_id_strings,
            notification_type=NotificationType.SYSTEM_ANNOUNCEMENT.value,
            title=title,
            message=message,
            data=data or {}
        )
    
    @staticmethod
    def send_moderation_action_notification(
        user_id: UUID,
        action: str,
        content_type: str,
        reason: Optional[str] = None
    ):
        """
        Send notification when moderation action is taken on user's content
        """
        title = f"Moderation action: {action}"
        message = f"Your {content_type} has been {action}"
        
        if reason:
            message += f" - Reason: {reason}"
        
        data = {
            "action": action,
            "content_type": content_type,
            "reason": reason
        }
        
        send_notification_task.delay(
            user_id=str(user_id),
            notification_type=NotificationType.MODERATION_ACTION.value,
            title=title,
            message=message,
            data=data
        )