"""
Analytics reporting service for generating comprehensive reports
"""
import csv
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from uuid import UUID
from io import StringIO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc, asc, text
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
from app.schemas.analytics import (
    UserEngagementReport,
    ContentPopularityReport,
    SystemHealthReport,
    AnalyticsDashboard
)


class AnalyticsReportingService:
    """Service for generating analytics reports and insights"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def generate_user_engagement_report(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> UserEngagementReport:
        """Generate comprehensive user engagement report"""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Total and active users
        total_users_stmt = select(func.count(User.id)).where(
            User.created_at <= end_date
        )
        total_users_result = await self.db.execute(total_users_stmt)
        total_users = total_users_result.scalar()
        
        # Active users (users with activity in the period)
        active_users_stmt = select(func.count(func.distinct(UserActivity.user_id))).where(
            and_(
                UserActivity.created_at >= start_date,
                UserActivity.created_at <= end_date,
                UserActivity.user_id.isnot(None)
            )
        )
        active_users_result = await self.db.execute(active_users_stmt)
        active_users = active_users_result.scalar() or 0
        
        # New users in period
        new_users_stmt = select(func.count(User.id)).where(
            and_(
                User.created_at >= start_date,
                User.created_at <= end_date
            )
        )
        new_users_result = await self.db.execute(new_users_stmt)
        new_users = new_users_result.scalar() or 0
        
        # User retention rate (users active in both current and previous period)
        previous_start = start_date - (end_date - start_date)
        retention_stmt = text("""
            SELECT COUNT(DISTINCT current_active.user_id) * 100.0 / NULLIF(COUNT(DISTINCT previous_active.user_id), 0) as retention_rate
            FROM (
                SELECT DISTINCT user_id 
                FROM user_activities 
                WHERE created_at >= :prev_start AND created_at < :start_date AND user_id IS NOT NULL
            ) previous_active
            FULL OUTER JOIN (
                SELECT DISTINCT user_id 
                FROM user_activities 
                WHERE created_at >= :start_date AND created_at <= :end_date AND user_id IS NOT NULL
            ) current_active ON previous_active.user_id = current_active.user_id
        """)
        retention_result = await self.db.execute(retention_stmt, {
            "prev_start": previous_start,
            "start_date": start_date,
            "end_date": end_date
        })
        retention_rate = retention_result.scalar() or 0.0
        
        # Average session duration
        avg_session_stmt = select(func.avg(UserEngagementMetrics.session_duration_minutes)).where(
            and_(
                UserEngagementMetrics.date >= start_date,
                UserEngagementMetrics.date <= end_date
            )
        )
        avg_session_result = await self.db.execute(avg_session_stmt)
        avg_session_duration = avg_session_result.scalar() or 0.0
        
        # Top activities
        top_activities_stmt = select(
            UserActivity.activity_type,
            func.count(UserActivity.id).label("count")
        ).where(
            and_(
                UserActivity.created_at >= start_date,
                UserActivity.created_at <= end_date
            )
        ).group_by(UserActivity.activity_type).order_by(desc("count")).limit(10)
        
        top_activities_result = await self.db.execute(top_activities_stmt)
        top_activities = [
            {"activity_type": row.activity_type, "count": row.count}
            for row in top_activities_result.fetchall()
        ]
        
        # Daily engagement trends
        daily_trends_stmt = select(
            func.date(UserActivity.created_at).label("date"),
            func.count(func.distinct(UserActivity.user_id)).label("active_users"),
            func.count(UserActivity.id).label("total_activities")
        ).where(
            and_(
                UserActivity.created_at >= start_date,
                UserActivity.created_at <= end_date,
                UserActivity.user_id.isnot(None)
            )
        ).group_by(func.date(UserActivity.created_at)).order_by(func.date(UserActivity.created_at))
        
        daily_trends_result = await self.db.execute(daily_trends_stmt)
        engagement_trends = {}
        for row in daily_trends_result.fetchall():
            date_str = row.date.isoformat()
            engagement_trends[date_str] = {
                "active_users": row.active_users,
                "total_activities": row.total_activities
            }
        
        return UserEngagementReport(
            period={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            total_users=total_users,
            active_users=active_users,
            new_users=new_users,
            user_retention_rate=float(retention_rate),
            average_session_duration=float(avg_session_duration),
            top_activities=top_activities,
            engagement_trends=engagement_trends
        )
    
    async def generate_content_popularity_report(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> ContentPopularityReport:
        """Generate content popularity and performance report"""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Total content count
        total_content_stmt = select(func.count(Movie.id))
        total_content_result = await self.db.execute(total_content_stmt)
        total_content = total_content_result.scalar()
        
        # Most viewed content
        most_viewed_stmt = text("""
            SELECT 
                m.id,
                m.title,
                m.release_date,
                COALESCE(SUM(cm.metric_value), 0) as total_views
            FROM movies m
            LEFT JOIN content_metrics cm ON m.id = cm.content_id 
                AND cm.content_type = 'movie' 
                AND cm.metric_type = 'views'
                AND cm.date >= :start_date 
                AND cm.date <= :end_date
            GROUP BY m.id, m.title, m.release_date
            ORDER BY total_views DESC
            LIMIT 10
        """)
        most_viewed_result = await self.db.execute(most_viewed_stmt, {
            "start_date": start_date,
            "end_date": end_date
        })
        most_viewed_content = [
            {
                "id": str(row.id),
                "title": row.title,
                "release_date": row.release_date.isoformat() if row.release_date else None,
                "total_views": int(row.total_views)
            }
            for row in most_viewed_result.fetchall()
        ]
        
        # Content performance metrics
        performance_stmt = select(
            ContentMetrics.metric_type,
            func.sum(ContentMetrics.metric_value).label("total"),
            func.avg(ContentMetrics.metric_value).label("average"),
            func.count(ContentMetrics.id).label("count")
        ).where(
            and_(
                ContentMetrics.date >= start_date,
                ContentMetrics.date <= end_date
            )
        ).group_by(ContentMetrics.metric_type)
        
        performance_result = await self.db.execute(performance_stmt)
        content_performance = {}
        for row in performance_result.fetchall():
            content_performance[row.metric_type] = {
                "total": float(row.total),
                "average": float(row.average),
                "count": row.count
            }
        
        # Trending content (high recent activity)
        trending_stmt = text("""
            SELECT 
                m.id,
                m.title,
                m.release_date,
                COUNT(DISTINCT ua.user_id) as unique_viewers,
                COUNT(ua.id) as total_interactions
            FROM movies m
            JOIN user_activities ua ON m.id = ua.resource_id 
                AND ua.resource_type = 'movie'
                AND ua.created_at >= :recent_start
                AND ua.created_at <= :end_date
            GROUP BY m.id, m.title, m.release_date
            HAVING COUNT(ua.id) > 5
            ORDER BY total_interactions DESC, unique_viewers DESC
            LIMIT 10
        """)
        recent_start = end_date - timedelta(days=7)  # Last 7 days for trending
        trending_result = await self.db.execute(trending_stmt, {
            "recent_start": recent_start,
            "end_date": end_date
        })
        trending_content = [
            {
                "id": str(row.id),
                "title": row.title,
                "release_date": row.release_date.isoformat() if row.release_date else None,
                "unique_viewers": row.unique_viewers,
                "total_interactions": row.total_interactions
            }
            for row in trending_result.fetchall()
        ]
        
        # Content engagement rates (reviews per view)
        engagement_rates_stmt = text("""
            SELECT 
                'movies' as content_type,
                COALESCE(
                    COUNT(DISTINCT r.id) * 100.0 / NULLIF(SUM(CASE WHEN cm.metric_type = 'views' THEN cm.metric_value ELSE 0 END), 0),
                    0
                ) as engagement_rate
            FROM movies m
            LEFT JOIN reviews r ON m.id = r.movie_id 
                AND r.created_at >= :start_date 
                AND r.created_at <= :end_date
            LEFT JOIN content_metrics cm ON m.id = cm.content_id 
                AND cm.content_type = 'movie'
                AND cm.date >= :start_date 
                AND cm.date <= :end_date
        """)
        engagement_rates_result = await self.db.execute(engagement_rates_stmt, {
            "start_date": start_date,
            "end_date": end_date
        })
        content_engagement_rates = {}
        for row in engagement_rates_result.fetchall():
            content_engagement_rates[row.content_type] = float(row.engagement_rate)
        
        return ContentPopularityReport(
            period={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            total_content=total_content,
            most_viewed_content=most_viewed_content,
            content_performance=content_performance,
            trending_content=trending_content,
            content_engagement_rates=content_engagement_rates
        )
    
    async def generate_system_health_report(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> SystemHealthReport:
        """Generate system health and performance report"""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(hours=24)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Component health metrics
        component_health_stmt = select(
            SystemMetrics.component,
            SystemMetrics.metric_name,
            func.avg(SystemMetrics.metric_value).label("average"),
            func.min(SystemMetrics.metric_value).label("minimum"),
            func.max(SystemMetrics.metric_value).label("maximum")
        ).where(
            and_(
                SystemMetrics.timestamp >= start_date,
                SystemMetrics.timestamp <= end_date,
                SystemMetrics.component.isnot(None)
            )
        ).group_by(SystemMetrics.component, SystemMetrics.metric_name)
        
        component_health_result = await self.db.execute(component_health_stmt)
        component_health = {}
        for row in component_health_result.fetchall():
            if row.component not in component_health:
                component_health[row.component] = {}
            component_health[row.component][row.metric_name] = {
                "average": float(row.average),
                "minimum": float(row.minimum),
                "maximum": float(row.maximum)
            }
        
        # Performance metrics summary
        performance_stmt = select(
            SystemMetrics.metric_name,
            func.avg(SystemMetrics.metric_value).label("average"),
            func.percentile_cont(0.95).within_group(SystemMetrics.metric_value).label("p95"),
            func.percentile_cont(0.99).within_group(SystemMetrics.metric_value).label("p99")
        ).where(
            and_(
                SystemMetrics.timestamp >= start_date,
                SystemMetrics.timestamp <= end_date
            )
        ).group_by(SystemMetrics.metric_name)
        
        performance_result = await self.db.execute(performance_stmt)
        performance_metrics = {}
        for row in performance_result.fetchall():
            performance_metrics[row.metric_name] = {
                "average": float(row.average),
                "p95": float(row.p95) if row.p95 else 0.0,
                "p99": float(row.p99) if row.p99 else 0.0
            }
        
        # Error rates (from system metrics with success=false)
        error_rates_stmt = text("""
            SELECT 
                component,
                COUNT(CASE WHEN extra_data->>'success' = 'false' THEN 1 END) * 100.0 / COUNT(*) as error_rate
            FROM system_metrics 
            WHERE timestamp >= :start_date 
                AND timestamp <= :end_date 
                AND extra_data IS NOT NULL
                AND component IS NOT NULL
            GROUP BY component
        """)
        error_rates_result = await self.db.execute(error_rates_stmt, {
            "start_date": start_date,
            "end_date": end_date
        })
        error_rates = {}
        for row in error_rates_result.fetchall():
            error_rates[row.component] = float(row.error_rate)
        
        # Calculate overall health score (0-100)
        # Based on response times, error rates, and system availability
        health_score = 100.0
        
        # Penalize for high response times
        if "response_time" in performance_metrics:
            avg_response_time = performance_metrics["response_time"]["average"]
            if avg_response_time > 1000:  # > 1 second
                health_score -= min(30, (avg_response_time - 1000) / 100)
        
        # Penalize for high error rates
        avg_error_rate = sum(error_rates.values()) / len(error_rates) if error_rates else 0
        health_score -= min(40, avg_error_rate)
        
        health_score = max(0, health_score)
        
        # Calculate uptime percentage
        total_time_hours = (end_date - start_date).total_seconds() / 3600
        # Assume system is up if we have metrics
        uptime_percentage = 100.0 if total_time_hours > 0 else 0.0
        
        return SystemHealthReport(
            period={
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            overall_health_score=health_score,
            component_health=component_health,
            performance_metrics=performance_metrics,
            error_rates=error_rates,
            uptime_percentage=uptime_percentage
        )
    
    async def generate_dashboard_data(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> AnalyticsDashboard:
        """Generate comprehensive dashboard data"""
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=7)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Generate all reports
        user_engagement = await self.generate_user_engagement_report(start_date, end_date)
        content_performance = await self.generate_content_popularity_report(start_date, end_date)
        system_health = await self.generate_system_health_report(start_date, end_date)
        
        # Overview metrics
        overview = {
            "total_users": user_engagement.total_users,
            "active_users": user_engagement.active_users,
            "total_content": content_performance.total_content,
            "system_health_score": system_health.overall_health_score,
            "user_retention_rate": user_engagement.user_retention_rate,
            "average_session_duration": user_engagement.average_session_duration
        }
        
        # Recent activities
        recent_activities_stmt = select(UserActivity).options(
            selectinload(UserActivity.user)
        ).where(
            UserActivity.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).order_by(desc(UserActivity.created_at)).limit(20)
        
        recent_activities_result = await self.db.execute(recent_activities_stmt)
        recent_activities = recent_activities_result.scalars().all()
        
        # Generate alerts based on thresholds
        alerts = []
        
        # High error rate alert
        avg_error_rate = sum(system_health.error_rates.values()) / len(system_health.error_rates) if system_health.error_rates else 0
        if avg_error_rate > 5:
            alerts.append({
                "type": "error",
                "message": f"High error rate detected: {avg_error_rate:.1f}%",
                "severity": "high" if avg_error_rate > 10 else "medium"
            })
        
        # Low user engagement alert
        if user_engagement.active_users < user_engagement.total_users * 0.1:
            alerts.append({
                "type": "warning",
                "message": f"Low user engagement: only {user_engagement.active_users} of {user_engagement.total_users} users active",
                "severity": "medium"
            })
        
        # System performance alert
        if system_health.overall_health_score < 80:
            alerts.append({
                "type": "error",
                "message": f"System health score is low: {system_health.overall_health_score:.1f}%",
                "severity": "high" if system_health.overall_health_score < 60 else "medium"
            })
        
        return AnalyticsDashboard(
            overview=overview,
            user_engagement=user_engagement,
            content_performance=content_performance,
            system_health=system_health,
            recent_activities=[
                {
                    "id": str(activity.id),
                    "user_id": str(activity.user_id) if activity.user_id else None,
                    "activity_type": activity.activity_type,
                    "resource_type": activity.resource_type,
                    "resource_id": str(activity.resource_id) if activity.resource_id else None,
                    "created_at": activity.created_at.isoformat()
                }
                for activity in recent_activities
            ],
            alerts=alerts
        )
    
    async def export_report_to_csv(self, report_data: Dict[str, Any], report_type: str) -> str:
        """Export report data to CSV format"""
        output = StringIO()
        
        if report_type == "user_engagement":
            writer = csv.writer(output)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Total Users", report_data.get("total_users", 0)])
            writer.writerow(["Active Users", report_data.get("active_users", 0)])
            writer.writerow(["New Users", report_data.get("new_users", 0)])
            writer.writerow(["Retention Rate (%)", report_data.get("user_retention_rate", 0)])
            writer.writerow(["Avg Session Duration (min)", report_data.get("average_session_duration", 0)])
            
            writer.writerow([])
            writer.writerow(["Top Activities"])
            writer.writerow(["Activity Type", "Count"])
            for activity in report_data.get("top_activities", []):
                writer.writerow([activity["activity_type"], activity["count"]])
        
        elif report_type == "content_performance":
            writer = csv.writer(output)
            writer.writerow(["Most Viewed Content"])
            writer.writerow(["Title", "Release Date", "Total Views"])
            for content in report_data.get("most_viewed_content", []):
                writer.writerow([content["title"], content["release_date"], content["total_views"]])
            
            writer.writerow([])
            writer.writerow(["Trending Content"])
            writer.writerow(["Title", "Unique Viewers", "Total Interactions"])
            for content in report_data.get("trending_content", []):
                writer.writerow([content["title"], content["unique_viewers"], content["total_interactions"]])
        
        elif report_type == "system_health":
            writer = csv.writer(output)
            writer.writerow(["System Health Metrics"])
            writer.writerow(["Overall Health Score", report_data.get("overall_health_score", 0)])
            writer.writerow(["Uptime Percentage", report_data.get("uptime_percentage", 0)])
            
            writer.writerow([])
            writer.writerow(["Performance Metrics"])
            writer.writerow(["Metric", "Average", "P95", "P99"])
            for metric, values in report_data.get("performance_metrics", {}).items():
                writer.writerow([metric, values["average"], values["p95"], values["p99"]])
        
        return output.getvalue()
    
    async def save_report(
        self,
        report_type: str,
        report_name: str,
        report_data: Dict[str, Any],
        generated_by: UUID,
        description: Optional[str] = None,
        format: str = "json",
        is_public: bool = False,
        expires_at: Optional[datetime] = None
    ) -> AnalyticsReport:
        """Save a generated report to the database"""
        report = AnalyticsReport(
            report_type=report_type,
            report_name=report_name,
            description=description,
            data=report_data,
            format=format,
            generated_by=generated_by,
            is_public=is_public,
            expires_at=expires_at
        )
        
        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)
        
        return report