"""
Tests for movie service functionality
"""
import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from datetime import date

from app.services.movie_service import MovieService
from app.models.movie import Movie, ContentType
from app.models.relationships import MovieGenre, MovieLanguage, MovieCast
from app.models.review import Review, ModerationStatus
from app.models.enums import CastRole
from app.schemas.movie import MovieCreate, MovieUpdate, MovieStats


class TestMovieService:
    """Test movie service functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.movie_service = MovieService()
        self.test_movie_id = uuid4()
        self.test_user_id = uuid4()
    
    @pytest.mark.asyncio
    async def test_create_movie_success(self):
        """Test successful movie creation"""
        mock_db = AsyncMock()
        
        movie_data = MovieCreate(
            title="Test Movie",
            local_title="Test Local Title",
            release_date=date(2023, 1, 1),
            runtime=120,
            plot_summary="Test plot",
            director="Test Director",
            producer="Test Producer",
            production_company="Test Company",
            production_state="Lagos",
            genres=["Action", "Drama"],
            languages=["English", "Yoruba"],
            cast=[
                {
                    "actor_name": "Test Actor",
                    "character_name": "Test Character",
                    "role_type": "actor"
                }
            ]
        )
        
        # Mock movie creation
        with patch('app.services.movie_service.Movie') as mock_movie_class:
            mock_movie = Movie(
                id=self.test_movie_id,
                title="Test Movie",
                director="Test Director",
                type=ContentType.MOVIE
            )
            mock_movie_class.return_value = mock_movie
            
            created_movie = await self.movie_service.create_movie(movie_data, mock_db)
            
            assert created_movie.title == "Test Movie"
            assert created_movie.director == "Test Director"
            mock_db.add.assert_called()
            mock_db.commit.assert_called()
    
    @pytest.mark.asyncio
    async def test_get_movie_by_id_success(self):
        """Test successful movie retrieval by ID"""
        mock_db = AsyncMock()
        
        # Mock movie with relationships
        mock_movie = Movie(
            id=self.test_movie_id,
            title="Test Movie",
            director="Test Director",
            type=ContentType.MOVIE
        )
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_movie
        mock_db.execute.return_value = mock_result
        
        movie = await self.movie_service.get_movie_by_id(self.test_movie_id, mock_db)
        
        assert movie.id == self.test_movie_id
        assert movie.title == "Test Movie"
        assert movie.director == "Test Director"
    
    @pytest.mark.asyncio
    async def test_get_movie_by_id_not_found(self):
        """Test movie not found by ID"""
        from fastapi import HTTPException
        
        mock_db = AsyncMock()
        
        # Mock movie not found
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        
        with pytest.raises(HTTPException) as exc_info:
            await self.movie_service.get_movie_by_id(self.test_movie_id, mock_db)
        
        assert exc_info.value.status_code == 404
        assert "Movie not found" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_update_movie_success(self):
        """Test successful movie update"""
        mock_db = AsyncMock()
        
        # Mock existing movie
        mock_movie = Movie(
            id=self.test_movie_id,
            title="Old Title",
            director="Old Director",
            type=ContentType.MOVIE
        )
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_movie
        mock_db.execute.return_value = mock_result
        
        # Update data
        update_data = MovieUpdate(
            title="New Title",
            director="New Director",
            genres=["Comedy", "Romance"]
        )
        
        updated_movie = await self.movie_service.update_movie(
            self.test_movie_id, update_data, mock_db
        )
        
        assert updated_movie.title == "New Title"
        assert updated_movie.director == "New Director"
        mock_db.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_delete_movie_success(self):
        """Test successful movie deletion"""
        mock_db = AsyncMock()
        
        # Mock existing movie
        mock_movie = Movie(
            id=self.test_movie_id,
            title="To Delete",
            type=ContentType.MOVIE
        )
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_movie
        mock_db.execute.return_value = mock_result
        
        result = await self.movie_service.delete_movie(self.test_movie_id, mock_db)
        
        assert result["message"] == "Movie deleted successfully"
        mock_db.delete.assert_called_once_with(mock_movie)
        mock_db.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_movies_with_filters(self):
        """Test getting movies with filters"""
        mock_db = AsyncMock()
        
        # Mock filtered movies
        mock_movies = [
            Movie(id=uuid4(), title="Action Movie 1", type=ContentType.MOVIE),
            Movie(id=uuid4(), title="Action Movie 2", type=ContentType.MOVIE)
        ]
        
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = mock_movies
        mock_db.execute.return_value = mock_result
        
        # Mock count query
        mock_count_result = AsyncMock()
        mock_count_result.scalar.return_value = 2
        
        # Set up side effects for different queries
        mock_db.execute.side_effect = [mock_result, mock_count_result]
        
        filters = {
            "genre": "Action",
            "year": 2023,
            "director": "Test Director"
        }
        
        result = await self.movie_service.get_movies(
            filters=filters,
            page=1,
            limit=10,
            db=mock_db
        )
        
        assert len(result["items"]) == 2
        assert result["total"] == 2
        assert result["page"] == 1
    
    @pytest.mark.asyncio
    async def test_get_movie_stats(self):
        """Test getting movie statistics"""
        mock_db = AsyncMock()
        
        # Mock movie exists
        mock_movie = Movie(
            id=self.test_movie_id,
            title="Stats Movie",
            type=ContentType.MOVIE
        )
        
        # Mock stats queries
        mock_results = [
            AsyncMock(scalar_one_or_none=lambda: mock_movie),  # Movie query
            AsyncMock(scalar=lambda: 10),   # review_count
            AsyncMock(scalar=lambda: 7.5),  # average_rating
            AsyncMock(scalar=lambda: 8.0),  # cultural_authenticity_avg
            AsyncMock(scalar=lambda: 7.0),  # production_quality_avg
            AsyncMock(scalar=lambda: 8.5),  # story_rating_avg
            AsyncMock(scalar=lambda: 9.0),  # acting_rating_avg
            AsyncMock(scalar=lambda: 6.5),  # cinematography_rating_avg
        ]
        
        # Mock rating distribution
        mock_distribution_result = AsyncMock()
        mock_distribution_result.fetchall.return_value = [
            (8, 3), (9, 4), (7, 2), (10, 1)
        ]
        mock_results.append(mock_distribution_result)
        
        mock_db.execute.side_effect = mock_results
        
        stats = await self.movie_service.get_movie_stats(self.test_movie_id, mock_db)
        
        assert isinstance(stats, MovieStats)
        assert stats.review_count == 10
        assert stats.average_rating == 7.5
        assert stats.cultural_authenticity_avg == 8.0
        assert stats.rating_distribution[8] == 3
        assert stats.rating_distribution[9] == 4
    
    @pytest.mark.asyncio
    async def test_get_trending_movies(self):
        """Test getting trending movies"""
        mock_db = AsyncMock()
        
        # Mock trending movies
        mock_movies = [
            Movie(id=uuid4(), title="Trending 1", type=ContentType.MOVIE),
            Movie(id=uuid4(), title="Trending 2", type=ContentType.MOVIE),
            Movie(id=uuid4(), title="Trending 3", type=ContentType.MOVIE)
        ]
        
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = mock_movies
        mock_db.execute.return_value = mock_result
        
        trending = await self.movie_service.get_trending_movies(limit=10, db=mock_db)
        
        assert len(trending) == 3
        assert trending[0].title == "Trending 1"
        assert trending[1].title == "Trending 2"
        assert trending[2].title == "Trending 3"
    
    @pytest.mark.asyncio
    async def test_get_featured_movies(self):
        """Test getting featured movies"""
        mock_db = AsyncMock()
        
        # Mock featured movies
        mock_movies = [
            Movie(id=uuid4(), title="Featured 1", type=ContentType.MOVIE),
            Movie(id=uuid4(), title="Featured 2", type=ContentType.MOVIE)
        ]
        
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = mock_movies
        mock_db.execute.return_value = mock_result
        
        featured = await self.movie_service.get_featured_movies(limit=5, db=mock_db)
        
        assert len(featured) == 2
        assert featured[0].title == "Featured 1"
        assert featured[1].title == "Featured 2"
    
    @pytest.mark.asyncio
    async def test_get_movie_reviews(self):
        """Test getting reviews for a movie"""
        mock_db = AsyncMock()
        
        # Mock movie exists
        mock_movie = Movie(
            id=self.test_movie_id,
            title="Movie with Reviews",
            type=ContentType.MOVIE
        )
        
        # Mock reviews
        mock_reviews = [
            Review(
                id=uuid4(),
                user_id=self.test_user_id,
                movie_id=self.test_movie_id,
                lemon_pie_rating=8,
                review_text="Great movie!",
                moderation_status=ModerationStatus.APPROVED
            ),
            Review(
                id=uuid4(),
                user_id=uuid4(),
                movie_id=self.test_movie_id,
                lemon_pie_rating=7,
                review_text="Good movie!",
                moderation_status=ModerationStatus.APPROVED
            )
        ]
        
        # Mock queries
        mock_movie_result = AsyncMock()
        mock_movie_result.scalar_one_or_none.return_value = mock_movie
        
        mock_reviews_result = AsyncMock()
        mock_reviews_result.scalars.return_value.all.return_value = mock_reviews
        
        mock_count_result = AsyncMock()
        mock_count_result.scalar.return_value = 2
        
        mock_db.execute.side_effect = [mock_movie_result, mock_reviews_result, mock_count_result]
        
        result = await self.movie_service.get_movie_reviews(
            self.test_movie_id, page=1, limit=10, db=mock_db
        )
        
        assert len(result["items"]) == 2
        assert result["total"] == 2
        assert result["items"][0].lemon_pie_rating == 8
        assert result["items"][1].lemon_pie_rating == 7
    
    @pytest.mark.asyncio
    async def test_add_movie_genre(self):
        """Test adding genre to movie"""
        mock_db = AsyncMock()
        
        # Mock movie exists
        mock_movie = Movie(
            id=self.test_movie_id,
            title="Test Movie",
            type=ContentType.MOVIE
        )
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_movie
        mock_db.execute.return_value = mock_result
        
        await self.movie_service.add_movie_genre(self.test_movie_id, "Action", mock_db)
        
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_add_movie_cast(self):
        """Test adding cast member to movie"""
        mock_db = AsyncMock()
        
        # Mock movie exists
        mock_movie = Movie(
            id=self.test_movie_id,
            title="Test Movie",
            type=ContentType.MOVIE
        )
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_movie
        mock_db.execute.return_value = mock_result
        
        cast_data = {
            "actor_name": "Test Actor",
            "character_name": "Test Character",
            "role_type": CastRole.ACTOR
        }
        
        await self.movie_service.add_movie_cast(self.test_movie_id, cast_data, mock_db)
        
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_movies_by_genre(self):
        """Test getting movies by genre"""
        mock_db = AsyncMock()
        
        # Mock movies with specific genre
        mock_movies = [
            Movie(id=uuid4(), title="Action Movie 1", type=ContentType.MOVIE),
            Movie(id=uuid4(), title="Action Movie 2", type=ContentType.MOVIE)
        ]
        
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = mock_movies
        mock_db.execute.return_value = mock_result
        
        movies = await self.movie_service.get_movies_by_genre("Action", mock_db)
        
        assert len(movies) == 2
        assert movies[0].title == "Action Movie 1"
        assert movies[1].title == "Action Movie 2"
    
    @pytest.mark.asyncio
    async def test_get_movies_by_year(self):
        """Test getting movies by release year"""
        mock_db = AsyncMock()
        
        # Mock movies from specific year
        mock_movies = [
            Movie(
                id=uuid4(),
                title="2023 Movie 1",
                release_date=date(2023, 1, 1),
                type=ContentType.MOVIE
            ),
            Movie(
                id=uuid4(),
                title="2023 Movie 2",
                release_date=date(2023, 6, 15),
                type=ContentType.MOVIE
            )
        ]
        
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = mock_movies
        mock_db.execute.return_value = mock_result
        
        movies = await self.movie_service.get_movies_by_year(2023, mock_db)
        
        assert len(movies) == 2
        assert movies[0].title == "2023 Movie 1"
        assert movies[1].title == "2023 Movie 2"
    
    @pytest.mark.asyncio
    async def test_get_movies_by_director(self):
        """Test getting movies by director"""
        mock_db = AsyncMock()
        
        # Mock movies by specific director
        mock_movies = [
            Movie(id=uuid4(), title="Director Movie 1", director="Test Director", type=ContentType.MOVIE),
            Movie(id=uuid4(), title="Director Movie 2", director="Test Director", type=ContentType.MOVIE)
        ]
        
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = mock_movies
        mock_db.execute.return_value = mock_result
        
        movies = await self.movie_service.get_movies_by_director("Test Director", mock_db)
        
        assert len(movies) == 2
        assert movies[0].director == "Test Director"
        assert movies[1].director == "Test Director"