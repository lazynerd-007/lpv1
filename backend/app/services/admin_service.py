"""
Admin service for LemonNPie Backend API
"""
from datetime import datetime, timedelta, date
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID
from sqlalchemy import func, and_, or_, desc, asc, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
import structlog

from app.models.user import User
from app.models.movie import Movie
from app.models.review import Review
from app.models.moderation import UserReport, Notification
from app.models.relationships import UserFollow, UserWatchlist, UserFavorite, ReviewVote
from app.models.enums import UserRole, ModerationStatus, VoteType
from app.schemas.admin import (
    SystemMetrics, UserAnalytics, ContentAnalytics, AdminDashboard,
    UserListItem, UserListResponse, ReviewModerationItem, ReviewModerationResponse,
    ReportItem, ReportListResponse, AnalyticsDateRange, AnalyticsFilter
)
from app.core.exceptions import LemonPieException

logger = structlog.get_logger(__name__)


class AdminService:
    """Service for admin panel functionality"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_system_metrics(self) -> SystemMetrics:
        """Get system-wide metrics for admin dashboard"""
        try:
            now = datetime.utcnow()
            today = now.date()
            week_ago = today - timedelta(days=7)
            month_ago = today - timedelta(days=30)
            
            # Basic counts
            total_users = await self._count_records(User)
            total_movies = await self._count_records(Movie)
            total_reviews = await self._count_records(Review)
            total_reports = await self._count_records(UserReport)
            
            # Active users (users who logged in or created content)
            active_users_today = await self._count_active_users(today, today)
            active_users_week = await self._count_active_users(week_ago, today)
            active_users_month = await self._count_active_users(month_ago, today)
            
            # New users
            new_users_today = await self._count_new_users(today, today)
            new_users_week = await self._count_new_users(week_ago, today)
            new_users_month = await self._count_new_users(month_ago, today)
            
            # Reviews
            reviews_today = await self._count_reviews_by_date(today, today)
            reviews_week = await self._count_reviews_by_date(week_ago, today)
            reviews_month = await self._count_reviews_by_date(month_ago, today)
            
            # Moderation
            pending_reports = await self._count_pending_reports()
            flagged_reviews = await self._count_flagged_reviews()
            
            return SystemMetrics(
                total_users=total_users,
                total_movies=total_movies,
                total_reviews=total_reviews,
                total_reports=total_reports,
                active_users_today=active_users_today,
                active_users_week=active_users_week,
                active_users_month=active_users_month,
                new_users_today=new_users_today,
                new_users_week=new_users_week,
                new_users_month=new_users_month,
                reviews_today=reviews_today,
                reviews_week=reviews_week,
                reviews_month=reviews_month,
                pending_reports=pending_reports,
                flagged_reviews=flagged_reviews
            )
        except Exception as e:
            logger.error("Failed to get system metrics", error=str(e))
            raise LemonPieException("Failed to retrieve system metrics", 500)
    
    async def get_user_analytics(self, date_range: Optional[AnalyticsDateRange] = None) -> UserAnalytics:
        """Get user analytics data"""
        try:
            # Default to last 30 days if no range provided
            if not date_range:
                end_date = datetime.utcnow().date()
                start_date = end_date - timedelta(days=30)
            else:
                start_date = date_range.start_date
                end_date = date_range.end_date
            
            # User growth data
            user_growth = await self._get_user_growth(start_date, end_date)
            
            # User activity patterns
            user_activity = await self._get_user_activity(start_date, end_date)
            
            # Role distribution
            role_distribution = await self._get_role_distribution()
            
            # Top reviewers
            top_reviewers = await self._get_top_reviewers(limit=10)
            
            # User retention (simplified - could be more sophisticated)
            user_retention = await self._get_user_retention()
            
            return UserAnalytics(
                user_growth=user_growth,
                user_activity=user_activity,
                role_distribution=role_distribution,
                top_reviewers=top_reviewers,
                user_retention=user_retention
            )
        except Exception as e:
            logger.error("Failed to get user analytics", error=str(e))
            raise LemonPieException("Failed to retrieve user analytics", 500)
    
    async def get_content_analytics(self, date_range: Optional[AnalyticsDateRange] = None) -> ContentAnalytics:
        """Get content analytics data"""
        try:
            # Default to last 30 days if no range provided
            if not date_range:
                end_date = datetime.utcnow().date()
                start_date = end_date - timedelta(days=30)
            else:
                start_date = date_range.start_date
                end_date = date_range.end_date
            
            # Review trends
            review_trends = await self._get_review_trends(start_date, end_date)
            
            # Rating distribution
            rating_distribution = await self._get_rating_distribution()
            
            # Popular movies
            popular_movies = await self._get_popular_movies(limit=10)
            
            # Genre popularity
            genre_popularity = await self._get_genre_popularity()
            
            # Content moderation stats
            moderation_stats = await self._get_moderation_stats()
            
            return ContentAnalytics(
                review_trends=review_trends,
                rating_distribution=rating_distribution,
                popular_movies=popular_movies,
                genre_popularity=genre_popularity,
                content_moderation_stats=moderation_stats
            )
        except Exception as e:
            logger.error("Failed to get content analytics", error=str(e))
            raise LemonPieException("Failed to retrieve content analytics", 500)
    
    async def get_admin_dashboard(self) -> AdminDashboard:
        """Get complete admin dashboard data"""
        try:
            # Get all dashboard components
            system_metrics = await self.get_system_metrics()
            user_analytics = await self.get_user_analytics()
            content_analytics = await self.get_content_analytics()
            recent_activity = await self._get_recent_activity(limit=20)
            
            return AdminDashboard(
                system_metrics=system_metrics,
                user_analytics=user_analytics,
                content_analytics=content_analytics,
                recent_activity=recent_activity
            )
        except Exception as e:
            logger.error("Failed to get admin dashboard", error=str(e))
            raise LemonPieException("Failed to retrieve admin dashboard", 500)
    
    async def get_users_list(
        self,
        page: int = 1,
        per_page: int = 20,
        search: Optional[str] = None,
        role: Optional[UserRole] = None,
        is_active: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> UserListResponse:
        """Get paginated list of users for admin management"""
        try:
            # Build query
            query = select(User).options(
                selectinload(User.reviews),
                selectinload(User.followers)
            )
            
            # Apply filters
            conditions = []
            if search:
                search_term = f"%{search}%"
                conditions.append(
                    or_(
                        User.name.ilike(search_term),
                        User.email.ilike(search_term)
                    )
                )
            
            if role:
                conditions.append(User.role == role)
            
            if is_active is not None:
                conditions.append(User.is_active == is_active)
            
            if conditions:
                query = query.where(and_(*conditions))
            
            # Apply sorting
            sort_column = getattr(User, sort_by, User.created_at)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
            
            # Get total count
            count_query = select(func.count(User.id))
            if conditions:
                count_query = count_query.where(and_(*conditions))
            
            total_result = await self.db.execute(count_query)
            total = total_result.scalar()
            
            # Apply pagination
            offset = (page - 1) * per_page
            query = query.offset(offset).limit(per_page)
            
            # Execute query
            result = await self.db.execute(query)
            users = result.scalars().all()
            
            # Convert to response format
            user_items = []
            for user in users:
                user_items.append(UserListItem(
                    id=user.id,
                    email=user.email,
                    name=user.name,
                    role=user.role,
                    is_active=user.is_active,
                    is_verified=user.is_verified,
                    created_at=user.created_at,
                    total_reviews=len(user.reviews),
                    total_followers=len(user.followers),
                    last_login=None  # Would need to track this separately
                ))
            
            total_pages = (total + per_page - 1) // per_page
            
            return UserListResponse(
                users=user_items,
                total=total,
                page=page,
                per_page=per_page,
                total_pages=total_pages
            )
        except Exception as e:
            logger.error("Failed to get users list", error=str(e))
            raise LemonPieException("Failed to retrieve users list", 500)
    
    async def update_user_role(self, user_id: UUID, new_role: UserRole, admin_id: UUID) -> bool:
        """Update user role"""
        try:
            # Get user
            result = await self.db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            
            if not user:
                raise LemonPieException("User not found", 404)
            
            old_role = user.role
            user.role = new_role
            user.updated_at = datetime.utcnow()
            
            await self.db.commit()
            
            # Log the action
            logger.info(
                "User role updated",
                user_id=str(user_id),
                old_role=old_role,
                new_role=new_role,
                admin_id=str(admin_id)
            )
            
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to update user role", error=str(e), user_id=str(user_id))
            raise LemonPieException("Failed to update user role", 500)
    
    async def suspend_user(self, user_id: UUID, reason: str, duration_days: Optional[int], admin_id: UUID) -> bool:
        """Suspend user account"""
        try:
            # Get user
            result = await self.db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            
            if not user:
                raise LemonPieException("User not found", 404)
            
            user.is_active = False
            if duration_days:
                user.locked_until = datetime.utcnow() + timedelta(days=duration_days)
            user.updated_at = datetime.utcnow()
            
            await self.db.commit()
            
            # Create notification for user
            notification = Notification(
                user_id=user_id,
                type="account_suspended",
                title="Account Suspended",
                message=f"Your account has been suspended. Reason: {reason}",
                data={"reason": reason, "duration_days": duration_days}
            )
            self.db.add(notification)
            await self.db.commit()
            
            logger.info(
                "User suspended",
                user_id=str(user_id),
                reason=reason,
                duration_days=duration_days,
                admin_id=str(admin_id)
            )
            
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to suspend user", error=str(e), user_id=str(user_id))
            raise LemonPieException("Failed to suspend user", 500)
    
    async def activate_user(self, user_id: UUID, reason: str, admin_id: UUID) -> bool:
        """Activate user account"""
        try:
            # Get user
            result = await self.db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            
            if not user:
                raise LemonPieException("User not found", 404)
            
            user.is_active = True
            user.locked_until = None
            user.login_attempts = 0
            user.updated_at = datetime.utcnow()
            
            await self.db.commit()
            
            # Create notification for user
            notification = Notification(
                user_id=user_id,
                type="account_activated",
                title="Account Activated",
                message=f"Your account has been activated. Reason: {reason}",
                data={"reason": reason}
            )
            self.db.add(notification)
            await self.db.commit()
            
            logger.info(
                "User activated",
                user_id=str(user_id),
                reason=reason,
                admin_id=str(admin_id)
            )
            
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to activate user", error=str(e), user_id=str(user_id))
            raise LemonPieException("Failed to activate user", 500)
    
    # Helper methods for analytics
    async def _count_records(self, model) -> int:
        """Count total records for a model"""
        result = await self.db.execute(select(func.count(model.id)))
        return result.scalar()
    
    async def _count_active_users(self, start_date: date, end_date: date) -> int:
        """Count active users in date range"""
        # Users who created reviews or logged in (simplified - would need login tracking)
        result = await self.db.execute(
            select(func.count(func.distinct(Review.user_id)))
            .where(
                and_(
                    Review.created_at >= start_date,
                    Review.created_at <= end_date + timedelta(days=1)
                )
            )
        )
        return result.scalar() or 0
    
    async def _count_new_users(self, start_date: date, end_date: date) -> int:
        """Count new users in date range"""
        result = await self.db.execute(
            select(func.count(User.id))
            .where(
                and_(
                    User.created_at >= start_date,
                    User.created_at <= end_date + timedelta(days=1)
                )
            )
        )
        return result.scalar() or 0
    
    async def _count_reviews_by_date(self, start_date: date, end_date: date) -> int:
        """Count reviews in date range"""
        result = await self.db.execute(
            select(func.count(Review.id))
            .where(
                and_(
                    Review.created_at >= start_date,
                    Review.created_at <= end_date + timedelta(days=1)
                )
            )
        )
        return result.scalar() or 0
    
    async def _count_pending_reports(self) -> int:
        """Count pending reports"""
        result = await self.db.execute(
            select(func.count(UserReport.id))
            .where(UserReport.status == ModerationStatus.PENDING)
        )
        return result.scalar() or 0
    
    async def _count_flagged_reviews(self) -> int:
        """Count flagged reviews"""
        result = await self.db.execute(
            select(func.count(Review.id))
            .where(Review.is_flagged == True)
        )
        return result.scalar() or 0
    
    async def _get_user_growth(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get user growth data"""
        # Daily user registrations
        query = text("""
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM users
            WHERE DATE(created_at) BETWEEN :start_date AND :end_date
            GROUP BY DATE(created_at)
            ORDER BY date
        """)
        
        result = await self.db.execute(query, {"start_date": start_date, "end_date": end_date})
        return [{"date": str(row.date), "count": row.count} for row in result.fetchall()]
    
    async def _get_user_activity(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get user activity patterns"""
        # Daily review activity
        query = text("""
            SELECT DATE(created_at) as date, COUNT(*) as reviews, COUNT(DISTINCT user_id) as active_users
            FROM reviews
            WHERE DATE(created_at) BETWEEN :start_date AND :end_date
            GROUP BY DATE(created_at)
            ORDER BY date
        """)
        
        result = await self.db.execute(query, {"start_date": start_date, "end_date": end_date})
        return [{"date": str(row.date), "reviews": row.reviews, "active_users": row.active_users} for row in result.fetchall()]
    
    async def _get_role_distribution(self) -> Dict[str, int]:
        """Get user role distribution"""
        query = text("""
            SELECT role, COUNT(*) as count
            FROM users
            GROUP BY role
        """)
        
        result = await self.db.execute(query)
        return {row.role: row.count for row in result.fetchall()}
    
    async def _get_top_reviewers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top reviewers by review count"""
        query = text("""
            SELECT u.id, u.name, u.email, COUNT(r.id) as review_count, AVG(r.lemon_pie_rating) as avg_rating
            FROM users u
            JOIN reviews r ON u.id = r.user_id
            WHERE u.is_active = true
            GROUP BY u.id, u.name, u.email
            ORDER BY review_count DESC
            LIMIT :limit
        """)
        
        result = await self.db.execute(query, {"limit": limit})
        return [
            {
                "id": str(row.id),
                "name": row.name,
                "email": row.email,
                "review_count": row.review_count,
                "avg_rating": float(row.avg_rating) if row.avg_rating else 0
            }
            for row in result.fetchall()
        ]
    
    async def _get_user_retention(self) -> Dict[str, float]:
        """Get user retention metrics (simplified)"""
        # This is a simplified version - real retention would be more complex
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # Users who joined in the last month
        new_users_month = await self._count_new_users(month_ago.date(), now.date())
        
        # Users who were active in the last week (of those who joined last month)
        if new_users_month > 0:
            query = text("""
                SELECT COUNT(DISTINCT r.user_id)
                FROM reviews r
                JOIN users u ON r.user_id = u.id
                WHERE u.created_at >= :month_ago
                AND u.created_at <= :now
                AND r.created_at >= :week_ago
            """)
            
            result = await self.db.execute(query, {
                "month_ago": month_ago,
                "now": now,
                "week_ago": week_ago
            })
            active_new_users = result.scalar() or 0
            retention_rate = (active_new_users / new_users_month) * 100
        else:
            retention_rate = 0
        
        return {
            "weekly_retention": retention_rate,
            "monthly_retention": 0  # Would need more complex calculation
        }
    
    async def _get_review_trends(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """Get review submission trends"""
        query = text("""
            SELECT DATE(created_at) as date, COUNT(*) as count, AVG(lemon_pie_rating) as avg_rating
            FROM reviews
            WHERE DATE(created_at) BETWEEN :start_date AND :end_date
            GROUP BY DATE(created_at)
            ORDER BY date
        """)
        
        result = await self.db.execute(query, {"start_date": start_date, "end_date": end_date})
        return [
            {
                "date": str(row.date),
                "count": row.count,
                "avg_rating": float(row.avg_rating) if row.avg_rating else 0
            }
            for row in result.fetchall()
        ]
    
    async def _get_rating_distribution(self) -> Dict[int, int]:
        """Get rating distribution"""
        query = text("""
            SELECT lemon_pie_rating, COUNT(*) as count
            FROM reviews
            GROUP BY lemon_pie_rating
            ORDER BY lemon_pie_rating
        """)
        
        result = await self.db.execute(query)
        return {row.lemon_pie_rating: row.count for row in result.fetchall()}
    
    async def _get_popular_movies(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular movies by review count"""
        query = text("""
            SELECT m.id, m.title, COUNT(r.id) as review_count, AVG(r.lemon_pie_rating) as avg_rating
            FROM movies m
            LEFT JOIN reviews r ON m.id = r.movie_id
            GROUP BY m.id, m.title
            ORDER BY review_count DESC, avg_rating DESC
            LIMIT :limit
        """)
        
        result = await self.db.execute(query, {"limit": limit})
        return [
            {
                "id": str(row.id),
                "title": row.title,
                "review_count": row.review_count,
                "avg_rating": float(row.avg_rating) if row.avg_rating else 0
            }
            for row in result.fetchall()
        ]
    
    async def _get_genre_popularity(self) -> List[Dict[str, Any]]:
        """Get genre popularity"""
        query = text("""
            SELECT mg.genre, COUNT(r.id) as review_count, AVG(r.lemon_pie_rating) as avg_rating
            FROM movie_genres mg
            JOIN movies m ON mg.movie_id = m.id
            LEFT JOIN reviews r ON m.id = r.movie_id
            GROUP BY mg.genre
            ORDER BY review_count DESC
        """)
        
        result = await self.db.execute(query)
        return [
            {
                "genre": row.genre,
                "review_count": row.review_count,
                "avg_rating": float(row.avg_rating) if row.avg_rating else 0
            }
            for row in result.fetchall()
        ]
    
    async def _get_moderation_stats(self) -> Dict[str, int]:
        """Get content moderation statistics"""
        # Review moderation stats
        review_stats_query = text("""
            SELECT moderation_status, COUNT(*) as count
            FROM reviews
            GROUP BY moderation_status
        """)
        
        result = await self.db.execute(review_stats_query)
        review_stats = {row.moderation_status: row.count for row in result.fetchall()}
        
        # Report stats
        report_stats_query = text("""
            SELECT status, COUNT(*) as count
            FROM user_reports
            GROUP BY status
        """)
        
        result = await self.db.execute(report_stats_query)
        report_stats = {f"reports_{row.status}": row.count for row in result.fetchall()}
        
        return {**review_stats, **report_stats}
    
    async def get_reviews_for_moderation(
        self,
        page: int = 1,
        per_page: int = 20,
        status: Optional[ModerationStatus] = None,
        is_flagged: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> ReviewModerationResponse:
        """Get reviews for moderation dashboard"""
        try:
            # Build query
            query = select(Review).options(
                selectinload(Review.user),
                selectinload(Review.movie),
                selectinload(Review.reports)
            )
            
            # Apply filters
            conditions = []
            if status:
                conditions.append(Review.moderation_status == status)
            
            if is_flagged is not None:
                conditions.append(Review.is_flagged == is_flagged)
            
            if conditions:
                query = query.where(and_(*conditions))
            
            # Apply sorting
            sort_column = getattr(Review, sort_by, Review.created_at)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
            
            # Get total count
            count_query = select(func.count(Review.id))
            if conditions:
                count_query = count_query.where(and_(*conditions))
            
            total_result = await self.db.execute(count_query)
            total = total_result.scalar()
            
            # Apply pagination
            offset = (page - 1) * per_page
            query = query.offset(offset).limit(per_page)
            
            # Execute query
            result = await self.db.execute(query)
            reviews = result.scalars().all()
            
            # Convert to response format
            review_items = []
            for review in reviews:
                review_items.append(ReviewModerationItem(
                    id=review.id,
                    user_id=review.user_id,
                    user_name=review.user.name,
                    movie_id=review.movie_id,
                    movie_title=review.movie.title,
                    review_text=review.review_text,
                    lemon_pie_rating=review.lemon_pie_rating,
                    is_flagged=review.is_flagged,
                    moderation_status=review.moderation_status,
                    created_at=review.created_at,
                    report_count=len(review.reports)
                ))
            
            total_pages = (total + per_page - 1) // per_page
            
            return ReviewModerationResponse(
                reviews=review_items,
                total=total,
                page=page,
                per_page=per_page,
                total_pages=total_pages
            )
        except Exception as e:
            logger.error("Failed to get reviews for moderation", error=str(e))
            raise LemonPieException("Failed to retrieve reviews for moderation", 500)
    
    async def moderate_review(self, review_id: UUID, action: str, reason: Optional[str], admin_id: UUID) -> bool:
        """Moderate a single review"""
        try:
            # Get review
            result = await self.db.execute(select(Review).where(Review.id == review_id))
            review = result.scalar_one_or_none()
            
            if not review:
                raise LemonPieException("Review not found", 404)
            
            # Apply moderation action
            if action == "approve":
                review.moderation_status = ModerationStatus.APPROVED
                review.is_flagged = False
            elif action == "reject":
                review.moderation_status = ModerationStatus.REJECTED
            elif action == "flag":
                review.is_flagged = True
            else:
                raise LemonPieException("Invalid moderation action", 400)
            
            review.updated_at = datetime.utcnow()
            await self.db.commit()
            
            # Create notification for review author if rejected
            if action == "reject":
                notification = Notification(
                    user_id=review.user_id,
                    type="review_rejected",
                    title="Review Rejected",
                    message=f"Your review has been rejected. Reason: {reason or 'Content policy violation'}",
                    data={"review_id": str(review_id), "reason": reason}
                )
                self.db.add(notification)
                await self.db.commit()
            
            logger.info(
                "Review moderated",
                review_id=str(review_id),
                action=action,
                reason=reason,
                admin_id=str(admin_id)
            )
            
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to moderate review", error=str(e), review_id=str(review_id))
            raise LemonPieException("Failed to moderate review", 500)
    
    async def bulk_moderate_reviews(self, review_ids: List[UUID], action: str, reason: Optional[str], admin_id: UUID) -> int:
        """Moderate multiple reviews at once"""
        try:
            # Get reviews
            result = await self.db.execute(
                select(Review).where(Review.id.in_(review_ids))
            )
            reviews = result.scalars().all()
            
            if not reviews:
                raise LemonPieException("No reviews found", 404)
            
            moderated_count = 0
            
            # Apply moderation action to each review
            for review in reviews:
                if action == "approve":
                    review.moderation_status = ModerationStatus.APPROVED
                    review.is_flagged = False
                elif action == "reject":
                    review.moderation_status = ModerationStatus.REJECTED
                elif action == "flag":
                    review.is_flagged = True
                else:
                    continue
                
                review.updated_at = datetime.utcnow()
                moderated_count += 1
                
                # Create notification for review author if rejected
                if action == "reject":
                    notification = Notification(
                        user_id=review.user_id,
                        type="review_rejected",
                        title="Review Rejected",
                        message=f"Your review has been rejected. Reason: {reason or 'Content policy violation'}",
                        data={"review_id": str(review.id), "reason": reason}
                    )
                    self.db.add(notification)
            
            await self.db.commit()
            
            logger.info(
                "Bulk review moderation completed",
                review_count=moderated_count,
                action=action,
                reason=reason,
                admin_id=str(admin_id)
            )
            
            return moderated_count
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to bulk moderate reviews", error=str(e))
            raise LemonPieException("Failed to bulk moderate reviews", 500)
    
    async def get_reports_list(
        self,
        page: int = 1,
        per_page: int = 20,
        status: Optional[ModerationStatus] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> ReportListResponse:
        """Get paginated list of user reports"""
        try:
            # Build query
            query = select(UserReport).options(
                selectinload(UserReport.reporter),
                selectinload(UserReport.reported_user),
                selectinload(UserReport.reported_review),
                selectinload(UserReport.resolver)
            )
            
            # Apply filters
            conditions = []
            if status:
                conditions.append(UserReport.status == status)
            
            if conditions:
                query = query.where(and_(*conditions))
            
            # Apply sorting
            sort_column = getattr(UserReport, sort_by, UserReport.created_at)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
            
            # Get total count
            count_query = select(func.count(UserReport.id))
            if conditions:
                count_query = count_query.where(and_(*conditions))
            
            total_result = await self.db.execute(count_query)
            total = total_result.scalar()
            
            # Apply pagination
            offset = (page - 1) * per_page
            query = query.offset(offset).limit(per_page)
            
            # Execute query
            result = await self.db.execute(query)
            reports = result.scalars().all()
            
            # Convert to response format
            report_items = []
            for report in reports:
                report_items.append(ReportItem(
                    id=report.id,
                    reporter_id=report.reporter_id,
                    reporter_name=report.reporter.name,
                    reported_user_id=report.reported_user_id,
                    reported_user_name=report.reported_user.name if report.reported_user else None,
                    reported_review_id=report.reported_review_id,
                    reason=report.reason,
                    description=report.description,
                    status=report.status,
                    created_at=report.created_at,
                    resolved_by=report.resolved_by,
                    resolved_at=report.resolved_at
                ))
            
            total_pages = (total + per_page - 1) // per_page
            
            return ReportListResponse(
                reports=report_items,
                total=total,
                page=page,
                per_page=per_page,
                total_pages=total_pages
            )
        except Exception as e:
            logger.error("Failed to get reports list", error=str(e))
            raise LemonPieException("Failed to retrieve reports list", 500)
    
    async def resolve_report(self, report_id: UUID, action: str, reason: str, admin_id: UUID, notify_reporter: bool = True, notify_reported: bool = True) -> bool:
        """Resolve a user report"""
        try:
            # Get report
            result = await self.db.execute(
                select(UserReport).options(
                    selectinload(UserReport.reporter),
                    selectinload(UserReport.reported_user),
                    selectinload(UserReport.reported_review)
                ).where(UserReport.id == report_id)
            )
            report = result.scalar_one_or_none()
            
            if not report:
                raise LemonPieException("Report not found", 404)
            
            # Update report status
            if action in ["dismiss", "warn"]:
                report.status = ModerationStatus.REJECTED
            else:
                report.status = ModerationStatus.APPROVED
            
            report.resolved_by = admin_id
            report.resolved_at = datetime.utcnow()
            
            # Take action based on resolution
            if action == "suspend" and report.reported_user:
                # Suspend the reported user
                await self.suspend_user(
                    user_id=report.reported_user_id,
                    reason=f"Report resolution: {reason}",
                    duration_days=7,  # Default 7 days
                    admin_id=admin_id
                )
            elif action == "ban" and report.reported_user:
                # Permanently suspend the reported user
                await self.suspend_user(
                    user_id=report.reported_user_id,
                    reason=f"Report resolution: {reason}",
                    duration_days=None,  # Permanent
                    admin_id=admin_id
                )
            elif action == "warn" and report.reported_user:
                # Send warning notification
                notification = Notification(
                    user_id=report.reported_user_id,
                    type="warning",
                    title="Warning",
                    message=f"You have received a warning. Reason: {reason}",
                    data={"reason": reason, "report_id": str(report_id)}
                )
                self.db.add(notification)
            
            # If reported content is a review, moderate it
            if report.reported_review and action in ["suspend", "ban"]:
                await self.moderate_review(
                    review_id=report.reported_review_id,
                    action="reject",
                    reason=f"Report resolution: {reason}",
                    admin_id=admin_id
                )
            
            await self.db.commit()
            
            # Send notifications
            if notify_reporter:
                notification = Notification(
                    user_id=report.reporter_id,
                    type="report_resolved",
                    title="Report Resolved",
                    message=f"Your report has been resolved. Action taken: {action}",
                    data={"action": action, "reason": reason, "report_id": str(report_id)}
                )
                self.db.add(notification)
            
            if notify_reported and report.reported_user_id and action != "dismiss":
                notification = Notification(
                    user_id=report.reported_user_id,
                    type="report_action",
                    title="Action Taken",
                    message=f"Action has been taken on your account based on a report. Action: {action}",
                    data={"action": action, "reason": reason, "report_id": str(report_id)}
                )
                self.db.add(notification)
            
            await self.db.commit()
            
            logger.info(
                "Report resolved",
                report_id=str(report_id),
                action=action,
                reason=reason,
                admin_id=str(admin_id)
            )
            
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error("Failed to resolve report", error=str(e), report_id=str(report_id))
            raise LemonPieException("Failed to resolve report", 500)

    async def _get_recent_activity(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent platform activity"""
        # Combine recent reviews, user registrations, and reports
        activities = []
        
        # Recent reviews
        recent_reviews_query = text("""
            SELECT 'review' as type, r.id, r.created_at, u.name as user_name, m.title as movie_title
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            JOIN movies m ON r.movie_id = m.id
            ORDER BY r.created_at DESC
            LIMIT :limit
        """)
        
        result = await self.db.execute(recent_reviews_query, {"limit": limit // 2})
        for row in result.fetchall():
            activities.append({
                "type": row.type,
                "id": str(row.id),
                "timestamp": row.created_at.isoformat(),
                "description": f"{row.user_name} reviewed {row.movie_title}"
            })
        
        # Recent user registrations
        recent_users_query = text("""
            SELECT 'user_registration' as type, id, created_at, name
            FROM users
            ORDER BY created_at DESC
            LIMIT :limit
        """)
        
        result = await self.db.execute(recent_users_query, {"limit": limit // 2})
        for row in result.fetchall():
            activities.append({
                "type": row.type,
                "id": str(row.id),
                "timestamp": row.created_at.isoformat(),
                "description": f"New user registered: {row.name}"
            })
        
        # Sort by timestamp and limit
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        return activities[:limit]