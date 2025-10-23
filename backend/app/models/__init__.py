"""
Database models for LemonNPie Backend API
"""

# Import all models to ensure they are registered with SQLAlchemy
from app.models.user import User
from app.models.movie import Movie
from app.models.review import Review
from app.models.relationships import (
    UserFollow,
    UserWatchlist,
    UserFavorite,
    ReviewVote,
    MovieGenre,
    MovieLanguage,
    MovieCast
)
from app.models.moderation import UserReport, Notification, NotificationPreference
from app.models.search import MovieSearchIndex
from app.models.analytics import (
    UserActivity,
    ContentMetrics,
    SystemMetrics,
    AnalyticsReport,
    UserEngagementMetrics
)
from app.models.enums import UserRole, ContentType, ModerationStatus, VoteType, CastRole, NotificationType

__all__ = [
    "User",
    "Movie", 
    "Review",
    "UserFollow",
    "UserWatchlist",
    "UserFavorite",
    "ReviewVote",
    "MovieGenre",
    "MovieLanguage",
    "MovieCast",
    "UserReport",
    "Notification",
    "NotificationPreference",
    "MovieSearchIndex",
    "UserActivity",
    "ContentMetrics",
    "SystemMetrics",
    "AnalyticsReport",
    "UserEngagementMetrics",
    "UserRole",
    "ContentType",
    "ModerationStatus",
    "VoteType",
    "CastRole",
    "NotificationType"
]