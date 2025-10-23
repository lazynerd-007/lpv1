"""
Review schemas for LemonNPie Backend API
"""
from datetime import datetime
from typing import Optional, List, Dict
from uuid import UUID

from pydantic import BaseModel, Field, validator

from app.models.enums import ModerationStatus, VoteType
from app.schemas.user import UserPublicProfile


class ReviewBase(BaseModel):
    """Base schema for review data"""
    lemon_pie_rating: int = Field(..., ge=1, le=10, description="Overall LemonPie rating (1-10)")
    review_text: str = Field(..., min_length=10, max_length=5000, description="Review content")
    spoiler_warning: bool = Field(False, description="Whether review contains spoilers")
    cultural_authenticity_rating: Optional[int] = Field(None, ge=1, le=10, description="Cultural authenticity rating (1-10)")
    production_quality_rating: Optional[int] = Field(None, ge=1, le=10, description="Production quality rating (1-10)")
    story_rating: Optional[int] = Field(None, ge=1, le=10, description="Story rating (1-10)")
    acting_rating: Optional[int] = Field(None, ge=1, le=10, description="Acting rating (1-10)")
    cinematography_rating: Optional[int] = Field(None, ge=1, le=10, description="Cinematography rating (1-10)")
    review_language: str = Field("en", max_length=10, description="Review language code")


class ReviewCreate(ReviewBase):
    """Schema for creating a new review"""
    movie_id: UUID = Field(..., description="ID of the movie being reviewed")
    
    @validator('review_text')
    def validate_review_text(cls, v):
        """Validate review text content"""
        if not v.strip():
            raise ValueError('Review text cannot be empty')
        
        # Basic content validation - no excessive profanity or spam patterns
        v = v.strip()
        
        # Check for minimum meaningful content (not just repeated characters)
        if len(set(v.lower().replace(' ', ''))) < 5:
            raise ValueError('Review must contain meaningful content')
        
        return v


class ReviewUpdate(BaseModel):
    """Schema for updating an existing review"""
    lemon_pie_rating: Optional[int] = Field(None, ge=1, le=10)
    review_text: Optional[str] = Field(None, min_length=10, max_length=5000)
    spoiler_warning: Optional[bool] = None
    cultural_authenticity_rating: Optional[int] = Field(None, ge=1, le=10)
    production_quality_rating: Optional[int] = Field(None, ge=1, le=10)
    story_rating: Optional[int] = Field(None, ge=1, le=10)
    acting_rating: Optional[int] = Field(None, ge=1, le=10)
    cinematography_rating: Optional[int] = Field(None, ge=1, le=10)
    review_language: Optional[str] = Field(None, max_length=10)
    
    @validator('review_text')
    def validate_review_text(cls, v):
        """Validate review text content"""
        if v is not None:
            if not v.strip():
                raise ValueError('Review text cannot be empty')
            
            v = v.strip()
            
            # Check for minimum meaningful content
            if len(set(v.lower().replace(' ', ''))) < 5:
                raise ValueError('Review must contain meaningful content')
        
        return v


class ReviewVoteCreate(BaseModel):
    """Schema for voting on a review"""
    vote_type: VoteType = Field(..., description="Type of vote (helpful/unhelpful)")


class ReviewResponse(ReviewBase):
    """Schema for review response"""
    id: UUID
    user: "UserPublicProfile"
    movie_id: UUID
    helpful_votes: int = 0
    unhelpful_votes: int = 0
    helpfulness_score: int = 0
    user_vote: Optional[VoteType] = None
    is_flagged: bool = False
    moderation_status: ModerationStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReviewListResponse(BaseModel):
    """Schema for review list item"""
    id: UUID
    user: "UserPublicProfile"
    movie_id: UUID
    lemon_pie_rating: int
    review_text: str
    spoiler_warning: bool
    helpful_votes: int = 0
    unhelpful_votes: int = 0
    helpfulness_score: int = 0
    user_vote: Optional[VoteType] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReviewFilters(BaseModel):
    """Schema for review filtering options"""
    movie_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    rating_min: Optional[int] = Field(None, ge=1, le=10)
    rating_max: Optional[int] = Field(None, ge=1, le=10)
    spoiler_warning: Optional[bool] = None
    moderation_status: Optional[ModerationStatus] = None
    has_spoilers: Optional[bool] = None


class ReviewSortBy(BaseModel):
    """Schema for review sorting options"""
    field: str = Field("created_at", pattern="^(created_at|updated_at|lemon_pie_rating|helpful_votes|helpfulness_score)$")
    order: str = Field("desc", pattern="^(asc|desc)$")


class ReviewListRequest(BaseModel):
    """Schema for review list request with pagination and filtering"""
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    filters: Optional[ReviewFilters] = None
    sort_by: Optional[ReviewSortBy] = None


class PaginatedReviewResponse(BaseModel):
    """Schema for paginated review response"""
    items: List[ReviewListResponse]
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
    has_prev: bool


class ReviewStats(BaseModel):
    """Schema for review statistics"""
    total_reviews: int
    average_rating: float
    rating_distribution: Dict[int, int]
    cultural_authenticity_avg: Optional[float] = None
    production_quality_avg: Optional[float] = None
    story_rating_avg: Optional[float] = None
    acting_rating_avg: Optional[float] = None
    cinematography_rating_avg: Optional[float] = None
    
    class Config:
        from_attributes = True


class ReviewModerationAction(BaseModel):
    """Schema for review moderation actions"""
    action: str = Field(..., pattern="^(approve|reject|flag|unflag)$")
    reason: Optional[str] = Field(None, max_length=500)


class ReviewReportCreate(BaseModel):
    """Schema for reporting a review"""
    reason: str = Field(..., min_length=5, max_length=500, description="Reason for reporting")
    category: str = Field(..., pattern="^(spam|inappropriate|offensive|copyright|other)$")


# Resolve forward references
ReviewResponse.model_rebuild()
ReviewListResponse.model_rebuild()