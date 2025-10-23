"""
Search service for LemonNPie Backend API
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text, or_, and_, desc
from sqlalchemy.orm import selectinload

from app.models.movie import Movie
from app.models.search import MovieSearchIndex
from app.models.relationships import MovieGenre, MovieLanguage, MovieCast
from app.schemas.movie import MovieListResponse, MovieStats
from app.services.movie_service import MovieService
from app.cache.redis import get_search_cache_service
import json
import hashlib


class SearchService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.movie_service = MovieService(db)

    async def search_movies(
        self, 
        query: str, 
        filters: Optional[Dict] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[MovieListResponse]:
        """
        Advanced movie search using PostgreSQL full-text search with fallback to LIKE search
        """
        # Try to get from cache first
        query_hash = self._generate_query_hash(query, filters, limit, offset)
        search_cache = await get_search_cache_service()
        cached_result = await search_cache.get_search_results(query_hash)
        
        if cached_result:
            return [MovieListResponse(**movie_data) for movie_data in cached_result]
        
        # Build search query
        search_query = select(Movie).options(
            selectinload(Movie.genres),
            selectinload(Movie.languages),
            selectinload(Movie.cast),
            selectinload(Movie.reviews)
        )
        
        # Add search conditions
        search_conditions = []
        
        if query and query.strip():
            # Use LIKE search for SQLite compatibility
            search_term = f"%{query.strip()}%"
            search_conditions.append(
                or_(
                    Movie.title.ilike(search_term),
                    Movie.local_title.ilike(search_term),
                    Movie.director.ilike(search_term),
                    Movie.producer.ilike(search_term),
                    Movie.production_company.ilike(search_term),
                    Movie.plot_summary.ilike(search_term)
                )
            )
        
        # Add filters
        if filters:
            if filters.get("genre"):
                genre_subquery = select(MovieGenre.movie_id).where(MovieGenre.genre == filters["genre"])
                search_conditions.append(Movie.id.in_(genre_subquery))
            
            if filters.get("year"):
                search_conditions.append(func.extract('year', Movie.release_date) == filters["year"])
            
            if filters.get("language"):
                lang_subquery = select(MovieLanguage.movie_id).where(MovieLanguage.language == filters["language"])
                search_conditions.append(Movie.id.in_(lang_subquery))
            
            if filters.get("director"):
                search_conditions.append(Movie.director.ilike(f"%{filters['director']}%"))
            
            if filters.get("production_state"):
                search_conditions.append(Movie.production_state.ilike(f"%{filters['production_state']}%"))
            
            if filters.get("rating_min"):
                # This would require a subquery to calculate average ratings
                pass  # Skip for now, can be added later
        
        if search_conditions:
            search_query = search_query.where(and_(*search_conditions))
        
        # Order by relevance (for now, just by title similarity and then by rating)
        search_query = search_query.order_by(Movie.title, desc(Movie.created_at))
        
        # Apply pagination
        search_query = search_query.offset(offset).limit(limit)
        
        # Execute query
        result = await self.db.execute(search_query)
        movies = result.scalars().all()
        
        # Convert to response format
        movie_responses = []
        for movie in movies:
            stats = await self.movie_service._calculate_movie_stats(movie)
            movie_response = MovieListResponse(
                id=movie.id,
                title=movie.title,
                local_title=movie.local_title,
                release_date=movie.release_date,
                director=movie.director,
                poster_url=movie.poster_url,
                type=movie.type,
                genres=[genre.genre for genre in movie.genres],
                stats=stats,
                created_at=movie.created_at
            )
            movie_responses.append(movie_response)
        
        # Cache the result
        await search_cache.set_search_results(query_hash, [movie.dict() for movie in movie_responses])
        
        return movie_responses

    async def suggest_movies(self, partial_query: str, limit: int = 5) -> List[str]:
        """
        Provide search suggestions using similarity matching
        """
        if not partial_query or len(partial_query.strip()) < 2:
            return []
        
        # Try to get from cache first
        search_cache = await get_search_cache_service()
        cached_result = await search_cache.get_search_suggestions(partial_query.strip())
        if cached_result:
            return cached_result[:limit]
        
        search_term = f"%{partial_query.strip()}%"
        
        # Query for movie titles that match the partial query
        query = select(Movie.title).where(
            or_(
                Movie.title.ilike(search_term),
                Movie.local_title.ilike(search_term)
            )
        ).distinct().limit(limit)
        
        result = await self.db.execute(query)
        suggestions = [row[0] for row in result.fetchall()]
        
        # Cache the result
        await search_cache.set_search_suggestions(partial_query.strip(), suggestions)
        
        return suggestions

    async def get_popular_searches(self, limit: int = 10) -> List[str]:
        """
        Get popular search terms (for now, return popular movie titles)
        """
        search_cache = await get_search_cache_service()
        cached_result = await search_cache.get_popular_searches()
        if cached_result:
            return cached_result[:limit]
        
        # Get movies with most reviews as popular searches
        query = select(Movie.title).outerjoin(Movie.reviews).group_by(
            Movie.id, Movie.title
        ).order_by(
            desc(func.count(Movie.reviews))
        ).limit(limit)
        
        result = await self.db.execute(query)
        popular_searches = [row[0] for row in result.fetchall()]
        
        # Cache the result
        await search_cache.set_popular_searches(popular_searches)
        
        return popular_searches

    async def search_by_cast(self, actor_name: str, limit: int = 20) -> List[MovieListResponse]:
        """
        Search movies by cast member name
        """
        query_hash = f"cast:{hashlib.md5(actor_name.encode()).hexdigest()}:{limit}"
        search_cache = await get_search_cache_service()
        cached_result = await search_cache.get_search_results(query_hash)
        if cached_result:
            return [MovieListResponse(**movie_data) for movie_data in cached_result]
        
        # Find movies with the specified actor
        cast_subquery = select(MovieCast.movie_id).where(
            MovieCast.actor_name.ilike(f"%{actor_name}%")
        )
        
        query = select(Movie).options(
            selectinload(Movie.genres),
            selectinload(Movie.languages),
            selectinload(Movie.cast),
            selectinload(Movie.reviews)
        ).where(
            Movie.id.in_(cast_subquery)
        ).order_by(desc(Movie.created_at)).limit(limit)
        
        result = await self.db.execute(query)
        movies = result.scalars().all()
        
        # Convert to response format
        movie_responses = []
        for movie in movies:
            stats = await self.movie_service._calculate_movie_stats(movie)
            movie_response = MovieListResponse(
                id=movie.id,
                title=movie.title,
                local_title=movie.local_title,
                release_date=movie.release_date,
                director=movie.director,
                poster_url=movie.poster_url,
                type=movie.type,
                genres=[genre.genre for genre in movie.genres],
                stats=stats,
                created_at=movie.created_at
            )
            movie_responses.append(movie_response)
        
        # Cache the result
        await search_cache.set_search_results(query_hash, [movie.dict() for movie in movie_responses])
        
        return movie_responses

    def _generate_query_hash(self, query: str, filters: Optional[Dict], limit: int, offset: int) -> str:
        """Generate hash for search query parameters"""
        key_data = {
            "query": query,
            "filters": filters or {},
            "limit": limit,
            "offset": offset
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()