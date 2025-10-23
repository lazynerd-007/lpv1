"""
Admin schemas for LemonNPie Backend API
"""
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

from app.models.enums import UserRole, ModerationStatus, VoteType


# Dashboard Analytics Schemas
class SystemMetrics(BaseModel):
    """System-wide metrics for admin dashboard"""
    total_users: int
    total_movies: int
    total_reviews: int
    total_reports: int
    active_users_today: int
    active_users_week: int
    active_users_month: int
    new_users_today: int
    new_users_week: int
    new_users_month: int
    reviews_today: int
    reviews_week: int
    reviews_month: int
    pending_reports: int
    flagged_reviews: int


class UserAnalytics(BaseModel):
    """User analytics data"""
    user_growth: List[Dict[str, Any]]  # Daily/weekly/monthly user growth
    user_activity: List[Dict[str, Any]]  # User activity patterns
    role_distribution: Dict[str, int]  # Distribution of user roles
    top_reviewers: List[Dict[str, Any]]  # Most active reviewers
    user_retention: Dict[str, float]  # User retention metrics


class ContentAnalytics(BaseModel):
    """Content analytics data"""
    review_trends: List[Dict[str, Any]]  # Review submission trends
    rating_distribution: Dict[int, int]  # Distribution of ratings
    popular_movies: List[Dict[str, Any]]  # Most reviewed/rated movies
    genre_popularity: List[Dict[str, Any]]  # Popular genres
    content_moderation_stats: Dict[str, int]  # Moderation statistics


class AdminDashboard(BaseModel):
    """Complete admin dashboard data"""
    system_metrics: SystemMetrics
    user_analytics: UserAnalytics
    content_analytics: ContentAnalytics
    recent_activity: List[Dict[str, Any]]  # Recent platform activity


# User Management Schemas
class UserListItem(BaseModel):
    """User item for admin user list"""
    id: UUID
    email: str
    name: str
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    total_reviews: int
    total_followers: int
    last_login: Optional[datetime] = None


class UserListResponse(BaseModel):
    """Paginated user list response"""
    users: List[UserListItem]
    total: int
    page: int
    per_page: int
    total_pages: int


class UserRoleUpdate(BaseModel):
    """Schema for updating user role"""
    role: UserRole


class UserSuspension(BaseModel):
    """Schema for user suspension"""
    reason: str = Field(..., min_length=10, max_length=500)
    duration_days: Optional[int] = Field(None, ge=1, le=365)  # None for permanent


class UserActivation(BaseModel):
    """Schema for user activation"""
    reason: str = Field(..., min_length=10, max_length=500)


# Content Moderation Schemas
class ReviewModerationItem(BaseModel):
    """Review item for moderation dashboard"""
    id: UUID
    user_id: UUID
    user_name: str
    movie_id: UUID
    movie_title: str
    review_text: str
    lemon_pie_rating: int
    is_flagged: bool
    moderation_status: ModerationStatus
    created_at: datetime
    report_count: int


class ReviewModerationResponse(BaseModel):
    """Paginated review moderation response"""
    reviews: List[ReviewModerationItem]
    total: int
    page: int
    per_page: int
    total_pages: int


class ModerationAction(BaseModel):
    """Schema for moderation actions"""
    action: str = Field(..., regex="^(approve|reject|flag)$")
    reason: Optional[str] = Field(None, max_length=500)


class BulkModerationAction(BaseModel):
    """Schema for bulk moderation actions"""
    review_ids: List[UUID] = Field(..., min_items=1, max_items=100)
    action: str = Field(..., regex="^(approve|reject|flag)$")
    reason: Optional[str] = Field(None, max_length=500)


# Report Management Schemas
class ReportItem(BaseModel):
    """Report item for admin dashboard"""
    id: UUID
    reporter_id: UUID
    reporter_name: str
    reported_user_id: Optional[UUID] = None
    reported_user_name: Optional[str] = None
    reported_review_id: Optional[UUID] = None
    reason: str
    description: Optional[str] = None
    status: ModerationStatus
    created_at: datetime
    resolved_by: Optional[UUID] = None
    resolved_at: Optional[datetime] = None


class ReportListResponse(BaseModel):
    """Paginated report list response"""
    reports: List[ReportItem]
    total: int
    page: int
    per_page: int
    total_pages: int


class ReportResolution(BaseModel):
    """Schema for resolving reports"""
    action: str = Field(..., regex="^(dismiss|warn|suspend|ban)$")
    reason: str = Field(..., min_length=10, max_length=500)
    notify_reporter: bool = True
    notify_reported: bool = True


# Analytics Request Schemas
class AnalyticsDateRange(BaseModel):
    """Date range for analytics queries"""
    start_date: date
    end_date: date
    granularity: str = Field("day", regex="^(hour|day|week|month)$")


class AnalyticsFilter(BaseModel):
    """Filters for analytics queries"""
    user_role: Optional[UserRole] = None
    content_type: Optional[str] = None
    genre: Optional[str] = None
    date_range: Optional[AnalyticsDateRange] = None


# Export Schemas
class ExportRequest(BaseModel):
    """Schema for data export requests"""
    export_type: str = Field(..., regex="^(users|reviews|reports|analytics)$")
    format: str = Field("csv", regex="^(csv|json|xlsx)$")
    filters: Optional[Dict[str, Any]] = None
    date_range: Optional[AnalyticsDateRange] = None


class ExportResponse(BaseModel):
    """Response for export requests"""
    export_id: UUID
    status: str
    download_url: Optional[str] = None
    created_at: datetime
    expires_at: datetime