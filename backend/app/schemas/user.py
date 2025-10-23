"""
User schemas for LemonNPie Backend API
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, validator
from app.models.enums import UserRole


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    bio: Optional[str] = Field(None, max_length=1000)
    location: Optional[str] = Field(None, max_length=255)
    avatar_url: Optional[str] = Field(None, max_length=500)
    
    @validator('name')
    def validate_name(cls, v):
        """Validate name format"""
        if v is not None:
            if not v.strip():
                raise ValueError('Name cannot be empty')
            
            # Check for valid characters (letters, spaces, hyphens, apostrophes)
            import re
            if not re.match(r"^[a-zA-Z\s\-']+$", v):
                raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
            
            return v.strip()
        return v


class UserStats(BaseModel):
    """Schema for user statistics"""
    total_reviews: int
    average_rating: Optional[float] = None
    followers_count: int
    following_count: int
    watchlist_count: int
    favorites_count: int
    
    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    """Schema for user profile response"""
    id: UUID
    email: str
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    role: UserRole
    is_verified: bool
    created_at: datetime
    stats: UserStats
    
    class Config:
        from_attributes = True


class UserPublicProfile(BaseModel):
    """Schema for public user profile (limited information)"""
    id: UUID
    name: str
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    role: UserRole
    is_verified: bool
    created_at: datetime
    stats: Optional[UserStats] = None
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for user list response with pagination"""
    users: List[UserPublicProfile]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool
    
    class Config:
        from_attributes = True


class ActivityItem(BaseModel):
    """Schema for activity feed item"""
    id: UUID
    type: str  # 'review_posted', 'user_followed', 'movie_watchlisted', 'movie_favorited'
    user: UserPublicProfile
    title: str
    description: str
    data: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ActivityFeedResponse(BaseModel):
    """Schema for activity feed response with pagination"""
    activities: List[ActivityItem]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool
    
    class Config:
        from_attributes = True


class MovieListItem(BaseModel):
    """Schema for movie in user lists (watchlist/favorites)"""
    id: UUID
    title: str
    local_title: Optional[str] = None
    release_date: datetime
    runtime: Optional[int] = None
    plot_summary: Optional[str] = None
    poster_url: Optional[str] = None
    director: Optional[str] = None
    added_at: datetime
    
    class Config:
        from_attributes = True


class MovieListResponse(BaseModel):
    """Schema for movie list response with pagination"""
    movies: List[MovieListItem]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool
    
    class Config:
        from_attributes = True