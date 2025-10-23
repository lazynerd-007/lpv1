"""
Tests for movie API endpoints
"""
import pytest
from datetime import date
from uuid import uuid4
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole
from app.models.movie import Movie, ContentType
from app.models.relationships import MovieGenre, MovieLanguage, MovieCast
from app.models.review import Review, ModerationStatus
from app.models.enums import CastRole


@pytest.mark.asyncio
async def test_get_movies_empty(async_client: AsyncClient):
    """Test getting movies when database is empty"""
    response = await async_client.get("/api/v1/movies/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["limit"] == 20
    assert data["pages"] == 0
    assert data["has_next"] is False
    assert data["has_prev"] is False


@pytest.mark.asyncio
async def test_create_movie_admin_required(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test that creating a movie requires admin privileges"""
    # Create regular user
    user = User(
        email="user@example.com",
        password_hash="hashed_password",
        name="Test User",
        role=UserRole.USER
    )
    test_db_session.add(user)
    await test_db_session.commit()
    
    # Try to create movie without authentication
    movie_data = {
        "title": "Test Movie",
        "release_date": "2023-01-01",
        "plot_summary": "A test movie",
        "director": "Test Director",
        "genres": ["Action", "Drama"],
        "languages": ["English"],
        "cast": []
    }
    
    response = await async_client.post("/api/v1/movies/", json=movie_data)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_movie_success(async_client: AsyncClient, test_db_session: AsyncSession, admin_token: str):
    """Test successful movie creation by admin"""
    movie_data = {
        "title": "Test Nollywood Movie",
        "local_title": "Test Local Title",
        "release_date": "2023-01-01",
        "runtime": 120,
        "plot_summary": "A great Nollywood movie about family and tradition",
        "director": "Kunle Afolayan",
        "producer": "Test Producer",
        "production_company": "Golden Effects Pictures",
        "production_state": "Lagos",
        "box_office_ng": "₦50M",
        "type": "movie",
        "genres": ["Drama", "Family"],
        "languages": ["English", "Yoruba"],
        "cast": [
            {
                "actor_name": "Ramsey Nouah",
                "character_name": "Chief Adebayo",
                "role_type": "actor"
            },
            {
                "actor_name": "Kunle Afolayan",
                "character_name": "",
                "role_type": "director"
            }
        ],
        "poster_url": "https://example.com/poster.jpg",
        "trailer_url": "https://example.com/trailer.mp4"
    }
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.post("/api/v1/movies/", json=movie_data, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Test Nollywood Movie"
    assert data["local_title"] == "Test Local Title"
    assert data["director"] == "Kunle Afolayan"
    assert data["genres"] == ["Drama", "Family"]
    assert data["languages"] == ["English", "Yoruba"]
    assert len(data["cast"]) == 2
    assert data["stats"]["review_count"] == 0
    assert data["stats"]["average_rating"] == 0.0


@pytest.mark.asyncio
async def test_get_movie_by_id(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test getting a movie by ID"""
    # Create a movie
    movie = Movie(
        title="Test Movie",
        release_date=date(2023, 1, 1),
        plot_summary="Test plot",
        director="Test Director",
        type=ContentType.MOVIE
    )
    test_db_session.add(movie)
    await test_db_session.flush()
    
    # Add genres
    genre1 = MovieGenre(movie_id=movie.id, genre="Action")
    genre2 = MovieGenre(movie_id=movie.id, genre="Drama")
    test_db_session.add_all([genre1, genre2])
    
    # Add languages
    lang1 = MovieLanguage(movie_id=movie.id, language="English")
    test_db_session.add(lang1)
    
    # Add cast
    cast1 = MovieCast(
        movie_id=movie.id,
        actor_name="Test Actor",
        character_name="Test Character",
        role_type=CastRole.ACTOR
    )
    test_db_session.add(cast1)
    
    await test_db_session.commit()
    
    response = await async_client.get(f"/api/v1/movies/{movie.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == str(movie.id)
    assert data["title"] == "Test Movie"
    assert data["director"] == "Test Director"
    assert "Action" in data["genres"]
    assert "Drama" in data["genres"]
    assert "English" in data["languages"]
    assert len(data["cast"]) == 1
    assert data["cast"][0]["actor_name"] == "Test Actor"


@pytest.mark.asyncio
async def test_get_movie_not_found(async_client: AsyncClient):
    """Test getting a non-existent movie"""
    fake_id = uuid4()
    response = await async_client.get(f"/api/v1/movies/{fake_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_movies_with_filters(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test getting movies with various filters"""
    # Create movies with different attributes
    movie1 = Movie(
        title="Action Movie",
        release_date=date(2023, 1, 1),
        director="Action Director",
        type=ContentType.MOVIE
    )
    movie2 = Movie(
        title="Drama Movie",
        release_date=date(2022, 1, 1),
        director="Drama Director",
        type=ContentType.MOVIE
    )
    test_db_session.add_all([movie1, movie2])
    await test_db_session.flush()
    
    # Add genres
    genre1 = MovieGenre(movie_id=movie1.id, genre="Action")
    genre2 = MovieGenre(movie_id=movie2.id, genre="Drama")
    test_db_session.add_all([genre1, genre2])
    
    await test_db_session.commit()
    
    # Test genre filter
    response = await async_client.get("/api/v1/movies/?genre=Action")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Action Movie"
    
    # Test year filter
    response = await async_client.get("/api/v1/movies/?year=2023")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Action Movie"
    
    # Test director filter
    response = await async_client.get("/api/v1/movies/?director=Drama")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Drama Movie"


@pytest.mark.asyncio
async def test_get_movies_with_sorting(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test getting movies with different sorting options"""
    # Create movies
    movie1 = Movie(
        title="A Movie",
        release_date=date(2023, 1, 1),
        director="Director A",
        type=ContentType.MOVIE
    )
    movie2 = Movie(
        title="B Movie",
        release_date=date(2022, 1, 1),
        director="Director B",
        type=ContentType.MOVIE
    )
    test_db_session.add_all([movie1, movie2])
    await test_db_session.commit()
    
    # Test title sorting ascending
    response = await async_client.get("/api/v1/movies/?sort_field=title&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    assert data["items"][0]["title"] == "A Movie"
    assert data["items"][1]["title"] == "B Movie"
    
    # Test title sorting descending
    response = await async_client.get("/api/v1/movies/?sort_field=title&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    assert data["items"][0]["title"] == "B Movie"
    assert data["items"][1]["title"] == "A Movie"
    
    # Test release date sorting
    response = await async_client.get("/api/v1/movies/?sort_field=release_date&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    assert data["items"][0]["title"] == "A Movie"  # 2023 movie first


@pytest.mark.asyncio
async def test_get_movies_pagination(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test movie pagination"""
    # Create multiple movies
    movies = []
    for i in range(25):
        movie = Movie(
            title=f"Movie {i}",
            release_date=date(2023, 1, 1),
            director=f"Director {i}",
            type=ContentType.MOVIE
        )
        movies.append(movie)
    
    test_db_session.add_all(movies)
    await test_db_session.commit()
    
    # Test first page
    response = await async_client.get("/api/v1/movies/?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 25
    assert data["page"] == 1
    assert data["pages"] == 3
    assert data["has_next"] is True
    assert data["has_prev"] is False
    
    # Test second page
    response = await async_client.get("/api/v1/movies/?page=2&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["page"] == 2
    assert data["has_next"] is True
    assert data["has_prev"] is True
    
    # Test last page
    response = await async_client.get("/api/v1/movies/?page=3&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5
    assert data["page"] == 3
    assert data["has_next"] is False
    assert data["has_prev"] is True


@pytest.mark.asyncio
async def test_movie_stats_calculation(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test movie statistics calculation with reviews"""
    # Create users and movie
    user1 = User(
        email="reviewer1@example.com",
        password_hash="hashed_password",
        name="Reviewer 1",
        role=UserRole.USER
    )
    user2 = User(
        email="reviewer2@example.com",
        password_hash="hashed_password",
        name="Reviewer 2",
        role=UserRole.USER
    )
    movie = Movie(
        title="Movie with Reviews",
        release_date=date(2023, 1, 1),
        director="Test Director",
        type=ContentType.MOVIE
    )
    test_db_session.add_all([user1, user2, movie])
    await test_db_session.flush()
    
    # Create reviews from different users
    review1 = Review(
        user_id=user1.id,
        movie_id=movie.id,
        lemon_pie_rating=8,
        review_text="Great movie!",
        cultural_authenticity_rating=9,
        production_quality_rating=7,
        story_rating=8,
        acting_rating=9,
        cinematography_rating=6,
        moderation_status=ModerationStatus.APPROVED
    )
    review2 = Review(
        user_id=user2.id,
        movie_id=movie.id,
        lemon_pie_rating=6,
        review_text="Good movie!",
        cultural_authenticity_rating=7,
        production_quality_rating=8,
        story_rating=6,
        acting_rating=7,
        cinematography_rating=8,
        moderation_status=ModerationStatus.APPROVED
    )
    test_db_session.add_all([review1, review2])
    await test_db_session.commit()
    
    response = await async_client.get(f"/api/v1/movies/{movie.id}")
    assert response.status_code == 200
    
    data = response.json()
    stats = data["stats"]
    assert stats["review_count"] == 2
    assert stats["average_rating"] == 7.0  # (8 + 6) / 2
    assert stats["cultural_authenticity_avg"] == 8.0  # (9 + 7) / 2
    assert stats["production_quality_avg"] == 7.5  # (7 + 8) / 2
    assert stats["story_rating_avg"] == 7.0  # (8 + 6) / 2
    assert stats["acting_rating_avg"] == 8.0  # (9 + 7) / 2
    assert stats["cinematography_rating_avg"] == 7.0  # (6 + 8) / 2
    
    # Check rating distribution
    assert stats["rating_distribution"]["6"] == 1
    assert stats["rating_distribution"]["8"] == 1


@pytest.mark.asyncio
async def test_get_movie_stats_endpoint(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test the dedicated movie stats endpoint"""
    # Create movie
    movie = Movie(
        title="Stats Test Movie",
        release_date=date(2023, 1, 1),
        director="Test Director",
        type=ContentType.MOVIE
    )
    test_db_session.add(movie)
    await test_db_session.commit()
    
    response = await async_client.get(f"/api/v1/movies/{movie.id}/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert data["movie_id"] == str(movie.id)
    assert data["title"] == "Stats Test Movie"
    assert "stats" in data
    assert data["stats"]["review_count"] == 0


@pytest.mark.asyncio
async def test_update_movie_admin_required(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test that updating a movie requires admin privileges"""
    # Create movie
    movie = Movie(
        title="Original Title",
        release_date=date(2023, 1, 1),
        director="Original Director",
        type=ContentType.MOVIE
    )
    test_db_session.add(movie)
    await test_db_session.commit()
    
    update_data = {"title": "Updated Title"}
    
    response = await async_client.put(f"/api/v1/movies/{movie.id}", json=update_data)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_movie_success(async_client: AsyncClient, test_db_session: AsyncSession, admin_token: str):
    """Test successful movie update by admin"""
    # Create movie
    movie = Movie(
        title="Original Title",
        release_date=date(2023, 1, 1),
        director="Original Director",
        type=ContentType.MOVIE
    )
    test_db_session.add(movie)
    await test_db_session.flush()
    
    # Add original genre
    genre = MovieGenre(movie_id=movie.id, genre="Action")
    test_db_session.add(genre)
    await test_db_session.commit()
    
    update_data = {
        "title": "Updated Title",
        "director": "Updated Director",
        "genres": ["Drama", "Romance"]
    }
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/api/v1/movies/{movie.id}", json=update_data, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["director"] == "Updated Director"
    assert "Drama" in data["genres"]
    assert "Romance" in data["genres"]
    assert "Action" not in data["genres"]  # Should be replaced


@pytest.mark.asyncio
async def test_delete_movie_admin_required(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test that deleting a movie requires admin privileges"""
    # Create movie
    movie = Movie(
        title="To Delete",
        release_date=date(2023, 1, 1),
        director="Test Director",
        type=ContentType.MOVIE
    )
    test_db_session.add(movie)
    await test_db_session.commit()
    
    response = await async_client.delete(f"/api/v1/movies/{movie.id}")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_movie_success(async_client: AsyncClient, test_db_session: AsyncSession, admin_token: str):
    """Test successful movie deletion by admin"""
    # Create movie
    movie = Movie(
        title="To Delete",
        release_date=date(2023, 1, 1),
        director="Test Director",
        type=ContentType.MOVIE
    )
    test_db_session.add(movie)
    await test_db_session.commit()
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.delete(f"/api/v1/movies/{movie.id}", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Movie deleted successfully"
    
    # Verify movie is deleted
    response = await async_client.get(f"/api/v1/movies/{movie.id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_trending_movies(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test getting trending movies"""
    response = await async_client.get("/api/v1/movies/trending")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    # With empty database, should return empty list
    assert len(data) == 0


@pytest.mark.asyncio
async def test_get_featured_movies(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test getting featured movies"""
    response = await async_client.get("/api/v1/movies/featured")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    # With empty database, should return empty list
    assert len(data) == 0


@pytest.mark.asyncio
async def test_get_trending_movies_with_limit(async_client: AsyncClient):
    """Test getting trending movies with custom limit"""
    response = await async_client.get("/api/v1/movies/trending?limit=5")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5


@pytest.mark.asyncio
async def test_get_featured_movies_with_limit(async_client: AsyncClient):
    """Test getting featured movies with custom limit"""
    response = await async_client.get("/api/v1/movies/featured?limit=5")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5


@pytest.mark.asyncio
async def test_get_movie_reviews(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test getting reviews for a specific movie"""
    # Create user and movie
    user = User(
        email="reviewer@example.com",
        password_hash="hashed_password",
        name="Reviewer",
        role=UserRole.USER
    )
    movie = Movie(
        title="Movie with Reviews",
        release_date=date(2023, 1, 1),
        director="Test Director",
        type=ContentType.MOVIE
    )
    test_db_session.add_all([user, movie])
    await test_db_session.flush()
    
    # Create a review
    review = Review(
        user_id=user.id,
        movie_id=movie.id,
        lemon_pie_rating=8,
        review_text="Great movie!",
        cultural_authenticity_rating=9,
        production_quality_rating=7,
        story_rating=8,
        acting_rating=9,
        cinematography_rating=6,
        moderation_status=ModerationStatus.APPROVED
    )
    test_db_session.add(review)
    await test_db_session.commit()
    
    response = await async_client.get(f"/api/v1/movies/{movie.id}/reviews")
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["lemon_pie_rating"] == 8
    assert data["items"][0]["review_text"] == "Great movie!"
    assert data["items"][0]["user"]["name"] == "Reviewer"


@pytest.mark.asyncio
async def test_get_movie_reviews_not_found(async_client: AsyncClient):
    """Test getting reviews for a non-existent movie"""
    fake_id = uuid4()
    response = await async_client.get(f"/api/v1/movies/{fake_id}/reviews")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_movie_reviews_pagination(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test movie reviews pagination"""
    # Create users and movie
    users = []
    for i in range(15):
        user = User(
            email=f"reviewer{i}@example.com",
            password_hash="hashed_password",
            name=f"Reviewer {i}",
            role=UserRole.USER
        )
        users.append(user)
    
    movie = Movie(
        title="Popular Movie",
        release_date=date(2023, 1, 1),
        director="Test Director",
        type=ContentType.MOVIE
    )
    test_db_session.add_all(users + [movie])
    await test_db_session.flush()
    
    # Create reviews
    reviews = []
    for i, user in enumerate(users):
        review = Review(
            user_id=user.id,
            movie_id=movie.id,
            lemon_pie_rating=5 + (i % 6),  # Ratings from 5-10
            review_text=f"Review {i}",
            moderation_status=ModerationStatus.APPROVED
        )
        reviews.append(review)
    
    test_db_session.add_all(reviews)
    await test_db_session.commit()
    
    # Test first page
    response = await async_client.get(f"/api/v1/movies/{movie.id}/reviews?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["pages"] == 2
    assert data["has_next"] is True
    assert data["has_prev"] is False
    
    # Test second page
    response = await async_client.get(f"/api/v1/movies/{movie.id}/reviews?page=2&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5
    assert data["page"] == 2
    assert data["has_next"] is False
    assert data["has_prev"] is True


@pytest.mark.asyncio
async def test_search_movies_basic(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test basic movie search functionality"""
    # Create movies
    movie1 = Movie(
        title="The Wedding Party",
        release_date=date(2016, 12, 16),
        director="Kemi Adetiba",
        plot_summary="A chaotic Nigerian wedding",
        type=ContentType.MOVIE
    )
    movie2 = Movie(
        title="King of Boys",
        release_date=date(2018, 10, 26),
        director="Kemi Adetiba",
        plot_summary="A political thriller",
        type=ContentType.MOVIE
    )
    movie3 = Movie(
        title="Lionheart",
        release_date=date(2018, 12, 21),
        director="Genevieve Nnaji",
        plot_summary="A family business story",
        type=ContentType.MOVIE
    )
    test_db_session.add_all([movie1, movie2, movie3])
    await test_db_session.commit()
    
    # Test search by title
    response = await async_client.get("/api/v1/movies/search?q=Wedding")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "The Wedding Party"
    
    # Test search by director
    response = await async_client.get("/api/v1/movies/search?q=Kemi")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Test search with no results
    response = await async_client.get("/api/v1/movies/search?q=NonExistent")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.asyncio
async def test_search_movies_with_filters(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test movie search with filters"""
    # Create movie with genres
    movie = Movie(
        title="Chief Daddy",
        release_date=date(2018, 12, 14),
        director="Niyi Akinmolayan",
        type=ContentType.MOVIE
    )
    test_db_session.add(movie)
    await test_db_session.flush()
    
    # Add genre
    genre = MovieGenre(movie_id=movie.id, genre="Comedy")
    test_db_session.add(genre)
    await test_db_session.commit()
    
    # Test search with genre filter
    response = await async_client.get("/api/v1/movies/search?q=Chief&genre=Comedy")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Chief Daddy"
    
    # Test search with wrong genre filter
    response = await async_client.get("/api/v1/movies/search?q=Chief&genre=Action")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.asyncio
async def test_search_suggestions(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test search suggestions"""
    # Create movies
    movies = [
        Movie(title="The Wedding Party", release_date=date(2016, 12, 16), director="Kemi Adetiba", type=ContentType.MOVIE),
        Movie(title="The Wedding Party 2", release_date=date(2017, 12, 15), director="Niyi Akinmolayan", type=ContentType.MOVIE),
        Movie(title="Wedding Fever", release_date=date(2019, 1, 1), director="Test Director", type=ContentType.MOVIE),
    ]
    test_db_session.add_all(movies)
    await test_db_session.commit()
    
    response = await async_client.get("/api/v1/movies/search/suggestions?q=Wed")
    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert len(data["suggestions"]) >= 2
    assert any("Wedding" in suggestion for suggestion in data["suggestions"])


@pytest.mark.asyncio
async def test_search_popular(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test popular searches endpoint"""
    # Create movies with reviews to make them popular
    user = User(
        email="reviewer@example.com",
        password_hash="hashed_password",
        name="Reviewer",
        role=UserRole.USER
    )
    movie = Movie(
        title="Popular Movie",
        release_date=date(2023, 1, 1),
        director="Popular Director",
        type=ContentType.MOVIE
    )
    test_db_session.add_all([user, movie])
    await test_db_session.flush()
    
    # Add review to make it popular
    review = Review(
        user_id=user.id,
        movie_id=movie.id,
        lemon_pie_rating=9,
        review_text="Amazing movie!",
        moderation_status=ModerationStatus.APPROVED
    )
    test_db_session.add(review)
    await test_db_session.commit()
    
    response = await async_client.get("/api/v1/movies/search/popular")
    assert response.status_code == 200
    data = response.json()
    assert "popular_searches" in data
    assert isinstance(data["popular_searches"], list)


@pytest.mark.asyncio
async def test_search_by_cast(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test search by cast member"""
    # Create movie with cast
    movie = Movie(
        title="Nollywood Classic",
        release_date=date(2020, 1, 1),
        director="Great Director",
        type=ContentType.MOVIE
    )
    test_db_session.add(movie)
    await test_db_session.flush()
    
    # Add cast member
    cast = MovieCast(
        movie_id=movie.id,
        actor_name="Ramsey Nouah",
        character_name="Lead Character",
        role_type=CastRole.ACTOR
    )
    test_db_session.add(cast)
    await test_db_session.commit()
    
    response = await async_client.get("/api/v1/movies/search/by-cast?actor=Ramsey")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Nollywood Classic"


@pytest.mark.asyncio
async def test_search_pagination(async_client: AsyncClient, test_db_session: AsyncSession):
    """Test search pagination"""
    # Create multiple movies with similar titles
    movies = []
    for i in range(25):
        movie = Movie(
            title=f"Nollywood Movie {i}",
            release_date=date(2023, 1, 1),
            director=f"Director {i}",
            type=ContentType.MOVIE
        )
        movies.append(movie)
    
    test_db_session.add_all(movies)
    await test_db_session.commit()
    
    # Test first page
    response = await async_client.get("/api/v1/movies/search?q=Nollywood&page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    
    # Test second page
    response = await async_client.get("/api/v1/movies/search?q=Nollywood&page=2&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    
    # Test third page
    response = await async_client.get("/api/v1/movies/search?q=Nollywood&page=3&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


@pytest.mark.asyncio
async def test_search_empty_query(async_client: AsyncClient):
    """Test search with empty query"""
    response = await async_client.get("/api/v1/movies/search?q=")
    assert response.status_code == 422  # Validation error for empty query


@pytest.mark.asyncio
async def test_search_suggestions_short_query(async_client: AsyncClient):
    """Test search suggestions with too short query"""
    response = await async_client.get("/api/v1/movies/search/suggestions?q=a")
    assert response.status_code == 422  # Validation error for short query