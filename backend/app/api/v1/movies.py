"""
Movie API endpoints for LemonNPie Backend API
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.auth.dependencies import get_current_user, require_admin
from app.models.user import User
from app.services.movie_service import MovieService
from app.services.search_service import SearchService
from app.schemas.movie import (
    MovieCreate, MovieUpdate, MovieResponse, MovieListResponse,
    PaginatedMovieResponse, MovieSearchFilters, MovieSortBy, MovieListRequest
)
from app.core.exceptions import NotFoundError, ValidationError

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=PaginatedMovieResponse)
async def get_movies(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    # Filters
    genre: str = Query(None, description="Filter by genre"),
    year: int = Query(None, ge=1900, le=2030, description="Filter by release year"),
    rating_min: float = Query(None, ge=0.0, le=10.0, description="Minimum rating"),
    rating_max: float = Query(None, ge=0.0, le=10.0, description="Maximum rating"),
    language: str = Query(None, description="Filter by language"),
    director: str = Query(None, description="Filter by director name"),
    production_state: str = Query(None, description="Filter by production state"),
    # Sorting
    sort_field: str = Query("created_at", pattern="^(title|release_date|rating|review_count|created_at)$", description="Sort field"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$", description="Sort order"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get paginated list of movies with filtering and sorting options.
    
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 20, max: 100)
    - **genre**: Filter by genre
    - **year**: Filter by release year
    - **rating_min**: Minimum rating filter
    - **rating_max**: Maximum rating filter
    - **language**: Filter by language
    - **director**: Filter by director name (partial match)
    - **production_state**: Filter by production state
    - **sort_field**: Field to sort by (title, release_date, rating, review_count, created_at)
    - **sort_order**: Sort order (asc, desc)
    """
    try:
        # Build filters
        filters = MovieSearchFilters(
            genre=genre,
            year=year,
            rating_min=rating_min,
            rating_max=rating_max,
            language=language,
            director=director,
            production_state=production_state
        )
        
        # Build sort options
        sort_by = MovieSortBy(field=sort_field, order=sort_order)
        
        movie_service = MovieService(db)
        return await movie_service.get_movies(
            page=page,
            limit=limit,
            filters=filters,
            sort_by=sort_by
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending", response_model=List[MovieListResponse])
async def get_trending_movies(
    limit: int = Query(10, ge=1, le=50, description="Number of trending movies to return"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get trending movies based on recent review activity.
    
    - **limit**: Number of movies to return (default: 10, max: 50)
    """
    try:
        movie_service = MovieService(db)
        return await movie_service.get_trending_movies(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/featured", response_model=List[MovieListResponse])
async def get_featured_movies(
    limit: int = Query(10, ge=1, le=50, description="Number of featured movies to return"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get featured movies based on high ratings and review count.
    
    - **limit**: Number of movies to return (default: 10, max: 50)
    """
    try:
        movie_service = MovieService(db)
        return await movie_service.get_featured_movies(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=List[MovieListResponse])
async def search_movies(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    # Filters
    genre: str = Query(None, description="Filter by genre"),
    year: int = Query(None, ge=1900, le=2030, description="Filter by release year"),
    language: str = Query(None, description="Filter by language"),
    director: str = Query(None, description="Filter by director name"),
    production_state: str = Query(None, description="Filter by production state"),
    db: AsyncSession = Depends(get_db)
):
    """
    Search movies with advanced filtering and ranking.
    
    - **q**: Search query (required)
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 20, max: 100)
    - **genre**: Filter by genre
    - **year**: Filter by release year
    - **language**: Filter by language
    - **director**: Filter by director name (partial match)
    - **production_state**: Filter by production state
    """
    try:
        # Build filters
        filters = {}
        if genre:
            filters["genre"] = genre
        if year:
            filters["year"] = year
        if language:
            filters["language"] = language
        if director:
            filters["director"] = director
        if production_state:
            filters["production_state"] = production_state
        
        search_service = SearchService(db)
        offset = (page - 1) * limit
        
        return await search_service.search_movies(
            query=q,
            filters=filters if filters else None,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=2, description="Partial search query"),
    limit: int = Query(5, ge=1, le=20, description="Number of suggestions"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get search suggestions based on partial query.
    
    - **q**: Partial search query (minimum 2 characters)
    - **limit**: Number of suggestions (default: 5, max: 20)
    """
    try:
        search_service = SearchService(db)
        suggestions = await search_service.suggest_movies(q, limit)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/popular")
async def get_popular_searches(
    limit: int = Query(10, ge=1, le=50, description="Number of popular searches"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get popular search terms.
    
    - **limit**: Number of popular searches (default: 10, max: 50)
    """
    try:
        search_service = SearchService(db)
        popular_searches = await search_service.get_popular_searches(limit)
        return {"popular_searches": popular_searches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/by-cast", response_model=List[MovieListResponse])
async def search_movies_by_cast(
    actor: str = Query(..., min_length=2, description="Actor name"),
    limit: int = Query(20, ge=1, le=100, description="Number of movies to return"),
    db: AsyncSession = Depends(get_db)
):
    """
    Search movies by cast member name.
    
    - **actor**: Actor name (minimum 2 characters)
    - **limit**: Number of movies (default: 20, max: 100)
    """
    try:
        search_service = SearchService(db)
        return await search_service.search_by_cast(actor, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(
    movie_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get movie by ID with full details and statistics.
    
    - **movie_id**: UUID of the movie
    """
    try:
        movie_service = MovieService(db)
        return await movie_service.get_movie_by_id(movie_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=MovieResponse)
async def create_movie(
    movie_data: MovieCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new movie (Admin only).
    
    - **movie_data**: Movie creation data
    """
    try:
        movie_service = MovieService(db)
        return await movie_service.create_movie(movie_data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie(
    movie_id: UUID,
    movie_data: MovieUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update an existing movie (Admin only).
    
    - **movie_id**: UUID of the movie to update
    - **movie_data**: Movie update data
    """
    try:
        movie_service = MovieService(db)
        return await movie_service.update_movie(movie_id, movie_data)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{movie_id}")
async def delete_movie(
    movie_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete a movie (Admin only).
    
    - **movie_id**: UUID of the movie to delete
    """
    try:
        movie_service = MovieService(db)
        success = await movie_service.delete_movie(movie_id)
        if success:
            return {"message": "Movie deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete movie")
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{movie_id}/stats", response_model=dict)
async def get_movie_stats(
    movie_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed statistics for a movie.
    
    - **movie_id**: UUID of the movie
    """
    try:
        movie_service = MovieService(db)
        movie = await movie_service.get_movie_by_id(movie_id)
        return {
            "movie_id": movie_id,
            "title": movie.title,
            "stats": movie.stats
        }
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{movie_id}/reviews")
async def get_movie_reviews(
    movie_id: UUID,
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get reviews for a specific movie with pagination.
    
    - **movie_id**: UUID of the movie
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 20, max: 100)
    """
    try:
        movie_service = MovieService(db)
        # First verify the movie exists
        await movie_service.get_movie_by_id(movie_id)
        
        # Get reviews for the movie
        reviews = await movie_service.get_movie_reviews(movie_id, page, limit)
        return reviews
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

