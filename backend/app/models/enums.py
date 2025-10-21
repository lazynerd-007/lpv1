"""
Enums for LemonNPie Backend API models
"""
import enum


class UserRole(str, enum.Enum):
    USER = "user"
    CRITIC = "critic"
    MODERATOR = "moderator"
    ADMIN = "admin"


class ContentType(str, enum.Enum):
    MOVIE = "movie"
    SERIES = "series"


class ModerationStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class VoteType(str, enum.Enum):
    HELPFUL = "helpful"
    UNHELPFUL = "unhelpful"


class CastRole(str, enum.Enum):
    ACTOR = "actor"
    DIRECTOR = "director"
    PRODUCER = "producer"
    WRITER = "writer"