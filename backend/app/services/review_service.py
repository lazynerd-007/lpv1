"""
Review service for LemonNPie Backend API
"""
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID
from datetime import datetime
import math

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc, asc, update, delete
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.review import Review
from app.models.user import User
from app.models.movie import Movie
from app.models.relationships import ReviewVote
from app.models.moderation import UserReport
from app.models.enums import VoteType, ModerationStatus, UserRole
from app.schemas.review import (
    ReviewCreate, 
    ReviewUpdate, 
    ReviewResponse, 
    ReviewListResponse,
    ReviewFilters,
    ReviewSortBy,
    PaginatedReviewResponse,
    ReviewStats,
    ReviewVoteCreate,
    ReviewModerationAction,
    ReviewReportCreate
)
from app.schemas.user import UserPublicProfile


class ReviewService:
    """Service for managing reviews"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_review(self, review_data: ReviewCreate, user_id: UUID) -> ReviewResponse:
        """Create a new review"""
        
        # Check if user already has a review for this movie
        existing_review = await self.db.execute(
            select(Review).where(
                and_(
                    Review.user_id == user_id,
                    Review.movie_id == review_data.movie_id
                )
            )
        )
        if existing_review.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already reviewed this movie"
            )
        
        # Verify movie exists
        movie = await self.db.execute(
            select(Movie).where(Movie.id == review_data.movie_id)
        )
        if not movie.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found"
            )
        
        # Check for inappropriate content
        should_flag = await self.auto_moderate_review(review_data.review_text)
        
        # Create review
        review = Review(
            user_id=user_id,
            movie_id=review_data.movie_id,
            lemon_pie_rating=review_data.lemon_pie_rating,
            review_text=review_data.review_text,
            spoiler_warning=review_data.spoiler_warning,
            cultural_authenticity_rating=review_data.cultural_authenticity_rating,
            production_quality_rating=review_data.production_quality_rating,
            story_rating=review_data.story_rating,
            acting_rating=review_data.acting_rating,
            cinematography_rating=review_data.cinematography_rating,
            review_language=review_data.review_language,
            is_flagged=should_flag,
            moderation_status=ModerationStatus.PENDING if should_flag else ModerationStatus.APPROVED
        )
        
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        
        # Load user relationship for response
        await self.db.refresh(review, ['user'])
        
        return await self._build_review_response(review, user_id)
    
    async def get_review(self, review_id: UUID, user_id: Optional[UUID] = None) -> ReviewResponse:
        """Get a single review by ID"""
        
        query = select(Review).options(
            selectinload(Review.user)
        ).where(Review.id == review_id)
        
        result = await self.db.execute(query)
        review = result.scalar_one_or_none()
        
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        
        return await self._build_review_response(review, user_id)
    
    async def update_review(self, review_id: UUID, review_data: ReviewUpdate, user_id: UUID) -> ReviewResponse:
        """Update an existing review"""
        
        # Get review and verify ownership
        query = select(Review).options(
            selectinload(Review.user)
        ).where(Review.id == review_id)
        
        result = await self.db.execute(query)
        review = result.scalar_one_or_none()
        
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        
        if review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own reviews"
            )
        
        # Update fields
        update_data = review_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(review, field, value)
        
        review.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(review)
        
        return await self._build_review_response(review, user_id)
    
    async def delete_review(self, review_id: UUID, user_id: UUID) -> bool:
        """Delete a review"""
        
        # Get review and verify ownership
        query = select(Review).where(Review.id == review_id)
        result = await self.db.execute(query)
        review = result.scalar_one_or_none()
        
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        
        if review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own reviews"
            )
        
        await self.db.delete(review)
        await self.db.commit()
        
        return True
    
    async def get_reviews(
        self, 
        page: int = 1, 
        limit: int = 20,
        filters: Optional[ReviewFilters] = None,
        sort_by: Optional[ReviewSortBy] = None,
        user_id: Optional[UUID] = None
    ) -> PaginatedReviewResponse:
        """Get paginated list of reviews with filtering and sorting"""
        
        # Build base query
        query = select(Review).options(
            selectinload(Review.user)
        )
        
        # Apply filters
        if filters:
            conditions = []
            
            if filters.movie_id:
                conditions.append(Review.movie_id == filters.movie_id)
            
            if filters.user_id:
                conditions.append(Review.user_id == filters.user_id)
            
            if filters.rating_min is not None:
                conditions.append(Review.lemon_pie_rating >= filters.rating_min)
            
            if filters.rating_max is not None:
                conditions.append(Review.lemon_pie_rating <= filters.rating_max)
            
            if filters.spoiler_warning is not None:
                conditions.append(Review.spoiler_warning == filters.spoiler_warning)
            
            if filters.moderation_status:
                conditions.append(Review.moderation_status == filters.moderation_status)
            else:
                # Default to approved reviews only
                conditions.append(Review.moderation_status == ModerationStatus.APPROVED)
            
            if conditions:
                query = query.where(and_(*conditions))
        else:
            # Default to approved reviews only
            query = query.where(Review.moderation_status == ModerationStatus.APPROVED)
        
        # Apply sorting
        if sort_by:
            order_func = desc if sort_by.order == "desc" else asc
            
            if sort_by.field == "created_at":
                query = query.order_by(order_func(Review.created_at))
            elif sort_by.field == "updated_at":
                query = query.order_by(order_func(Review.updated_at))
            elif sort_by.field == "lemon_pie_rating":
                query = query.order_by(order_func(Review.lemon_pie_rating))
            elif sort_by.field == "helpful_votes":
                query = query.order_by(order_func(Review.helpful_votes))
            elif sort_by.field == "helpfulness_score":
                # Calculate helpfulness score as helpful_votes - unhelpful_votes
                query = query.order_by(order_func(Review.helpful_votes - Review.unhelpful_votes))
        else:
            # Default sort by creation date (newest first)
            query = query.order_by(desc(Review.created_at))
        
        # Get total count
        count_query = select(func.count(Review.id))
        if filters:
            # Apply same filters to count query
            conditions = []
            
            if filters.movie_id:
                conditions.append(Review.movie_id == filters.movie_id)
            
            if filters.user_id:
                conditions.append(Review.user_id == filters.user_id)
            
            if filters.rating_min is not None:
                conditions.append(Review.lemon_pie_rating >= filters.rating_min)
            
            if filters.rating_max is not None:
                conditions.append(Review.lemon_pie_rating <= filters.rating_max)
            
            if filters.spoiler_warning is not None:
                conditions.append(Review.spoiler_warning == filters.spoiler_warning)
            
            if filters.moderation_status:
                conditions.append(Review.moderation_status == filters.moderation_status)
            else:
                conditions.append(Review.moderation_status == ModerationStatus.APPROVED)
            
            if conditions:
                count_query = count_query.where(and_(*conditions))
        else:
            count_query = count_query.where(Review.moderation_status == ModerationStatus.APPROVED)
        
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        reviews = result.scalars().all()
        
        # Build response items
        items = []
        for review in reviews:
            review_response = await self._build_review_list_response(review, user_id)
            items.append(review_response)
        
        # Calculate pagination info
        pages = math.ceil(total / limit) if total > 0 else 1
        has_next = page < pages
        has_prev = page > 1
        
        return PaginatedReviewResponse(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev
        )
    
    async def vote_on_review(self, review_id: UUID, vote_data: ReviewVoteCreate, user_id: UUID) -> ReviewResponse:
        """Vote on a review (helpful/unhelpful)"""
        
        # Get review
        review = await self.db.execute(
            select(Review).options(selectinload(Review.user)).where(Review.id == review_id)
        )
        review = review.scalar_one_or_none()
        
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        
        # Prevent self-voting
        if review.user_id == user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot vote on your own review"
            )
        
        # Check for existing vote
        existing_vote = await self.db.execute(
            select(ReviewVote).where(
                and_(
                    ReviewVote.user_id == user_id,
                    ReviewVote.review_id == review_id
                )
            )
        )
        existing_vote = existing_vote.scalar_one_or_none()
        
        if existing_vote:
            # Update existing vote if different
            if existing_vote.vote_type != vote_data.vote_type:
                # Remove old vote count
                if existing_vote.vote_type == VoteType.HELPFUL:
                    review.helpful_votes = max(0, review.helpful_votes - 1)
                else:
                    review.unhelpful_votes = max(0, review.unhelpful_votes - 1)
                
                # Update vote type
                existing_vote.vote_type = vote_data.vote_type
                
                # Add new vote count
                if vote_data.vote_type == VoteType.HELPFUL:
                    review.helpful_votes += 1
                else:
                    review.unhelpful_votes += 1
            # If same vote type, no change needed
        else:
            # Create new vote
            vote = ReviewVote(
                user_id=user_id,
                review_id=review_id,
                vote_type=vote_data.vote_type
            )
            self.db.add(vote)
            
            # Update vote count
            if vote_data.vote_type == VoteType.HELPFUL:
                review.helpful_votes += 1
            else:
                review.unhelpful_votes += 1
        
        await self.db.commit()
        await self.db.refresh(review)
        
        return await self._build_review_response(review, user_id)
    
    async def remove_vote(self, review_id: UUID, user_id: UUID) -> ReviewResponse:
        """Remove user's vote from a review"""
        
        # Get review
        review = await self.db.execute(
            select(Review).options(selectinload(Review.user)).where(Review.id == review_id)
        )
        review = review.scalar_one_or_none()
        
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        
        # Get existing vote
        existing_vote = await self.db.execute(
            select(ReviewVote).where(
                and_(
                    ReviewVote.user_id == user_id,
                    ReviewVote.review_id == review_id
                )
            )
        )
        existing_vote = existing_vote.scalar_one_or_none()
        
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote not found"
            )
        
        # Remove vote count
        if existing_vote.vote_type == VoteType.HELPFUL:
            review.helpful_votes = max(0, review.helpful_votes - 1)
        else:
            review.unhelpful_votes = max(0, review.unhelpful_votes - 1)
        
        # Delete vote
        await self.db.delete(existing_vote)
        await self.db.commit()
        await self.db.refresh(review)
        
        return await self._build_review_response(review, user_id)
    
    async def report_review(self, review_id: UUID, report_data: ReviewReportCreate, reporter_id: UUID) -> bool:
        """Report a review for moderation"""
        
        # Check if review exists
        review = await self.db.execute(
            select(Review).where(Review.id == review_id)
        )
        review = review.scalar_one_or_none()
        
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        
        # Prevent self-reporting
        if review.user_id == reporter_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You cannot report your own review"
            )
        
        # Check for existing report from this user
        existing_report = await self.db.execute(
            select(UserReport).where(
                and_(
                    UserReport.reporter_id == reporter_id,
                    UserReport.reported_review_id == review_id
                )
            )
        )
        if existing_report.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already reported this review"
            )
        
        # Create report
        report = UserReport(
            reporter_id=reporter_id,
            reported_review_id=review_id,
            reason=report_data.category,
            description=report_data.reason,
            status=ModerationStatus.PENDING
        )
        
        self.db.add(report)
        
        # Flag the review for moderation if it gets multiple reports
        report_count = await self.db.execute(
            select(func.count(UserReport.id)).where(
                and_(
                    UserReport.reported_review_id == review_id,
                    UserReport.status == ModerationStatus.PENDING
                )
            )
        )
        
        if report_count.scalar() >= 3:  # Auto-flag after 3 reports
            review.is_flagged = True
            review.moderation_status = ModerationStatus.PENDING
        
        await self.db.commit()
        return True
    
    async def moderate_review(self, review_id: UUID, action_data: ReviewModerationAction, moderator_id: UUID) -> ReviewResponse:
        """Moderate a review (admin/moderator only)"""
        
        # Get review
        review = await self.db.execute(
            select(Review).options(selectinload(Review.user)).where(Review.id == review_id)
        )
        review = review.scalar_one_or_none()
        
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found"
            )
        
        # Apply moderation action
        if action_data.action == "approve":
            review.moderation_status = ModerationStatus.APPROVED
            review.is_flagged = False
        elif action_data.action == "reject":
            review.moderation_status = ModerationStatus.REJECTED
            review.is_flagged = True
        elif action_data.action == "flag":
            review.is_flagged = True
            review.moderation_status = ModerationStatus.PENDING
        elif action_data.action == "unflag":
            review.is_flagged = False
            if review.moderation_status == ModerationStatus.PENDING:
                review.moderation_status = ModerationStatus.APPROVED
        
        # Update related reports
        if action_data.action in ["approve", "reject"]:
            await self.db.execute(
                update(UserReport)
                .where(UserReport.reported_review_id == review_id)
                .values(
                    status=ModerationStatus.APPROVED if action_data.action == "approve" else ModerationStatus.REJECTED,
                    resolved_by=moderator_id,
                    resolved_at=datetime.utcnow()
                )
            )
        
        await self.db.commit()
        await self.db.refresh(review)
        
        return await self._build_review_response(review, moderator_id)
    
    async def get_flagged_reviews(
        self, 
        moderator_id: UUID,
        page: int = 1, 
        limit: int = 20
    ) -> PaginatedReviewResponse:
        """Get flagged reviews for moderation"""
        
        # Build query for flagged reviews
        query = select(Review).options(
            selectinload(Review.user)
        ).where(
            or_(
                Review.is_flagged == True,
                Review.moderation_status == ModerationStatus.PENDING
            )
        ).order_by(desc(Review.created_at))
        
        # Get total count
        count_query = select(func.count(Review.id)).where(
            or_(
                Review.is_flagged == True,
                Review.moderation_status == ModerationStatus.PENDING
            )
        )
        
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        reviews = result.scalars().all()
        
        # Build response items
        items = []
        for review in reviews:
            review_response = await self._build_review_response(review, moderator_id)
            items.append(ReviewListResponse(
                id=review_response.id,
                user=review_response.user,
                movie_id=review_response.movie_id,
                lemon_pie_rating=review_response.lemon_pie_rating,
                review_text=review_response.review_text,
                spoiler_warning=review_response.spoiler_warning,
                helpful_votes=review_response.helpful_votes,
                unhelpful_votes=review_response.unhelpful_votes,
                helpfulness_score=review_response.helpfulness_score,
                user_vote=review_response.user_vote,
                created_at=review_response.created_at,
                updated_at=review_response.updated_at
            ))
        
        # Calculate pagination info
        pages = math.ceil(total / limit) if total > 0 else 1
        has_next = page < pages
        has_prev = page > 1
        
        return PaginatedReviewResponse(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev
        )
    
    async def auto_moderate_review(self, review_text: str) -> bool:
        """
        Automatic content moderation using basic keyword filtering
        Returns True if content should be flagged
        """
        
        # Basic inappropriate content detection
        inappropriate_keywords = [
            'spam', 'scam', 'fake', 'bot', 'advertisement', 'ad',
            # Add more keywords as needed
        ]
        
        text_lower = review_text.lower()
        
        # Check for excessive profanity or spam patterns
        for keyword in inappropriate_keywords:
            if keyword in text_lower:
                return True
        
        # Check for excessive repetition (spam indicator)
        words = text_lower.split()
        if len(words) > 10:
            unique_words = set(words)
            if len(unique_words) / len(words) < 0.3:  # Less than 30% unique words
                return True
        
        # Check for excessive capitalization
        if len([c for c in review_text if c.isupper()]) / len(review_text) > 0.7:
            return True
        
        return False

    async def get_review_stats(self, movie_id: Optional[UUID] = None) -> ReviewStats:
        """Get review statistics for a movie or overall"""
        
        base_query = select(Review).where(Review.moderation_status == ModerationStatus.APPROVED)
        
        if movie_id:
            base_query = base_query.where(Review.movie_id == movie_id)
        
        # Get total count and average rating
        count_query = select(func.count(Review.id)).select_from(base_query.subquery())
        avg_query = select(func.avg(Review.lemon_pie_rating)).select_from(base_query.subquery())
        
        count_result = await self.db.execute(count_query)
        avg_result = await self.db.execute(avg_query)
        
        total_reviews = count_result.scalar() or 0
        average_rating = float(avg_result.scalar() or 0)
        
        # Get rating distribution
        rating_dist_query = select(
            Review.lemon_pie_rating,
            func.count(Review.id)
        ).select_from(base_query.subquery()).group_by(Review.lemon_pie_rating)
        
        rating_dist_result = await self.db.execute(rating_dist_query)
        rating_distribution = {rating: count for rating, count in rating_dist_result.fetchall()}
        
        # Get category averages
        category_avgs = {}
        for category in ['cultural_authenticity_rating', 'production_quality_rating', 
                        'story_rating', 'acting_rating', 'cinematography_rating']:
            avg_query = select(func.avg(getattr(Review, category))).select_from(
                base_query.where(getattr(Review, category).isnot(None)).subquery()
            )
            result = await self.db.execute(avg_query)
            avg_value = result.scalar()
            category_avgs[f"{category.replace('_rating', '')}_avg"] = float(avg_value) if avg_value else None
        
        return ReviewStats(
            total_reviews=total_reviews,
            average_rating=average_rating,
            rating_distribution=rating_distribution,
            **category_avgs
        )
    
    async def _build_review_response(self, review: Review, user_id: Optional[UUID] = None) -> ReviewResponse:
        """Build a complete review response with user vote info"""
        
        # Get user's vote if authenticated
        user_vote = None
        if user_id:
            vote_query = select(ReviewVote.vote_type).where(
                and_(
                    ReviewVote.user_id == user_id,
                    ReviewVote.review_id == review.id
                )
            )
            vote_result = await self.db.execute(vote_query)
            user_vote = vote_result.scalar_one_or_none()
        
        # Calculate helpfulness score
        helpfulness_score = review.helpful_votes - review.unhelpful_votes
        
        # Build user profile
        user_profile = UserPublicProfile(
            id=review.user.id,
            name=review.user.name,
            bio=review.user.bio,
            location=review.user.location,
            avatar_url=review.user.avatar_url,
            role=review.user.role,
            is_verified=review.user.is_verified,
            created_at=review.user.created_at,
            stats=None  # We'll skip stats for now to avoid circular dependencies
        )
        
        return ReviewResponse(
            id=review.id,
            user=user_profile,
            movie_id=review.movie_id,
            lemon_pie_rating=review.lemon_pie_rating,
            review_text=review.review_text,
            spoiler_warning=review.spoiler_warning,
            cultural_authenticity_rating=review.cultural_authenticity_rating,
            production_quality_rating=review.production_quality_rating,
            story_rating=review.story_rating,
            acting_rating=review.acting_rating,
            cinematography_rating=review.cinematography_rating,
            review_language=review.review_language,
            helpful_votes=review.helpful_votes,
            unhelpful_votes=review.unhelpful_votes,
            helpfulness_score=helpfulness_score,
            user_vote=user_vote,
            is_flagged=review.is_flagged,
            moderation_status=review.moderation_status,
            created_at=review.created_at,
            updated_at=review.updated_at
        )
    
    async def _build_review_list_response(self, review: Review, user_id: Optional[UUID] = None) -> ReviewListResponse:
        """Build a review list response (lighter version)"""
        
        # Get user's vote if authenticated
        user_vote = None
        if user_id:
            vote_query = select(ReviewVote.vote_type).where(
                and_(
                    ReviewVote.user_id == user_id,
                    ReviewVote.review_id == review.id
                )
            )
            vote_result = await self.db.execute(vote_query)
            user_vote = vote_result.scalar_one_or_none()
        
        # Calculate helpfulness score
        helpfulness_score = review.helpful_votes - review.unhelpful_votes
        
        # Build user profile
        user_profile = UserPublicProfile(
            id=review.user.id,
            name=review.user.name,
            bio=review.user.bio,
            location=review.user.location,
            avatar_url=review.user.avatar_url,
            role=review.user.role,
            is_verified=review.user.is_verified,
            created_at=review.user.created_at,
            stats=None  # We'll skip stats for now
        )
        
        return ReviewListResponse(
            id=review.id,
            user=user_profile,
            movie_id=review.movie_id,
            lemon_pie_rating=review.lemon_pie_rating,
            review_text=review.review_text,
            spoiler_warning=review.spoiler_warning,
            helpful_votes=review.helpful_votes,
            unhelpful_votes=review.unhelpful_votes,
            helpfulness_score=helpfulness_score,
            user_vote=user_vote,
            created_at=review.created_at,
            updated_at=review.updated_at
        )


# Service instance
def get_review_service(db: AsyncSession) -> ReviewService:
    """Get review service instance"""
    return ReviewService(db)