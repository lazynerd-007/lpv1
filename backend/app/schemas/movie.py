"""
Movie schemas for LemonNPie Backend API
"""
from datetime import date, datetime
from typing import List, Optional, Dict
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import ContentType, CastRole


class CastMember(BaseModel):
    actor_name: str
    character_name: Optional[str] = None
    role_type: CastRole = CastRole.ACTOR


class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    local_title: Optional[str] = Field(None, max_length=500)
    release_date: date
    runtime: Optional[int] = Field(None, gt=0)
    plot_summary: Optional[str] = None
    director: Optional[str] = Field(None, max_length=255)
    producer: Optional[str] = Field(None, max_length=255)
    production_company: Optional[str] = Field(None, max_length=255)
    production_state: Optional[str] = Field(None, max_length=100)
    box_office_ng: Optional[str] = Field(None, max_length=100)
    type: ContentType = ContentType.MOVIE


class MovieCreate(MovieBase):
    genres: List[str] = []
    languages: List[str] = []
    cast: List[CastMember] = []
    poster_url: Optional[str] = Field(None, max_length=500)
    trailer_url: Optional[str] = Field(None, max_length=500)


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    local_title: Optional[str] = Field(None, max_length=500)
    release_date: Optional[date] = None
    runtime: Optional[int] = Field(None, gt=0)
    plot_summary: Optional[str] = None
    director: Optional[str] = Field(None, max_length=255)
    producer: Optional[str] = Field(None, max_length=255)
    production_company: Optional[str] = Field(None, max_length=255)
    production_state: Optional[str] = Field(None, max_length=100)
    box_office_ng: Optional[str] = Field(None, max_length=100)
    poster_url: Optional[str] = Field(None, max_length=500)
    trailer_url: Optional[str] = Field(None, max_length=500)
    genres: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    cast: Optional[List[CastMember]] = None


class MovieStats(BaseModel):
    average_rating: float = 0.0
    review_count: int = 0
    rating_distribution: Dict[int, int] = {}
    cultural_authenticity_avg: float = 0.0
    production_quality_avg: float = 0.0
    story_rating_avg: float = 0.0
    acting_rating_avg: float = 0.0
    cinematography_rating_avg: float = 0.0


class MovieResponse(MovieBase):
    id: UUID
    genres: List[str] = []
    languages: List[str] = []
    cast: List[CastMember] = []
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    stats: MovieStats
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MovieListResponse(BaseModel):
    id: UUID
    title: str
    local_title: Optional[str] = None
    release_date: date
    director: Optional[str] = None
    poster_url: Optional[str] = None
    type: ContentType
    genres: List[str] = []
    stats: MovieStats
    created_at: datetime

    class Config:
        from_attributes = True


class MovieSearchFilters(BaseModel):
    genre: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=2030)
    rating_min: Optional[float] = Field(None, ge=0.0, le=10.0)
    rating_max: Optional[float] = Field(None, ge=0.0, le=10.0)
    language: Optional[str] = None
    director: Optional[str] = None
    production_state: Optional[str] = None
    type: Optional[ContentType] = None


class MovieSortBy(BaseModel):
    field: str = Field("created_at", pattern="^(title|release_date|rating|review_count|created_at)$")
    order: str = Field("desc", pattern="^(asc|desc)$")


class MovieListRequest(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    filters: Optional[MovieSearchFilters] = None
    sort_by: Optional[MovieSortBy] = None


class PaginatedMovieResponse(BaseModel):
    items: List[MovieListResponse]
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
    has_prev: bool