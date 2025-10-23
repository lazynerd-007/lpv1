"""
Review API routes
"""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.auth.dependencies import get_current_user, get_optional_current_user, require_moderator_or_admin
from app.services.review_service import get_review_service, ReviewService
from app.schemas.review import (
    ReviewCreate,
    ReviewUpdate,
    ReviewResponse,
    ReviewListRequest,
    PaginatedReviewResponse,
    ReviewFilters,
    ReviewSortBy,
    ReviewVoteCreate,
    ReviewStats,
    ReviewModerationAction,
    ReviewReportCreate
)
from app.models.user import User


router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Create a new review for a movie
    
    - **movie_id**: ID of the movie to review
    - **lemon_pie_rating**: Overall rating (1-10)
    - **review_text**: Review content (10-5000 characters)
    - **spoiler_warning**: Whether review contains spoilers
    - **cultural_authenticity_rating**: Optional cultural authenticity rating (1-10)
    - **production_quality_rating**: Optional production quality rating (1-10)
    - **story_rating**: Optional story rating (1-10)
    - **acting_rating**: Optional acting rating (1-10)
    - **cinematography_rating**: Optional cinematography rating (1-10)
    - **review_language**: Language code (default: 'en')
    
    Returns the created review with user information.
    Users can only have one review per movie.
    """
    return await review_service.create_review(review_data, current_user.id)


@router.get("/", response_model=PaginatedReviewResponse)
async def get_reviews(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    movie_id: Optional[UUID] = Query(None, description="Filter by movie ID"),
    user_id: Optional[UUID] = Query(None, description="Filter by user ID"),
    rating_min: Optional[int] = Query(None, ge=1, le=10, description="Minimum rating filter"),
    rating_max: Optional[int] = Query(None, ge=1, le=10, description="Maximum rating filter"),
    spoiler_warning: Optional[bool] = Query(None, description="Filter by spoiler warning"),
    sort_field: str = Query("created_at", regex="^(created_at|updated_at|lemon_pie_rating|helpful_votes|helpfulness_score)$", description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Get paginated list of reviews with filtering and sorting
    
    **Filtering options:**
    - **movie_id**: Show reviews for specific movie
    - **user_id**: Show reviews by specific user
    - **rating_min/rating_max**: Filter by rating range
    - **spoiler_warning**: Filter by spoiler warning status
    
    **Sorting options:**
    - **sort_field**: Field to sort by (created_at, updated_at, lemon_pie_rating, helpful_votes, helpfulness_score)
    - **sort_order**: Sort order (asc, desc)
    
    Returns paginated list of reviews with user vote information if authenticated.
    Only approved reviews are shown by default.
    """
    
    # Build filters
    filters = ReviewFilters(
        movie_id=movie_id,
        user_id=user_id,
        rating_min=rating_min,
        rating_max=rating_max,
        spoiler_warning=spoiler_warning
    )
    
    # Build sort options
    sort_by = ReviewSortBy(field=sort_field, order=sort_order)
    
    user_id_for_votes = current_user.id if current_user else None
    
    return await review_service.get_reviews(
        page=page,
        limit=limit,
        filters=filters,
        sort_by=sort_by,
        user_id=user_id_for_votes
    )


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(
    review_id: UUID,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Get a specific review by ID
    
    Returns review details with user vote information if authenticated.
    """
    user_id = current_user.id if current_user else None
    return await review_service.get_review(review_id, user_id)


@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: UUID,
    review_data: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Update an existing review
    
    Users can only update their own reviews.
    All fields are optional - only provided fields will be updated.
    
    - **lemon_pie_rating**: Overall rating (1-10)
    - **review_text**: Review content (10-5000 characters)
    - **spoiler_warning**: Whether review contains spoilers
    - **cultural_authenticity_rating**: Cultural authenticity rating (1-10)
    - **production_quality_rating**: Production quality rating (1-10)
    - **story_rating**: Story rating (1-10)
    - **acting_rating**: Acting rating (1-10)
    - **cinematography_rating**: Cinematography rating (1-10)
    - **review_language**: Language code
    """
    return await review_service.update_review(review_id, review_data, current_user.id)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Delete a review
    
    Users can only delete their own reviews.
    This action cannot be undone.
    """
    await review_service.delete_review(review_id, current_user.id)


@router.post("/{review_id}/vote", response_model=ReviewResponse)
async def vote_on_review(
    review_id: UUID,
    vote_data: ReviewVoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Vote on a review (helpful or unhelpful)
    
    - **vote_type**: Type of vote ('helpful' or 'unhelpful')
    
    Users cannot vote on their own reviews.
    If user has already voted, the vote will be updated.
    Returns updated review with new vote counts.
    """
    return await review_service.vote_on_review(review_id, vote_data, current_user.id)


@router.delete("/{review_id}/vote", response_model=ReviewResponse)
async def remove_vote(
    review_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Remove your vote from a review
    
    Returns updated review with adjusted vote counts.
    """
    return await review_service.remove_vote(review_id, current_user.id)


@router.get("/stats/movie/{movie_id}", response_model=ReviewStats)
async def get_movie_review_stats(
    movie_id: UUID,
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Get review statistics for a specific movie
    
    Returns aggregated statistics including:
    - Total review count
    - Average rating
    - Rating distribution
    - Category averages (cultural authenticity, production quality, etc.)
    """
    return await review_service.get_review_stats(movie_id)


@router.get("/stats/overall", response_model=ReviewStats)
async def get_overall_review_stats(
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Get overall review statistics across all movies
    
    Returns platform-wide aggregated statistics.
    """
    return await review_service.get_review_stats()


# Additional endpoints for trending and featured reviews
@router.get("/trending/", response_model=PaginatedReviewResponse)
async def get_trending_reviews(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=50, description="Items per page"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Get trending reviews (sorted by helpfulness score)
    
    Returns reviews sorted by helpfulness score (helpful_votes - unhelpful_votes).
    """
    
    # Use helpfulness score sorting for trending
    sort_by = ReviewSortBy(field="helpfulness_score", order="desc")
    user_id = current_user.id if current_user else None
    
    return await review_service.get_reviews(
        page=page,
        limit=limit,
        sort_by=sort_by,
        user_id=user_id
    )


@router.get("/recent/", response_model=PaginatedReviewResponse)
async def get_recent_reviews(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=50, description="Items per page"),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Get most recent reviews
    
    Returns reviews sorted by creation date (newest first).
    """
    
    sort_by = ReviewSortBy(field="created_at", order="desc")
    user_id = current_user.id if current_user else None
    
    return await review_service.get_reviews(
        page=page,
        limit=limit,
        sort_by=sort_by,
        user_id=user_id
    )

# Moderation endpoints
@router.post("/{review_id}/report", status_code=status.HTTP_201_CREATED)
async def report_review(
    review_id: UUID,
    report_data: ReviewReportCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Report a review for inappropriate content
    
    - **reason**: Detailed reason for reporting (5-500 characters)
    - **category**: Category of report (spam, inappropriate, offensive, copyright, other)
    
    Users cannot report their own reviews.
    Multiple reports will automatically flag the review for moderation.
    """
    await review_service.report_review(review_id, report_data, current_user.id)
    return {"message": "Review reported successfully"}


@router.post("/{review_id}/moderate", response_model=ReviewResponse)
async def moderate_review(
    review_id: UUID,
    action_data: ReviewModerationAction,
    current_user: User = Depends(require_moderator_or_admin),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Moderate a review (Moderator/Admin only)
    
    - **action**: Moderation action (approve, reject, flag, unflag)
    - **reason**: Optional reason for the action
    
    Available actions:
    - **approve**: Approve the review and make it visible
    - **reject**: Reject the review and hide it
    - **flag**: Flag the review for further review
    - **unflag**: Remove flag and approve the review
    
    This action will also resolve any pending reports for the review.
    """
    return await review_service.moderate_review(review_id, action_data, current_user.id)


@router.get("/moderation/flagged", response_model=PaginatedReviewResponse)
async def get_flagged_reviews(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(require_moderator_or_admin),
    db: AsyncSession = Depends(get_db),
    review_service: ReviewService = Depends(get_review_service)
):
    """
    Get flagged reviews for moderation (Moderator/Admin only)
    
    Returns reviews that are flagged or pending moderation.
    Sorted by creation date (newest first).
    """
    return await review_service.get_flagged_reviews(page, limit, current_user.id)