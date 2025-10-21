"""
Tests for database configuration and models
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import Base, get_db
from app.models.user import User, UserRole
from app.models.movie import Movie, ContentType
from app.models.review import Review, ModerationStatus


@pytest.mark.asyncio
async def test_database_session(test_db_session):
    """Test database session creation"""
    assert isinstance(test_db_session, AsyncSession)
    
    # Test basic query
    result = await test_db_session.execute(select(1))
    assert result.scalar() == 1


@pytest.mark.asyncio
async def test_user_model_creation(test_db_session):
    """Test User model creation and persistence"""
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User",
        bio="Test bio",
        role=UserRole.USER
    )
    
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.role == UserRole.USER
    assert user.is_active is True
    assert user.is_verified is False
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_movie_model_creation(test_db_session):
    """Test Movie model creation and persistence"""
    from datetime import date
    
    movie = Movie(
        title="Test Movie",
        local_title="Test Local Title",
        release_date=date(2023, 1, 1),
        runtime=120,
        plot_summary="Test plot summary",
        director="Test Director",
        type=ContentType.MOVIE
    )
    
    test_db_session.add(movie)
    await test_db_session.commit()
    await test_db_session.refresh(movie)
    
    assert movie.id is not None
    assert movie.title == "Test Movie"
    assert movie.local_title == "Test Local Title"
    assert movie.runtime == 120
    assert movie.type == ContentType.MOVIE
    assert movie.created_at is not None


@pytest.mark.asyncio
async def test_review_model_creation(test_db_session):
    """Test Review model creation and persistence"""
    from datetime import date
    
    # Create user first
    user = User(
        email="reviewer@example.com",
        password_hash="hashed_password",
        name="Reviewer",
        role=UserRole.USER
    )
    test_db_session.add(user)
    await test_db_session.flush()
    
    # Create movie
    movie = Movie(
        title="Review Test Movie",
        release_date=date(2023, 1, 1),
        type=ContentType.MOVIE
    )
    test_db_session.add(movie)
    await test_db_session.flush()
    
    # Create review
    review = Review(
        user_id=user.id,
        movie_id=movie.id,
        lemon_pie_rating=8,
        review_text="Great movie!",
        cultural_authenticity_rating=9,
        production_quality_rating=7,
        story_rating=8,
        acting_rating=9,
        cinematography_rating=8,
        moderation_status=ModerationStatus.APPROVED
    )
    
    test_db_session.add(review)
    await test_db_session.commit()
    await test_db_session.refresh(review)
    
    assert review.id is not None
    assert review.user_id == user.id
    assert review.movie_id == movie.id
    assert review.lemon_pie_rating == 8
    assert review.review_text == "Great movie!"
    assert review.moderation_status == ModerationStatus.APPROVED
    assert review.helpful_votes == 0
    assert review.unhelpful_votes == 0


@pytest.mark.asyncio
async def test_user_roles():
    """Test user role enum values"""
    assert UserRole.USER == "user"
    assert UserRole.CRITIC == "critic"
    assert UserRole.MODERATOR == "moderator"
    assert UserRole.ADMIN == "admin"


@pytest.mark.asyncio
async def test_content_types():
    """Test content type enum values"""
    assert ContentType.MOVIE == "movie"
    assert ContentType.SERIES == "series"


@pytest.mark.asyncio
async def test_moderation_status():
    """Test moderation status enum values"""
    assert ModerationStatus.PENDING == "pending"
    assert ModerationStatus.APPROVED == "approved"
    assert ModerationStatus.REJECTED == "rejected"


@pytest.mark.asyncio
async def test_review_rating_constraints(test_db_session):
    """Test review rating constraints"""
    from datetime import date
    
    # Create user and movie
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User",
        role=UserRole.USER
    )
    movie = Movie(
        title="Test Movie",
        release_date=date(2023, 1, 1),
        type=ContentType.MOVIE
    )
    
    test_db_session.add_all([user, movie])
    await test_db_session.flush()
    
    # Test valid ratings
    review = Review(
        user_id=user.id,
        movie_id=movie.id,
        lemon_pie_rating=5,
        review_text="Average movie",
        cultural_authenticity_rating=1,  # Min value
        production_quality_rating=10,   # Max value
    )
    
    test_db_session.add(review)
    await test_db_session.commit()
    
    assert review.lemon_pie_rating == 5
    assert review.cultural_authenticity_rating == 1
    assert review.production_quality_rating == 10