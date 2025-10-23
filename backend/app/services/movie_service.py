"""
Movie service for LemonNPie Backend API
"""
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc, asc, delete
from sqlalchemy.orm import selectinload, joinedload

from app.models.movie import Movie
from app.models.relationships import MovieGenre, MovieLanguage, MovieCast
from app.models.review import Review
from app.schemas.movie import (
    MovieCreate, MovieUpdate, MovieResponse, MovieListResponse, 
    MovieSearchFilters, MovieSortBy, PaginatedMovieResponse, MovieStats, CastMember
)
from app.models.enums import ModerationStatus
from app.core.exceptions import NotFoundError, ValidationError
from app.cache.redis import get_movie_cache_service, get_review_cache_service
from app.db.optimization import OptimizedQueries
from app.services.performance_service import monitor_performance


class MovieService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_movies(
        self, 
        page: int = 1, 
        limit: int = 20,
        filters: Optional[MovieSearchFilters] = None,
        sort_by: Optional[MovieSortBy] = None
    ) -> PaginatedMovieResponse:
        """Get paginated list of movies with filtering and sorting"""
        
        # Build base query
        query = select(Movie).options(
            selectinload(Movie.genres),
            selectinload(Movie.languages),
            selectinload(Movie.cast),
            selectinload(Movie.reviews)
        )
        
        # Apply filters
        if filters:
            conditions = []
            
            if filters.genre:
                genre_subquery = select(MovieGenre.movie_id).where(MovieGenre.genre == filters.genre)
                conditions.append(Movie.id.in_(genre_subquery))
            
            if filters.year:
                conditions.append(func.extract('year', Movie.release_date) == filters.year)
            
            if filters.language:
                lang_subquery = select(MovieLanguage.movie_id).where(MovieLanguage.language == filters.language)
                conditions.append(Movie.id.in_(lang_subquery))
            
            if filters.director:
                conditions.append(Movie.director.ilike(f"%{filters.director}%"))
            
            if filters.production_state:
                conditions.append(Movie.production_state.ilike(f"%{filters.production_state}%"))
            
            if filters.type:
                conditions.append(Movie.type == filters.type)
            
            # Add rating filters if provided
            if filters.rating_min is not None or filters.rating_max is not None:
                # We need to join with reviews to filter by rating
                avg_rating_subquery = (
                    select(Review.movie_id)
                    .group_by(Review.movie_id)
                    .having(
                        and_(
                            func.avg(Review.lemon_pie_rating) >= (filters.rating_min or 0),
                            func.avg(Review.lemon_pie_rating) <= (filters.rating_max or 10)
                        )
                    )
                )
                conditions.append(Movie.id.in_(avg_rating_subquery))
            
            if conditions:
                query = query.where(and_(*conditions))
        
        # Apply sorting
        if sort_by:
            if sort_by.field == "title":
                order_field = Movie.title
            elif sort_by.field == "release_date":
                order_field = Movie.release_date
            elif sort_by.field == "created_at":
                order_field = Movie.created_at
            elif sort_by.field == "rating":
                # For rating, we need to join with reviews and calculate average
                avg_rating = func.coalesce(func.avg(Review.lemon_pie_rating), 0).label('avg_rating')
                query = query.outerjoin(Review).group_by(Movie.id)
                order_field = avg_rating
            elif sort_by.field == "review_count":
                # For review count, we need to count reviews
                review_count = func.count(Review.id).label('review_count')
                query = query.outerjoin(Review).group_by(Movie.id)
                order_field = review_count
            else:
                order_field = Movie.created_at
            
            if sort_by.order == "asc":
                query = query.order_by(asc(order_field))
            else:
                query = query.order_by(desc(order_field))
        else:
            query = query.order_by(desc(Movie.created_at))
        
        # Get total count - use a simpler approach for count
        count_query = select(func.count(Movie.id))
        if filters:
            count_conditions = []
            
            if filters.genre:
                genre_subquery = select(MovieGenre.movie_id).where(MovieGenre.genre == filters.genre)
                count_conditions.append(Movie.id.in_(genre_subquery))
            
            if filters.year:
                count_conditions.append(func.extract('year', Movie.release_date) == filters.year)
            
            if filters.language:
                lang_subquery = select(MovieLanguage.movie_id).where(MovieLanguage.language == filters.language)
                count_conditions.append(Movie.id.in_(lang_subquery))
            
            if filters.director:
                count_conditions.append(Movie.director.ilike(f"%{filters.director}%"))
            
            if filters.production_state:
                count_conditions.append(Movie.production_state.ilike(f"%{filters.production_state}%"))
            
            if filters.type:
                count_conditions.append(Movie.type == filters.type)
            
            # Add rating filters for count
            if filters.rating_min is not None or filters.rating_max is not None:
                avg_rating_subquery = (
                    select(Review.movie_id)
                    .group_by(Review.movie_id)
                    .having(
                        and_(
                            func.avg(Review.lemon_pie_rating) >= (filters.rating_min or 0),
                            func.avg(Review.lemon_pie_rating) <= (filters.rating_max or 10)
                        )
                    )
                )
                count_conditions.append(Movie.id.in_(avg_rating_subquery))
            
            if count_conditions:
                count_query = count_query.where(and_(*count_conditions))
        
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Apply pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        movies = result.scalars().all()
        
        # Convert to response format with stats
        movie_responses = []
        for movie in movies:
            stats = await self._calculate_movie_stats(movie)
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
        
        # Calculate pagination info
        pages = (total + limit - 1) // limit
        has_next = page < pages
        has_prev = page > 1
        
        return PaginatedMovieResponse(
            items=movie_responses,
            total=total,
            page=page,
            limit=limit,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev
        )

    async def get_movie_by_id(self, movie_id: UUID) -> MovieResponse:
        """Get movie by ID with full details and statistics"""
        
        # Try to get from cache first
        movie_cache = await get_movie_cache_service()
        cached_movie = await movie_cache.get_movie(str(movie_id))
        
        if cached_movie:
            # Convert cached data back to MovieResponse
            return MovieResponse(**cached_movie)
        
        query = select(Movie).options(
            selectinload(Movie.genres),
            selectinload(Movie.languages),
            selectinload(Movie.cast),
            selectinload(Movie.reviews)
        ).where(Movie.id == movie_id)
        
        result = await self.db.execute(query)
        movie = result.scalar_one_or_none()
        
        if not movie:
            raise NotFoundError(f"Movie with id {movie_id} not found")
        
        # Calculate statistics
        stats = await self._calculate_movie_stats(movie)
        
        # Convert cast to response format
        cast_members = [
            CastMember(
                actor_name=cast.actor_name,
                character_name=cast.character_name,
                role_type=cast.role_type
            )
            for cast in movie.cast
        ]
        
        movie_response = MovieResponse(
            id=movie.id,
            title=movie.title,
            local_title=movie.local_title,
            release_date=movie.release_date,
            runtime=movie.runtime,
            plot_summary=movie.plot_summary,
            director=movie.director,
            producer=movie.producer,
            production_company=movie.production_company,
            production_state=movie.production_state,
            box_office_ng=movie.box_office_ng,
            type=movie.type,
            poster_url=movie.poster_url,
            trailer_url=movie.trailer_url,
            genres=[genre.genre for genre in movie.genres],
            languages=[lang.language for lang in movie.languages],
            cast=cast_members,
            stats=stats,
            created_at=movie.created_at,
            updated_at=movie.updated_at
        )
        
        # Cache the result
        await movie_cache.set_movie(str(movie_id), movie_response.dict())
        
        return movie_response

    async def create_movie(self, movie_data: MovieCreate) -> MovieResponse:
        """Create a new movie"""
        
        # Create movie instance
        movie = Movie(
            title=movie_data.title,
            local_title=movie_data.local_title,
            release_date=movie_data.release_date,
            runtime=movie_data.runtime,
            plot_summary=movie_data.plot_summary,
            director=movie_data.director,
            producer=movie_data.producer,
            production_company=movie_data.production_company,
            production_state=movie_data.production_state,
            box_office_ng=movie_data.box_office_ng,
            type=movie_data.type,
            poster_url=movie_data.poster_url,
            trailer_url=movie_data.trailer_url
        )
        
        self.db.add(movie)
        await self.db.flush()  # Get the movie ID
        
        # Add genres
        for genre in movie_data.genres:
            movie_genre = MovieGenre(movie_id=movie.id, genre=genre)
            self.db.add(movie_genre)
        
        # Add languages
        for language in movie_data.languages:
            movie_language = MovieLanguage(movie_id=movie.id, language=language)
            self.db.add(movie_language)
        
        # Add cast
        for cast_member in movie_data.cast:
            movie_cast = MovieCast(
                movie_id=movie.id,
                actor_name=cast_member.actor_name,
                character_name=cast_member.character_name,
                role_type=cast_member.role_type
            )
            self.db.add(movie_cast)
        
        await self.db.commit()
        await self.db.refresh(movie)
        
        # Invalidate movie lists cache since we added a new movie
        movie_cache = await get_movie_cache_service()
        await movie_cache.invalidate_movie_lists()
        
        return await self.get_movie_by_id(movie.id)

    async def update_movie(self, movie_id: UUID, movie_data: MovieUpdate) -> MovieResponse:
        """Update an existing movie"""
        
        # Get existing movie
        query = select(Movie).where(Movie.id == movie_id)
        result = await self.db.execute(query)
        movie = result.scalar_one_or_none()
        
        if not movie:
            raise NotFoundError(f"Movie with id {movie_id} not found")
        
        # Update movie fields
        update_data = movie_data.dict(exclude_unset=True, exclude={'genres', 'languages', 'cast'})
        for field, value in update_data.items():
            setattr(movie, field, value)
        
        # Update genres if provided
        if movie_data.genres is not None:
            # Delete existing genres
            from sqlalchemy import delete
            await self.db.execute(
                delete(MovieGenre).where(MovieGenre.movie_id == movie_id)
            )
            # Add new genres
            for genre in movie_data.genres:
                movie_genre = MovieGenre(movie_id=movie.id, genre=genre)
                self.db.add(movie_genre)
        
        # Update languages if provided
        if movie_data.languages is not None:
            # Delete existing languages
            await self.db.execute(
                delete(MovieLanguage).where(MovieLanguage.movie_id == movie_id)
            )
            # Add new languages
            for language in movie_data.languages:
                movie_language = MovieLanguage(movie_id=movie.id, language=language)
                self.db.add(movie_language)
        
        # Update cast if provided
        if movie_data.cast is not None:
            # Delete existing cast
            await self.db.execute(
                delete(MovieCast).where(MovieCast.movie_id == movie_id)
            )
            # Add new cast
            for cast_member in movie_data.cast:
                movie_cast = MovieCast(
                    movie_id=movie.id,
                    actor_name=cast_member.actor_name,
                    character_name=cast_member.character_name,
                    role_type=cast_member.role_type
                )
                self.db.add(movie_cast)
        
        await self.db.commit()
        await self.db.refresh(movie)
        
        # Invalidate caches for this movie and movie lists
        movie_cache = await get_movie_cache_service()
        await movie_cache.invalidate_movie(str(movie_id))
        await movie_cache.invalidate_movie_lists()
        
        return await self.get_movie_by_id(movie.id)

    async def delete_movie(self, movie_id: UUID) -> bool:
        """Delete a movie"""
        
        query = select(Movie).where(Movie.id == movie_id)
        result = await self.db.execute(query)
        movie = result.scalar_one_or_none()
        
        if not movie:
            raise NotFoundError(f"Movie with id {movie_id} not found")
        
        await self.db.delete(movie)
        await self.db.commit()
        
        # Invalidate caches for this movie and movie lists
        movie_cache = await get_movie_cache_service()
        await movie_cache.invalidate_movie(str(movie_id))
        await movie_cache.invalidate_movie_lists()
        
        return True

    @monitor_performance("calculate_movie_stats")
    async def _calculate_movie_stats(self, movie: Movie) -> MovieStats:
        """Calculate statistics for a movie with performance monitoring"""
        
        # Try to get from cache first
        movie_cache = await get_movie_cache_service()
        cached_stats = await movie_cache.get_movie_stats(str(movie.id))
        
        if cached_stats:
            return MovieStats(**cached_stats)
        
        if not movie.reviews:
            empty_stats = MovieStats()
            await movie_cache.set_movie_stats(str(movie.id), empty_stats.dict())
            return empty_stats
        
        reviews = movie.reviews
        review_count = len(reviews)
        
        if review_count == 0:
            empty_stats = MovieStats()
            await movie_cache.set_movie_stats(str(movie.id), empty_stats.dict())
            return empty_stats
        
        # Calculate averages
        total_rating = sum(review.lemon_pie_rating for review in reviews)
        average_rating = total_rating / review_count
        
        cultural_authenticity_total = sum(
            review.cultural_authenticity_rating for review in reviews 
            if review.cultural_authenticity_rating is not None
        )
        cultural_authenticity_count = sum(
            1 for review in reviews 
            if review.cultural_authenticity_rating is not None
        )
        cultural_authenticity_avg = (
            cultural_authenticity_total / cultural_authenticity_count 
            if cultural_authenticity_count > 0 else 0.0
        )
        
        production_quality_total = sum(
            review.production_quality_rating for review in reviews 
            if review.production_quality_rating is not None
        )
        production_quality_count = sum(
            1 for review in reviews 
            if review.production_quality_rating is not None
        )
        production_quality_avg = (
            production_quality_total / production_quality_count 
            if production_quality_count > 0 else 0.0
        )
        
        story_rating_total = sum(
            review.story_rating for review in reviews 
            if review.story_rating is not None
        )
        story_rating_count = sum(
            1 for review in reviews 
            if review.story_rating is not None
        )
        story_rating_avg = (
            story_rating_total / story_rating_count 
            if story_rating_count > 0 else 0.0
        )
        
        acting_rating_total = sum(
            review.acting_rating for review in reviews 
            if review.acting_rating is not None
        )
        acting_rating_count = sum(
            1 for review in reviews 
            if review.acting_rating is not None
        )
        acting_rating_avg = (
            acting_rating_total / acting_rating_count 
            if acting_rating_count > 0 else 0.0
        )
        
        cinematography_rating_total = sum(
            review.cinematography_rating for review in reviews 
            if review.cinematography_rating is not None
        )
        cinematography_rating_count = sum(
            1 for review in reviews 
            if review.cinematography_rating is not None
        )
        cinematography_rating_avg = (
            cinematography_rating_total / cinematography_rating_count 
            if cinematography_rating_count > 0 else 0.0
        )
        
        # Calculate rating distribution
        rating_distribution = {}
        for i in range(1, 11):
            rating_distribution[i] = sum(
                1 for review in reviews 
                if review.lemon_pie_rating == i
            )
        
        movie_stats = MovieStats(
            average_rating=round(average_rating, 2),
            review_count=review_count,
            rating_distribution=rating_distribution,
            cultural_authenticity_avg=round(cultural_authenticity_avg, 2),
            production_quality_avg=round(production_quality_avg, 2),
            story_rating_avg=round(story_rating_avg, 2),
            acting_rating_avg=round(acting_rating_avg, 2),
            cinematography_rating_avg=round(cinematography_rating_avg, 2)
        )
        
        # Cache the result
        await movie_cache.set_movie_stats(str(movie.id), movie_stats.dict())
        
        return movie_stats

    async def get_trending_movies(self, limit: int = 10) -> List[MovieListResponse]:
        """Get trending movies based on recent review activity"""
        
        # Try to get from cache first
        movie_cache = await get_movie_cache_service()
        cached_trending = await movie_cache.get_trending_movies()
        
        if cached_trending:
            # Convert cached data back to MovieListResponse objects
            return [MovieListResponse(**movie_data) for movie_data in cached_trending[:limit]]
        
        # Get movies with recent reviews (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        query = select(Movie).options(
            selectinload(Movie.genres),
            selectinload(Movie.reviews)
        ).join(Review).where(
            Review.created_at >= thirty_days_ago
        ).group_by(Movie.id).order_by(
            desc(func.count(Review.id))
        ).limit(limit)
        
        result = await self.db.execute(query)
        movies = result.scalars().all()
        
        movie_responses = []
        for movie in movies:
            stats = await self._calculate_movie_stats(movie)
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
        await movie_cache.set_trending_movies([movie.dict() for movie in movie_responses])
        
        return movie_responses

    async def get_movie_reviews(self, movie_id: UUID, page: int = 1, limit: int = 20):
        """Get paginated reviews for a specific movie"""
        
        # Try to get from cache first
        movie_cache = await get_movie_cache_service()
        cached_reviews = await movie_cache.get_movie_reviews(str(movie_id), page, limit)
        
        if cached_reviews:
            return cached_reviews
        
        # Build query for reviews
        query = select(Review).options(
            selectinload(Review.user),
            selectinload(Review.votes)
        ).where(
            Review.movie_id == movie_id,
            Review.moderation_status == ModerationStatus.APPROVED
        ).order_by(desc(Review.created_at))
        
        # Get total count
        count_query = select(func.count(Review.id)).where(
            Review.movie_id == movie_id,
            Review.moderation_status == ModerationStatus.APPROVED
        )
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0
        
        # Apply pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)
        
        # Execute query
        result = await self.db.execute(query)
        reviews = result.scalars().all()
        
        # Convert to response format
        review_responses = []
        for review in reviews:
            user_data = {
                "id": review.user.id,
                "name": review.user.name,
                "role": review.user.role.value,
                "is_verified": review.user.is_verified,
                "avatar_url": review.user.avatar_url
            }
            
            review_response = {
                "id": review.id,
                "user": user_data,
                "movie_id": review.movie_id,
                "lemon_pie_rating": review.lemon_pie_rating,
                "review_text": review.review_text,
                "spoiler_warning": review.spoiler_warning,
                "cultural_authenticity_rating": review.cultural_authenticity_rating,
                "production_quality_rating": review.production_quality_rating,
                "story_rating": review.story_rating,
                "acting_rating": review.acting_rating,
                "cinematography_rating": review.cinematography_rating,
                "helpful_votes": review.helpful_votes,
                "unhelpful_votes": review.unhelpful_votes,
                "helpfulness_score": review.helpful_votes - review.unhelpful_votes,
                "created_at": review.created_at,
                "updated_at": review.updated_at
            }
            review_responses.append(review_response)
        
        # Calculate pagination info
        pages = (total + limit - 1) // limit
        has_next = page < pages
        has_prev = page > 1
        
        result_data = {
            "items": review_responses,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
            "has_next": has_next,
            "has_prev": has_prev
        }
        
        # Cache the result
        await movie_cache.set_movie_reviews(str(movie_id), page, limit, result_data)
        
        return result_data

    async def get_featured_movies(self, limit: int = 10) -> List[MovieListResponse]:
        """Get featured movies based on high ratings and review count"""
        
        # Try to get from cache first
        movie_cache = await get_movie_cache_service()
        cached_featured = await movie_cache.get_featured_movies()
        
        if cached_featured:
            # Convert cached data back to MovieListResponse objects
            return [MovieListResponse(**movie_data) for movie_data in cached_featured[:limit]]
        
        query = select(Movie).options(
            selectinload(Movie.genres),
            selectinload(Movie.reviews)
        ).outerjoin(Review).group_by(Movie.id).having(
            func.count(Review.id) >= 5  # At least 5 reviews
        ).order_by(
            desc(func.avg(Review.lemon_pie_rating))
        ).limit(limit)
        
        result = await self.db.execute(query)
        movies = result.scalars().all()
        
        movie_responses = []
        for movie in movies:
            stats = await self._calculate_movie_stats(movie)
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
        await movie_cache.set_featured_movies([movie.dict() for movie in movie_responses])
        
        return movie_responses