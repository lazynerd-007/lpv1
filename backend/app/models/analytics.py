"""
Analytics models for tracking user behavior and system performance
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column, String, Integer, DateTime, Float, Text, Boolean, ForeignKey, Index, JSON
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class UserActivity(Base):
    """Track user activities for analytics"""
    __tablename__ = "user_activities"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    session_id = Column(String(255), nullable=True)
    activity_type = Column(String(100), nullable=False)  # login, logout, view_movie, write_review, etc.
    resource_type = Column(String(50), nullable=True)  # movie, review, user
    resource_id = Column(String(36), nullable=True)
    extra_data = Column(JSON, nullable=True)  # Additional context data (JSON for SQLite compatibility)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="activities")
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_user_activities_user_id", "user_id"),
        Index("idx_user_activities_type", "activity_type"),
        Index("idx_user_activities_created_at", "created_at"),
        Index("idx_user_activities_resource", "resource_type", "resource_id"),
    )


class ContentMetrics(Base):
    """Track content performance metrics"""
    __tablename__ = "content_metrics"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    content_type = Column(String(50), nullable=False)  # movie, review
    content_id = Column(String(36), nullable=False)
    metric_type = Column(String(100), nullable=False)  # views, likes, shares, etc.
    metric_value = Column(Float, nullable=False, default=0.0)
    date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    extra_data = Column(JSON, nullable=True)
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_content_metrics_content", "content_type", "content_id"),
        Index("idx_content_metrics_type", "metric_type"),
        Index("idx_content_metrics_date", "date"),
    )


class SystemMetrics(Base):
    """Track system performance metrics"""
    __tablename__ = "system_metrics"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(50), nullable=True)  # ms, bytes, count, etc.
    component = Column(String(100), nullable=True)  # api, database, cache, etc.
    extra_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_system_metrics_name", "metric_name"),
        Index("idx_system_metrics_component", "component"),
        Index("idx_system_metrics_timestamp", "timestamp"),
    )


class AnalyticsReport(Base):
    """Store generated analytics reports"""
    __tablename__ = "analytics_reports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    report_type = Column(String(100), nullable=False)  # user_engagement, content_performance, etc.
    report_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    parameters = Column(JSON, nullable=True)  # Report generation parameters
    data = Column(JSON, nullable=False)  # Report data
    format = Column(String(20), nullable=False, default="json")  # json, csv, pdf
    file_url = Column(String(500), nullable=True)  # URL if exported to file
    generated_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_public = Column(Boolean, default=False)
    
    # Relationships
    generator = relationship("User")
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_analytics_reports_type", "report_type"),
        Index("idx_analytics_reports_generated_by", "generated_by"),
        Index("idx_analytics_reports_generated_at", "generated_at"),
    )


class UserEngagementMetrics(Base):
    """Aggregated user engagement metrics"""
    __tablename__ = "user_engagement_metrics"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    session_count = Column(Integer, default=0)
    session_duration_minutes = Column(Float, default=0.0)
    pages_viewed = Column(Integer, default=0)
    movies_viewed = Column(Integer, default=0)
    reviews_written = Column(Integer, default=0)
    reviews_voted = Column(Integer, default=0)
    social_interactions = Column(Integer, default=0)  # follows, unfollows
    last_activity = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User")
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_user_engagement_user_date", "user_id", "date"),
        Index("idx_user_engagement_date", "date"),
    )