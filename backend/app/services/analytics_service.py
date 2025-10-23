"""
Analytics service for tracking user behavior and system performance
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from uuid import UUID
import json
import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc, asc
from sqlalchemy.orm import selectinload

from app.models.analytics import (
    UserActivity,
    ContentMetrics,
    SystemMetrics,
    AnalyticsReport,
    UserEngagementMetrics
)
from app.models.user import User
from app.models.movie import Movie
from app.models.review import Review
from app.cache.redis import get_redis_client


class AnalyticsService:
    """Service for collecting and analyzing user behavior and system metrics"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis = None
    
    async def get_redis(self):
        """Get Redis client for caching"""
        if not self.redis:
            self.redis = await get_redis_client()
        return self.redis
    
    # User Activity Tracking
    async def track_user_activity(
        self,
        user_id: Optional[UUID],
        activity_type: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[UUID] = None,
        extra_data: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> UserActivity:
        """Track a user activity event"""
        activity = UserActivity(
            user_id=user_id,
            session_id=session_id,
            activity_type=activity_type,
            resource_type=resource_type,
            resource_id=resource_id,
            extra_data=extra_data,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.db.add(activity)
        await self.db.commit()
        await self.db.refresh(activity)
        
        # Update user engagement metrics asynchronously
        if user_id:
            asyncio.create_task(self._update_user_engagement_metrics(user_id, activity_type))
        
        return activity
    
    async def _update_user_engagement_metrics(self, user_id: UUID, activity_type: str):
        """Update aggregated user engagement metrics"""
        try:
            today = datetime.utcnow().date()
            
            # Get or create today's engagement record
            stmt = select(UserEngagementMetrics).where(
                and_(
                    UserEngagementMetrics.user_id == user_id,
                    func.date(UserEngagementMetrics.date) == today
                )
            )
            result = await self.db.execute(stmt)
            engagement = result.scalar_one_or_none()
            
            if not engagement:
                engagement = UserEngagementMetrics(
                    user_id=user_id,
                    date=datetime.utcnow()
                )
                self.db.add(engagement)
            
            # Update metrics based on activity type
            if activity_type == "login":
                engagement.session_count += 1
            elif activity_type == "view_movie":
                engagement.movies_viewed += 1
                engagement.pages_viewed += 1
            elif activity_type == "write_review":
                engagement.reviews_written += 1
            elif activity_type == "vote_review":
                engagement.reviews_voted += 1
            elif activity_type in ["follow_user", "unfollow_user"]:
                engagement.social_interactions += 1
            else:
                engagement.pages_viewed += 1
            
            engagement.last_activity = datetime.utcnow()
            
            await self.db.commit()
        except Exception as e:
            # Log error but don't fail the main operation
            print(f"Error updating user engagement metrics: {e}")
            await self.db.rollback()
    
    # Content Metrics Tracking
    async def track_content_metric(
        self,
        content_type: str,
        content_id: UUID,
        metric_type: str,
        metric_value: float = 1.0,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> ContentMetrics:
        """Track a content performance metric"""
        metric = ContentMetrics(
            content_type=content_type,
            content_id=content_id,
            metric_type=metric_type,
            metric_value=metric_value,
            extra_data=extra_data
        )
        
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        
        return metric
    
    async def increment_content_metric(
        self,
        content_type: str,
        content_id: UUID,
        metric_type: str,
        increment: float = 1.0
    ):
        """Increment a content metric (like view count)"""
        redis = await self.get_redis()
        cache_key = f"content_metric:{content_type}:{content_id}:{metric_type}"
        
        # Use Redis for real-time counting, batch update to DB
        await redis.incrbyfloat(cache_key, increment)
        await redis.expire(cache_key, 300)  # 5 minutes TTL
    
    # System Metrics Tracking
    async def track_system_metric(
        self,
        metric_name: str,
        metric_value: float,
        metric_unit: Optional[str] = None,
        component: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> SystemMetrics:
        """Track a system performance metric"""
        metric = SystemMetrics(
            metric_name=metric_name,
            metric_value=metric_value,
            metric_unit=metric_unit,
            component=component,
            extra_data=extra_data
        )
        
        self.db.add(metric)
        await self.db.commit()
        await self.db.refresh(metric)
        
        return metric
    
    # Analytics Queries
    async def get_user_activity_summary(
        self,
        user_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get user activity summary for a date range"""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Activity counts by type
        stmt = select(
            UserActivity.activity_type,
            func.count(UserActivity.id).label("count")
        ).where(
            and_(
                UserActivity.user_id == user_id,
                UserActivity.created_at >= start_date,
                UserActivity.created_at <= end_date
            )
        ).group_by(UserActivity.activity_type)
        
        result = await self.db.execute(stmt)
        activity_counts = {row.activity_type: row.count for row in result.fetchall()}
        
        # Total activities
        total_activities = sum(activity_counts.values())
        
        # Most active days
        stmt = select(
            func.date(UserActivity.created_at).label("date"),
            func.count(UserActivity.id).label("count")
        ).where(
            and_(
                UserActivity.user_id == user_id,
                UserActivity.created_at >= start_date,
                UserActivity.created_at <= end_date
            )
        ).group_by(func.date(UserActivity.created_at)).order_by(desc("count")).limit(5)
        
        result = await self.db.execute(stmt)
        active_days = [{"date": row.date.isoformat(), "count": row.count} for row in result.fetchall()]
        
        return {
            "user_id": str(user_id),
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "total_activities": total_activities,
            "activity_breakdown": activity_counts,
            "most_active_days": active_days
        }
    
    async def get_content_performance(
        self,
        content_type: str,
        content_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get content performance metrics"""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Metric summary
        stmt = select(
            ContentMetrics.metric_type,
            func.sum(ContentMetrics.metric_value).label("total"),
            func.avg(ContentMetrics.metric_value).label("average"),
            func.count(ContentMetrics.id).label("count")
        ).where(
            and_(
                ContentMetrics.content_type == content_type,
                ContentMetrics.content_id == content_id,
                ContentMetrics.date >= start_date,
                ContentMetrics.date <= end_date
            )
        ).group_by(ContentMetrics.metric_type)
        
        result = await self.db.execute(stmt)
        metrics = {}
        for row in result.fetchall():
            metrics[row.metric_type] = {
                "total": float(row.total),
                "average": float(row.average),
                "count": row.count
            }
        
        # Daily trends
        stmt = select(
            func.date(ContentMetrics.date).label("date"),
            ContentMetrics.metric_type,
            func.sum(ContentMetrics.metric_value).label("value")
        ).where(
            and_(
                ContentMetrics.content_type == content_type,
                ContentMetrics.content_id == content_id,
                ContentMetrics.date >= start_date,
                ContentMetrics.date <= end_date
            )
        ).group_by(
            func.date(ContentMetrics.date),
            ContentMetrics.metric_type
        ).order_by(func.date(ContentMetrics.date))
        
        result = await self.db.execute(stmt)
        daily_trends = {}
        for row in result.fetchall():
            date_str = row.date.isoformat()
            if date_str not in daily_trends:
                daily_trends[date_str] = {}
            daily_trends[date_str][row.metric_type] = float(row.value)
        
        return {
            "content_type": content_type,
            "content_id": str(content_id),
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "metrics_summary": metrics,
            "daily_trends": daily_trends
        }
    
    async def get_system_performance_summary(
        self,
        component: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get system performance metrics summary"""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(hours=24)
        if not end_date:
            end_date = datetime.utcnow()
        
        conditions = [
            SystemMetrics.timestamp >= start_date,
            SystemMetrics.timestamp <= end_date
        ]
        
        if component:
            conditions.append(SystemMetrics.component == component)
        
        # Metric summary
        stmt = select(
            SystemMetrics.metric_name,
            SystemMetrics.component,
            func.avg(SystemMetrics.metric_value).label("average"),
            func.min(SystemMetrics.metric_value).label("minimum"),
            func.max(SystemMetrics.metric_value).label("maximum"),
            func.count(SystemMetrics.id).label("count")
        ).where(and_(*conditions)).group_by(
            SystemMetrics.metric_name,
            SystemMetrics.component
        )
        
        result = await self.db.execute(stmt)
        metrics = {}
        for row in result.fetchall():
            key = f"{row.component or 'system'}:{row.metric_name}"
            metrics[key] = {
                "average": float(row.average),
                "minimum": float(row.minimum),
                "maximum": float(row.maximum),
                "count": row.count
            }
        
        return {
            "component": component,
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "metrics": metrics
        }
    
    # Batch operations for performance
    async def flush_cached_metrics(self):
        """Flush cached metrics from Redis to database"""
        redis = await self.get_redis()
        
        # Get all cached content metrics
        pattern = "content_metric:*"
        keys = await redis.keys(pattern)
        
        metrics_to_insert = []
        for key in keys:
            try:
                # Parse key: content_metric:type:id:metric_type
                parts = key.decode().split(":")
                if len(parts) == 4:
                    _, content_type, content_id, metric_type = parts
                    value = await redis.get(key)
                    
                    if value:
                        metrics_to_insert.append(ContentMetrics(
                            content_type=content_type,
                            content_id=UUID(content_id),
                            metric_type=metric_type,
                            metric_value=float(value)
                        ))
                        
                        # Delete the cached key
                        await redis.delete(key)
            except Exception as e:
                print(f"Error processing cached metric {key}: {e}")
        
        # Bulk insert
        if metrics_to_insert:
            self.db.add_all(metrics_to_insert)
            await self.db.commit()
        
        return len(metrics_to_insert)


# Performance monitoring decorator
def track_performance(component: str, metric_name: str):
    """Decorator to track function performance"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                success = True
            except Exception as e:
                success = False
                raise e
            finally:
                duration = (time.time() - start_time) * 1000  # Convert to milliseconds
                
                # Try to get analytics service from args (if it's a method)
                analytics_service = None
                for arg in args:
                    if hasattr(arg, 'db') and hasattr(arg, 'track_system_metric'):
                        analytics_service = arg
                        break
                
                if analytics_service:
                    try:
                        await analytics_service.track_system_metric(
                            metric_name=metric_name,
                            metric_value=duration,
                            metric_unit="ms",
                            component=component,
                            metadata={"success": success}
                        )
                    except Exception:
                        pass  # Don't fail the main operation
            
            return result
        return wrapper
    return decorator