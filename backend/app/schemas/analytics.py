"""
Pydantic schemas for analytics data
"""
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from uuid import UUID
from pydantic import BaseModel, Field


class UserActivityCreate(BaseModel):
    """Schema for creating user activity records"""
    activity_type: str = Field(..., description="Type of activity (login, view_movie, etc.)")
    resource_type: Optional[str] = Field(None, description="Type of resource (movie, review, user)")
    resource_id: Optional[UUID] = Field(None, description="ID of the resource")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="Additional context data")
    session_id: Optional[str] = Field(None, description="Session identifier")
    ip_address: Optional[str] = Field(None, description="User's IP address")
    user_agent: Optional[str] = Field(None, description="User's browser/client info")


class UserActivityResponse(BaseModel):
    """Schema for user activity responses"""
    id: UUID
    user_id: Optional[UUID]
    activity_type: str
    resource_type: Optional[str]
    resource_id: Optional[UUID]
    extra_data: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ContentMetricCreate(BaseModel):
    """Schema for creating content metrics"""
    content_type: str = Field(..., description="Type of content (movie, review)")
    content_id: UUID = Field(..., description="ID of the content")
    metric_type: str = Field(..., description="Type of metric (views, likes, etc.)")
    metric_value: float = Field(default=1.0, description="Metric value")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="Additional metric data")


class ContentMetricResponse(BaseModel):
    """Schema for content metric responses"""
    id: UUID
    content_type: str
    content_id: UUID
    metric_type: str
    metric_value: float
    date: datetime
    extra_data: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True


class SystemMetricCreate(BaseModel):
    """Schema for creating system metrics"""
    metric_name: str = Field(..., description="Name of the metric")
    metric_value: float = Field(..., description="Metric value")
    metric_unit: Optional[str] = Field(None, description="Unit of measurement")
    component: Optional[str] = Field(None, description="System component")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="Additional metric data")


class SystemMetricResponse(BaseModel):
    """Schema for system metric responses"""
    id: UUID
    metric_name: str
    metric_value: float
    metric_unit: Optional[str]
    component: Optional[str]
    extra_data: Optional[Dict[str, Any]]
    timestamp: datetime
    
    class Config:
        from_attributes = True


class UserActivitySummary(BaseModel):
    """Schema for user activity summary"""
    user_id: str
    period: Dict[str, str]
    total_activities: int
    activity_breakdown: Dict[str, int]
    most_active_days: List[Dict[str, Union[str, int]]]


class ContentPerformance(BaseModel):
    """Schema for content performance metrics"""
    content_type: str
    content_id: str
    period: Dict[str, str]
    metrics_summary: Dict[str, Dict[str, float]]
    daily_trends: Dict[str, Dict[str, float]]


class SystemPerformanceSummary(BaseModel):
    """Schema for system performance summary"""
    component: Optional[str]
    period: Dict[str, str]
    metrics: Dict[str, Dict[str, float]]


class UserEngagementMetricsResponse(BaseModel):
    """Schema for user engagement metrics"""
    id: UUID
    user_id: UUID
    date: datetime
    session_count: int
    session_duration_minutes: float
    pages_viewed: int
    movies_viewed: int
    reviews_written: int
    reviews_voted: int
    social_interactions: int
    last_activity: Optional[datetime]
    
    class Config:
        from_attributes = True


class AnalyticsReportCreate(BaseModel):
    """Schema for creating analytics reports"""
    report_type: str = Field(..., description="Type of report")
    report_name: str = Field(..., description="Name of the report")
    description: Optional[str] = Field(None, description="Report description")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Report parameters")
    format: str = Field(default="json", description="Report format")
    is_public: bool = Field(default=False, description="Whether report is public")


class AnalyticsReportResponse(BaseModel):
    """Schema for analytics report responses"""
    id: UUID
    report_type: str
    report_name: str
    description: Optional[str]
    parameters: Optional[Dict[str, Any]]
    data: Dict[str, Any]
    format: str
    file_url: Optional[str]
    generated_by: UUID
    generated_at: datetime
    expires_at: Optional[datetime]
    is_public: bool
    
    class Config:
        from_attributes = True


class UserEngagementReport(BaseModel):
    """Schema for user engagement reports"""
    period: Dict[str, str]
    total_users: int
    active_users: int
    new_users: int
    user_retention_rate: float
    average_session_duration: float
    top_activities: List[Dict[str, Union[str, int]]]
    engagement_trends: Dict[str, Dict[str, Union[int, float]]]


class ContentPopularityReport(BaseModel):
    """Schema for content popularity reports"""
    period: Dict[str, str]
    total_content: int
    most_viewed_content: List[Dict[str, Any]]
    content_performance: Dict[str, Dict[str, float]]
    trending_content: List[Dict[str, Any]]
    content_engagement_rates: Dict[str, float]


class SystemHealthReport(BaseModel):
    """Schema for system health reports"""
    period: Dict[str, str]
    overall_health_score: float
    component_health: Dict[str, Dict[str, float]]
    performance_metrics: Dict[str, Dict[str, float]]
    error_rates: Dict[str, float]
    uptime_percentage: float


class AnalyticsFilters(BaseModel):
    """Schema for analytics query filters"""
    start_date: Optional[datetime] = Field(None, description="Start date for filtering")
    end_date: Optional[datetime] = Field(None, description="End date for filtering")
    user_id: Optional[UUID] = Field(None, description="Filter by user ID")
    content_type: Optional[str] = Field(None, description="Filter by content type")
    content_id: Optional[UUID] = Field(None, description="Filter by content ID")
    activity_type: Optional[str] = Field(None, description="Filter by activity type")
    metric_type: Optional[str] = Field(None, description="Filter by metric type")
    component: Optional[str] = Field(None, description="Filter by system component")
    limit: int = Field(default=100, ge=1, le=1000, description="Limit results")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")


class AnalyticsDashboard(BaseModel):
    """Schema for analytics dashboard data"""
    overview: Dict[str, Union[int, float]]
    user_engagement: UserEngagementReport
    content_performance: ContentPopularityReport
    system_health: SystemHealthReport
    recent_activities: List[UserActivityResponse]
    alerts: List[Dict[str, Any]]