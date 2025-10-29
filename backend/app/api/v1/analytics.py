"""
Analytics API endpoints for LemonNPie Backend
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc

from app.db.database import get_db
from app.auth.dependencies import get_current_user, get_current_admin_user
from app.models.user import User
from app.models.analytics import AnalyticsReport, UserActivity, ContentMetrics, SystemMetrics
from app.services.analytics_service import AnalyticsService
from app.services.analytics_reporting_service import AnalyticsReportingService
from app.schemas.analytics import (
    UserActivityCreate,
    UserActivityResponse,
    ContentMetricCreate,
    ContentMetricResponse,
    SystemMetricCreate,
    SystemMetricResponse,
    UserActivitySummary,
    ContentPerformance,
    SystemPerformanceSummary,
    UserEngagementReport,
    ContentPopularityReport,
    SystemHealthReport,
    AnalyticsDashboard,
    AnalyticsReportCreate,
    AnalyticsReportResponse,
    AnalyticsFilters
)

router = APIRouter(tags=["analytics"])


# User Activity Endpoints
@router.post("/activities", response_model=UserActivityResponse)
async def track_user_activity(
    activity: UserActivityCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Track a user activity event"""
    analytics_service = AnalyticsService(db)
    
    tracked_activity = await analytics_service.track_user_activity(
        user_id=current_user.id,
        activity_type=activity.activity_type,
        resource_type=activity.resource_type,
        resource_id=activity.resource_id,
        extra_data=activity.extra_data,
        session_id=activity.session_id,
        ip_address=activity.ip_address,
        user_agent=activity.user_agent
    )
    
    return tracked_activity


@router.get("/activities", response_model=List[UserActivityResponse])
async def get_user_activities(
    filters: AnalyticsFilters = Depends(),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user activities with filtering"""
    conditions = [UserActivity.user_id == current_user.id]
    
    if filters.start_date:
        conditions.append(UserActivity.created_at >= filters.start_date)
    if filters.end_date:
        conditions.append(UserActivity.created_at <= filters.end_date)
    if filters.activity_type:
        conditions.append(UserActivity.activity_type == filters.activity_type)
    if filters.resource_type:
        conditions.append(UserActivity.resource_type == filters.resource_type)
    if filters.resource_id:
        conditions.append(UserActivity.resource_id == filters.resource_id)
    
    stmt = select(UserActivity).where(
        and_(*conditions)
    ).order_by(desc(UserActivity.created_at)).limit(filters.limit).offset(filters.offset)
    
    result = await db.execute(stmt)
    activities = result.scalars().all()
    
    return activities


@router.get("/activities/summary", response_model=UserActivitySummary)
async def get_user_activity_summary(
    start_date: Optional[datetime] = Query(None, description="Start date for summary"),
    end_date: Optional[datetime] = Query(None, description="End date for summary"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user activity summary"""
    analytics_service = AnalyticsService(db)
    
    summary = await analytics_service.get_user_activity_summary(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date
    )
    
    return UserActivitySummary(**summary)


# Content Metrics Endpoints
@router.post("/content-metrics", response_model=ContentMetricResponse)
async def track_content_metric(
    metric: ContentMetricCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Track a content performance metric"""
    analytics_service = AnalyticsService(db)
    
    tracked_metric = await analytics_service.track_content_metric(
        content_type=metric.content_type,
        content_id=metric.content_id,
        metric_type=metric.metric_type,
        metric_value=metric.metric_value,
        extra_data=metric.extra_data
    )
    
    return tracked_metric


@router.get("/content-metrics/{content_type}/{content_id}", response_model=ContentPerformance)
async def get_content_performance(
    content_type: str,
    content_id: UUID,
    start_date: Optional[datetime] = Query(None, description="Start date for metrics"),
    end_date: Optional[datetime] = Query(None, description="End date for metrics"),
    db: AsyncSession = Depends(get_db)
):
    """Get content performance metrics"""
    analytics_service = AnalyticsService(db)
    
    performance = await analytics_service.get_content_performance(
        content_type=content_type,
        content_id=content_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return ContentPerformance(**performance)


# Admin Analytics Endpoints
@router.post("/system-metrics", response_model=SystemMetricResponse)
async def track_system_metric(
    metric: SystemMetricCreate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Track a system performance metric (Admin only)"""
    analytics_service = AnalyticsService(db)
    
    tracked_metric = await analytics_service.track_system_metric(
        metric_name=metric.metric_name,
        metric_value=metric.metric_value,
        metric_unit=metric.metric_unit,
        component=metric.component,
        extra_data=metric.extra_data
    )
    
    return tracked_metric


@router.get("/system-performance", response_model=SystemPerformanceSummary)
async def get_system_performance(
    component: Optional[str] = Query(None, description="Filter by component"),
    start_date: Optional[datetime] = Query(None, description="Start date for metrics"),
    end_date: Optional[datetime] = Query(None, description="End date for metrics"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get system performance summary (Admin only)"""
    analytics_service = AnalyticsService(db)
    
    performance = await analytics_service.get_system_performance_summary(
        component=component,
        start_date=start_date,
        end_date=end_date
    )
    
    return SystemPerformanceSummary(**performance)


# Reporting Endpoints
@router.get("/reports/user-engagement", response_model=UserEngagementReport)
async def get_user_engagement_report(
    start_date: Optional[datetime] = Query(None, description="Start date for report"),
    end_date: Optional[datetime] = Query(None, description="End date for report"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate user engagement report (Admin only)"""
    reporting_service = AnalyticsReportingService(db)
    
    report = await reporting_service.generate_user_engagement_report(
        start_date=start_date,
        end_date=end_date
    )
    
    return report


@router.get("/reports/content-popularity", response_model=ContentPopularityReport)
async def get_content_popularity_report(
    start_date: Optional[datetime] = Query(None, description="Start date for report"),
    end_date: Optional[datetime] = Query(None, description="End date for report"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate content popularity report (Admin only)"""
    reporting_service = AnalyticsReportingService(db)
    
    report = await reporting_service.generate_content_popularity_report(
        start_date=start_date,
        end_date=end_date
    )
    
    return report


@router.get("/reports/system-health", response_model=SystemHealthReport)
async def get_system_health_report(
    start_date: Optional[datetime] = Query(None, description="Start date for report"),
    end_date: Optional[datetime] = Query(None, description="End date for report"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate system health report (Admin only)"""
    reporting_service = AnalyticsReportingService(db)
    
    report = await reporting_service.generate_system_health_report(
        start_date=start_date,
        end_date=end_date
    )
    
    return report


@router.get("/dashboard", response_model=AnalyticsDashboard)
async def get_analytics_dashboard(
    start_date: Optional[datetime] = Query(None, description="Start date for dashboard"),
    end_date: Optional[datetime] = Query(None, description="End date for dashboard"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get comprehensive analytics dashboard (Admin only)"""
    reporting_service = AnalyticsReportingService(db)
    
    dashboard = await reporting_service.generate_dashboard_data(
        start_date=start_date,
        end_date=end_date
    )
    
    return dashboard


# Report Management Endpoints
@router.post("/reports", response_model=AnalyticsReportResponse)
async def create_analytics_report(
    report_request: AnalyticsReportCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Create and save an analytics report (Admin only)"""
    reporting_service = AnalyticsReportingService(db)
    
    # Generate report data based on type
    report_data = {}
    if report_request.report_type == "user_engagement":
        start_date = report_request.parameters.get("start_date") if report_request.parameters else None
        end_date = report_request.parameters.get("end_date") if report_request.parameters else None
        if start_date:
            start_date = datetime.fromisoformat(start_date)
        if end_date:
            end_date = datetime.fromisoformat(end_date)
        
        report = await reporting_service.generate_user_engagement_report(start_date, end_date)
        report_data = report.dict()
    
    elif report_request.report_type == "content_popularity":
        start_date = report_request.parameters.get("start_date") if report_request.parameters else None
        end_date = report_request.parameters.get("end_date") if report_request.parameters else None
        if start_date:
            start_date = datetime.fromisoformat(start_date)
        if end_date:
            end_date = datetime.fromisoformat(end_date)
        
        report = await reporting_service.generate_content_popularity_report(start_date, end_date)
        report_data = report.dict()
    
    elif report_request.report_type == "system_health":
        start_date = report_request.parameters.get("start_date") if report_request.parameters else None
        end_date = report_request.parameters.get("end_date") if report_request.parameters else None
        if start_date:
            start_date = datetime.fromisoformat(start_date)
        if end_date:
            end_date = datetime.fromisoformat(end_date)
        
        report = await reporting_service.generate_system_health_report(start_date, end_date)
        report_data = report.dict()
    
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")
    
    # Save report
    saved_report = await reporting_service.save_report(
        report_type=report_request.report_type,
        report_name=report_request.report_name,
        report_data=report_data,
        generated_by=current_user.id,
        description=report_request.description,
        format=report_request.format,
        is_public=report_request.is_public,
        expires_at=datetime.utcnow() + timedelta(days=30)  # Default 30 days expiry
    )
    
    return saved_report


@router.get("/reports", response_model=List[AnalyticsReportResponse])
async def get_analytics_reports(
    report_type: Optional[str] = Query(None, description="Filter by report type"),
    limit: int = Query(20, ge=1, le=100, description="Limit results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Get saved analytics reports (Admin only)"""
    conditions = []
    
    if report_type:
        conditions.append(AnalyticsReport.report_type == report_type)
    
    # Show all reports for admins, only public reports for others
    if current_user.role.value != "admin":
        conditions.append(AnalyticsReport.is_public == True)
    
    stmt = select(AnalyticsReport).where(
        and_(*conditions) if conditions else True
    ).order_by(desc(AnalyticsReport.generated_at)).limit(limit).offset(offset)
    
    result = await db.execute(stmt)
    reports = result.scalars().all()
    
    return reports


@router.get("/reports/{report_id}", response_model=AnalyticsReportResponse)
async def get_analytics_report(
    report_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific analytics report"""
    stmt = select(AnalyticsReport).where(AnalyticsReport.id == report_id)
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Check permissions
    if not report.is_public and report.generated_by != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    return report


@router.get("/reports/{report_id}/export")
async def export_analytics_report(
    report_id: UUID,
    format: str = Query("csv", description="Export format (csv, json)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Export analytics report in specified format"""
    stmt = select(AnalyticsReport).where(AnalyticsReport.id == report_id)
    result = await db.execute(stmt)
    report = result.scalar_one_or_none()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Check permissions
    if not report.is_public and report.generated_by != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    if format.lower() == "csv":
        reporting_service = AnalyticsReportingService(db)
        csv_content = await reporting_service.export_report_to_csv(report.data, report.report_type)
        
        from fastapi.responses import Response
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={report.report_name}.csv"}
        )
    
    elif format.lower() == "json":
        from fastapi.responses import JSONResponse
        return JSONResponse(
            content=report.data,
            headers={"Content-Disposition": f"attachment; filename={report.report_name}.json"}
        )
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported export format")


# Utility Endpoints
@router.post("/flush-metrics")
async def flush_cached_metrics(
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Flush cached metrics from Redis to database (Admin only)"""
    analytics_service = AnalyticsService(db)
    
    flushed_count = await analytics_service.flush_cached_metrics()
    
    return {"message": f"Flushed {flushed_count} cached metrics to database"}


@router.get("/health")
async def analytics_health_check():
    """Health check endpoint for analytics service"""
    return {
        "status": "healthy",
        "service": "analytics",
        "timestamp": datetime.utcnow().isoformat()
    }