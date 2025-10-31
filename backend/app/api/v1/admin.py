"""
Admin API endpoints for LemonNPie Backend API
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.db.database import get_db
from app.auth.dependencies import get_current_user, require_role, require_roles
from app.models.user import User
from app.models.enums import UserRole, ModerationStatus
from app.services.admin_service import AdminService
from app.services.performance_service import PerformanceService
from app.schemas.admin import (
    AdminDashboard, SystemMetrics, UserAnalytics, ContentAnalytics,
    UserListResponse, UserRoleUpdate, UserSuspension, UserActivation,
    ReviewModerationResponse, ModerationAction, BulkModerationAction,
    ReportListResponse, ReportResolution,
    AnalyticsDateRange, AnalyticsFilter
)
from app.auth.rate_limiter import limiter
from app.core.exceptions import LemonPieException

logger = structlog.get_logger(__name__)

router = APIRouter(tags=["admin"])


@router.get("/dashboard", response_model=AdminDashboard)
@limiter.limit("10/minute")
async def get_admin_dashboard(
    request: Request,
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MODERATOR)),
    db: AsyncSession = Depends(get_db)
):
    """
    Get complete admin dashboard with system metrics, analytics, and recent activity.
    
    Requires admin or moderator role.
    """
    try:
        admin_service = AdminService(db)
        dashboard = await admin_service.get_admin_dashboard()
        
        logger.info(
            "Admin dashboard accessed",
            admin_id=str(current_user.id),
            admin_role=current_user.role
        )
        
        return dashboard
    except LemonPieException:
        raise
    except Exception as e:
        logger.error("Failed to get admin dashboard", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve admin dashboard"
        )


@router.get("/metrics", response_model=SystemMetrics)
@limiter.limit("20/minute")
async def get_system_metrics(
    request,
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MODERATOR)),
    db: AsyncSession = Depends(get_db)
):
    """
    Get system-wide metrics including user counts, content stats, and activity metrics.
    
    Requires admin or moderator role.
    """
    try:
        admin_service = AdminService(db)
        metrics = await admin_service.get_system_metrics()
        
        logger.info(
            "System metrics accessed",
            admin_id=str(current_user.id)
        )
        
        return metrics
    except LemonPieException:
        raise
    except Exception as e:
        logger.error("Failed to get system metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve system metrics"
        )


@router.get("/analytics/users", response_model=UserAnalytics)
@limiter.limit("10/minute")
async def get_user_analytics(
    request,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user analytics including growth, activity patterns, and engagement metrics.
    
    Requires admin role.
    """
    try:
        date_range = None
        if start_date and end_date:
            try:
                date_range = AnalyticsDateRange(
                    start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
                    end_date=datetime.strptime(end_date, "%Y-%m-%d").date()
                )
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid date format. Use YYYY-MM-DD"
                )
        
        admin_service = AdminService(db)
        analytics = await admin_service.get_user_analytics(date_range)
        
        logger.info(
            "User analytics accessed",
            admin_id=str(current_user.id),
            date_range=f"{start_date} to {end_date}" if start_date and end_date else "default"
        )
        
        return analytics
    except LemonPieException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get user analytics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user analytics"
        )


@router.get("/analytics/content", response_model=ContentAnalytics)
@limiter.limit("10/minute")
async def get_content_analytics(
    request,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Get content analytics including review trends, rating distribution, and popular content.
    
    Requires admin role.
    """
    try:
        date_range = None
        if start_date and end_date:
            try:
                date_range = AnalyticsDateRange(
                    start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
                    end_date=datetime.strptime(end_date, "%Y-%m-%d").date()
                )
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid date format. Use YYYY-MM-DD"
                )
        
        admin_service = AdminService(db)
        analytics = await admin_service.get_content_analytics(date_range)
        
        logger.info(
            "Content analytics accessed",
            admin_id=str(current_user.id),
            date_range=f"{start_date} to {end_date}" if start_date and end_date else "default"
        )
        
        return analytics
    except LemonPieException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get content analytics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve content analytics"
        )


@router.get("/users", response_model=UserListResponse)
@limiter.limit("30/minute")
async def get_users_list(
    request,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    role: Optional[UserRole] = Query(None, description="Filter by user role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MODERATOR)),
    db: AsyncSession = Depends(get_db)
):
    """
    Get paginated list of users with filtering and sorting options.
    
    Requires admin or moderator role.
    """
    try:
        admin_service = AdminService(db)
        users_list = await admin_service.get_users_list(
            page=page,
            per_page=per_page,
            search=search,
            role=role,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        logger.info(
            "Users list accessed",
            admin_id=str(current_user.id),
            page=page,
            per_page=per_page,
            filters={"search": search, "role": role, "is_active": is_active}
        )
        
        return users_list
    except LemonPieException:
        raise
    except Exception as e:
        logger.error("Failed to get users list", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users list"
        )


@router.put("/users/{user_id}/role")
@limiter.limit("10/minute")
async def update_user_role(
    request,
    user_id: UUID,
    role_update: UserRoleUpdate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Update user role. Only admins can change user roles.
    
    Requires admin role.
    """
    try:
        # Prevent self-role modification
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot modify your own role"
            )
        
        admin_service = AdminService(db)
        success = await admin_service.update_user_role(
            user_id=user_id,
            new_role=role_update.role,
            admin_id=current_user.id
        )
        
        if success:
            logger.info(
                "User role updated",
                target_user_id=str(user_id),
                new_role=role_update.role,
                admin_id=str(current_user.id)
            )
            return {"message": "User role updated successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user role"
            )
    except LemonPieException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update user role", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user role"
        )


@router.post("/users/{user_id}/suspend")
@limiter.limit("5/minute")
async def suspend_user(
    request,
    user_id: UUID,
    suspension: UserSuspension,
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MODERATOR)),
    db: AsyncSession = Depends(get_db)
):
    """
    Suspend user account with optional duration.
    
    Requires admin or moderator role.
    """
    try:
        # Prevent self-suspension
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot suspend your own account"
            )
        
        admin_service = AdminService(db)
        success = await admin_service.suspend_user(
            user_id=user_id,
            reason=suspension.reason,
            duration_days=suspension.duration_days,
            admin_id=current_user.id
        )
        
        if success:
            logger.info(
                "User suspended",
                target_user_id=str(user_id),
                reason=suspension.reason,
                duration_days=suspension.duration_days,
                admin_id=str(current_user.id)
            )
            return {"message": "User suspended successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to suspend user"
            )
    except LemonPieException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to suspend user", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to suspend user"
        )


@router.post("/users/{user_id}/activate")
@limiter.limit("10/minute")
async def activate_user(
    request,
    user_id: UUID,
    activation: UserActivation,
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MODERATOR)),
    db: AsyncSession = Depends(get_db)
):
    """
    Activate suspended user account.
    
    Requires admin or moderator role.
    """
    try:
        admin_service = AdminService(db)
        success = await admin_service.activate_user(
            user_id=user_id,
            reason=activation.reason,
            admin_id=current_user.id
        )
        
        if success:
            logger.info(
                "User activated",
                target_user_id=str(user_id),
                reason=activation.reason,
                admin_id=str(current_user.id)
            )
            return {"message": "User activated successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to activate user"
            )
    except LemonPieException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to activate user", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate user"
        )


@router.get("/moderation/reviews", response_model=ReviewModerationResponse)
@limiter.limit("30/minute")
async def get_reviews_for_moderation(
    request,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[ModerationStatus] = Query(None, description="Filter by moderation status"),
    is_flagged: Optional[bool] = Query(None, description="Filter by flagged status"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MODERATOR)),
    db: AsyncSession = Depends(get_db)
):
    """
    Get reviews for moderation dashboard with filtering and sorting.
    
    Requires admin or moderator role.
    """
    try:
        admin_service = AdminService(db)
        reviews = await admin_service.get_reviews_for_moderation(
            page=page,
            per_page=per_page,
            status=status,
            is_flagged=is_flagged,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        logger.info(
            "Reviews moderation list accessed",
            admin_id=str(current_user.id),
            page=page,
            per_page=per_page,
            filters={"status": status, "is_flagged": is_flagged}
        )
        
        return reviews
    except LemonPieException:
        raise
    except Exception as e:
        logger.error("Failed to get reviews for moderation", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve reviews for moderation"
        )


@router.post("/moderation/reviews/{review_id}")
@limiter.limit("20/minute")
async def moderate_review(
    request,
    review_id: UUID,
    moderation: ModerationAction,
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MODERATOR)),
    db: AsyncSession = Depends(get_db)
):
    """
    Moderate a single review (approve, reject, or flag).
    
    Requires admin or moderator role.
    """
    try:
        admin_service = AdminService(db)
        success = await admin_service.moderate_review(
            review_id=review_id,
            action=moderation.action,
            reason=moderation.reason,
            admin_id=current_user.id
        )
        
        if success:
            logger.info(
                "Review moderated",
                review_id=str(review_id),
                action=moderation.action,
                admin_id=str(current_user.id)
            )
            return {"message": f"Review {moderation.action}ed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to moderate review"
            )
    except LemonPieException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to moderate review", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to moderate review"
        )


@router.post("/moderation/reviews/bulk")
@limiter.limit("10/minute")
async def bulk_moderate_reviews(
    request,
    bulk_moderation: BulkModerationAction,
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MODERATOR)),
    db: AsyncSession = Depends(get_db)
):
    """
    Moderate multiple reviews at once (approve, reject, or flag).
    
    Requires admin or moderator role.
    """
    try:
        admin_service = AdminService(db)
        moderated_count = await admin_service.bulk_moderate_reviews(
            review_ids=bulk_moderation.review_ids,
            action=bulk_moderation.action,
            reason=bulk_moderation.reason,
            admin_id=current_user.id
        )
        
        logger.info(
            "Bulk review moderation completed",
            review_count=moderated_count,
            action=bulk_moderation.action,
            admin_id=str(current_user.id)
        )
        
        return {
            "message": f"Successfully {bulk_moderation.action}ed {moderated_count} reviews",
            "moderated_count": moderated_count
        }
    except LemonPieException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to bulk moderate reviews", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to bulk moderate reviews"
        )


@router.get("/reports", response_model=ReportListResponse)
@limiter.limit("30/minute")
async def get_reports_list(
    request,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[ModerationStatus] = Query(None, description="Filter by report status"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MODERATOR)),
    db: AsyncSession = Depends(get_db)
):
    """
    Get paginated list of user reports with filtering and sorting.
    
    Requires admin or moderator role.
    """
    try:
        admin_service = AdminService(db)
        reports = await admin_service.get_reports_list(
            page=page,
            per_page=per_page,
            status=status,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        logger.info(
            "Reports list accessed",
            admin_id=str(current_user.id),
            page=page,
            per_page=per_page,
            filters={"status": status}
        )
        
        return reports
    except LemonPieException:
        raise
    except Exception as e:
        logger.error("Failed to get reports list", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve reports list"
        )


@router.post("/reports/{report_id}/resolve")
@limiter.limit("10/minute")
async def resolve_report(
    request,
    report_id: UUID,
    resolution: ReportResolution,
    current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MODERATOR)),
    db: AsyncSession = Depends(get_db)
):
    """
    Resolve a user report with appropriate action.
    
    Requires admin or moderator role.
    """
    try:
        admin_service = AdminService(db)
        success = await admin_service.resolve_report(
            report_id=report_id,
            action=resolution.action,
            reason=resolution.reason,
            admin_id=current_user.id,
            notify_reporter=resolution.notify_reporter,
            notify_reported=resolution.notify_reported
        )
        
        if success:
            logger.info(
                "Report resolved",
                report_id=str(report_id),
                action=resolution.action,
                admin_id=str(current_user.id)
            )
            return {"message": f"Report resolved with action: {resolution.action}"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to resolve report"
            )
    except LemonPieException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to resolve report", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resolve report"
        )

# Performance and Optimization Endpoints

@router.get("/performance/metrics")
@limiter.limit("10/minute")
async def get_performance_metrics(
    request,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Get comprehensive performance metrics for the application.
    
    Requires admin role.
    """
    try:
        performance_service = PerformanceService()
        metrics = await performance_service.get_performance_metrics()
        
        logger.info(
            "Performance metrics accessed",
            admin_id=str(current_user.id)
        )
        
        return metrics
    except Exception as e:
        logger.error("Failed to get performance metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve performance metrics"
        )


@router.post("/performance/optimize-database")
@limiter.limit("2/hour")
async def optimize_database(
    request,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Run database optimization tasks including index creation and table analysis.
    
    Requires admin role. Limited to 2 requests per hour.
    """
    try:
        performance_service = PerformanceService()
        results = await performance_service.optimize_database()
        
        logger.info(
            "Database optimization executed",
            admin_id=str(current_user.id),
            results=results
        )
        
        return {
            "message": "Database optimization completed",
            "results": results
        }
    except Exception as e:
        logger.error("Failed to optimize database", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to optimize database"
        )


@router.get("/performance/cache-stats")
@limiter.limit("20/minute")
async def get_cache_statistics(
    request,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed cache statistics and usage information.
    
    Requires admin role.
    """
    try:
        performance_service = PerformanceService()
        stats = await performance_service.get_cache_statistics()
        
        logger.info(
            "Cache statistics accessed",
            admin_id=str(current_user.id)
        )
        
        return stats
    except Exception as e:
        logger.error("Failed to get cache statistics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve cache statistics"
        )


@router.delete("/performance/cache/{pattern}")
@limiter.limit("10/minute")
async def clear_cache_pattern(
    request,
    pattern: str,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Clear cache entries matching a specific pattern.
    
    Requires admin role.
    
    Common patterns:
    - movie:* - Clear all movie cache
    - user:* - Clear all user cache
    - search:* - Clear all search cache
    """
    try:
        performance_service = PerformanceService()
        deleted_count = await performance_service.clear_cache_by_pattern(pattern)
        
        logger.info(
            "Cache pattern cleared",
            admin_id=str(current_user.id),
            pattern=pattern,
            deleted_count=deleted_count
        )
        
        return {
            "message": f"Cleared {deleted_count} cache entries matching pattern: {pattern}",
            "deleted_count": deleted_count
        }
    except Exception as e:
        logger.error("Failed to clear cache pattern", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear cache pattern"
        )


@router.post("/performance/warm-cache")
@limiter.limit("5/hour")
async def warm_cache(
    request,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Warm up cache with frequently accessed data.
    
    Requires admin role. Limited to 5 requests per hour.
    """
    try:
        performance_service = PerformanceService()
        results = await performance_service.warm_cache()
        
        logger.info(
            "Cache warming executed",
            admin_id=str(current_user.id),
            results=results
        )
        
        return {
            "message": "Cache warming completed",
            "results": results
        }
    except Exception as e:
        logger.error("Failed to warm cache", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to warm cache"
        )


@router.get("/performance/slow-endpoints")
@limiter.limit("10/minute")
async def get_slow_endpoints(
    request,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze and return slow API endpoints based on database query performance.
    
    Requires admin role.
    """
    try:
        performance_service = PerformanceService()
        slow_endpoints = await performance_service.analyze_slow_endpoints(db)
        
        logger.info(
            "Slow endpoints analysis accessed",
            admin_id=str(current_user.id)
        )
        
        return {
            "slow_endpoints": slow_endpoints,
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error("Failed to analyze slow endpoints", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze slow endpoints"
        )


@router.post("/performance/analyze-query")
@limiter.limit("10/minute")
async def analyze_query_performance(
    request,
    query: str,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze the performance of a specific SQL query and get optimization suggestions.
    
    Requires admin role.
    """
    try:
        performance_service = PerformanceService()
        analysis = await performance_service.optimize_query_plan(query, db)
        
        logger.info(
            "Query analysis performed",
            admin_id=str(current_user.id),
            query_length=len(query)
        )
        
        return analysis
    except Exception as e:
        logger.error("Failed to analyze query", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze query performance"
        )
