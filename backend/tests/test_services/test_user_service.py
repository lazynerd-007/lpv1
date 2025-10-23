"""
Tests for user service functionality
"""
import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from datetime import datetime

from app.services.user_service import UserService
from app.models.user import User, UserRole
from app.models.movie import Movie, ContentType
from app.models.relationships import UserWatchlist, UserFavorites, UserFollows
from app.schemas.user import UserUpdate, UserStats


class TestUserService:
    """Test user service functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.user_service = UserService()
        self.test_user_id = uuid4()
        self.test_movie_id = uuid4()
    
    @pytest.mark.asyncio
    async def test_get_user_by_id_success(self):
        """Test successful user retrieval by ID"""
        mock_db = AsyncMock()
        
        # Mock user exists
        mock_user = User(
            id=self.test_user_id,
            email="test@example.com",
            name="Test User",
            role=UserRole.USER,
            is_active=True
        )
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result
        
        user = await self.user_service.get_user_by_id(self.test_user_id, mock_db)
        
        assert user.id == self.test_user_id
        assert user.email == "test@example.com"
        assert user.name == "Test User"
    
    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self):
        """Test user not found by ID"""
        from fastapi import HTTPException
        
        mock_db = AsyncMock()
        
        # Mock user not found
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db.execute.return_value = mock_result
        
        with pytest.raises(HTTPException) as exc_info:
            await self.user_service.get_user_by_id(self.test_user_id, mock_db)
        
        assert exc_info.value.status_code == 404
        assert "User not found" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_update_user_profile_success(self):
        """Test successful user profile update"""
        mock_db = AsyncMock()
        
        # Mock existing user
        mock_user = User(
            id=self.test_user_id,
            email="test@example.com",
            name="Old Name",
            bio="Old bio",
            role=UserRole.USER
        )
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute.return_value = mock_result
        
        # Update data
        update_data = UserUpdate(
            name="New Name",
            bio="New bio",
            location="New Location"
        )
        
        updated_user = await self.user_service.update_user_profile(
            self.test_user_id, update_data, mock_db
        )
        
        assert updated_user.name == "New Name"
        assert updated_user.bio == "New bio"
        assert updated_user.location == "New Location"
        mock_db.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_follow_user_success(self):
        """Test successful user following"""
        mock_db = AsyncMock()
        follower_id = uuid4()
        following_id = uuid4()
        
        # Mock users exist
        mock_follower = User(id=follower_id, email="follower@example.com", name="Follower")
        mock_following = User(id=following_id, email="following@example.com", name="Following")
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.side_effect = [mock_follower, mock_following, None]  # No existing follow
        mock_db.execute.return_value = mock_result
        
        result = await self.user_service.follow_user(follower_id, following_id, mock_db)
        
        assert result["message"] == "Successfully followed user"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_follow_user_already_following(self):
        """Test following user when already following"""
        from fastapi import HTTPException
        
        mock_db = AsyncMock()
        follower_id = uuid4()
        following_id = uuid4()
        
        # Mock users exist and follow relationship exists
        mock_follower = User(id=follower_id, email="follower@example.com", name="Follower")
        mock_following = User(id=following_id, email="following@example.com", name="Following")
        mock_follow = UserFollows(follower_id=follower_id, following_id=following_id)
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.side_effect = [mock_follower, mock_following, mock_follow]
        mock_db.execute.return_value = mock_result
        
        with pytest.raises(HTTPException) as exc_info:
            await self.user_service.follow_user(follower_id, following_id, mock_db)
        
        assert exc_info.value.status_code == 400
        assert "already following" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_follow_self_fails(self):
        """Test that user cannot follow themselves"""
        from fastapi import HTTPException
        
        mock_db = AsyncMock()
        user_id = uuid4()
        
        with pytest.raises(HTTPException) as exc_info:
            await self.user_service.follow_user(user_id, user_id, mock_db)
        
        assert exc_info.value.status_code == 400
        assert "cannot follow yourself" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_unfollow_user_success(self):
        """Test successful user unfollowing"""
        mock_db = AsyncMock()
        follower_id = uuid4()
        following_id = uuid4()
        
        # Mock follow relationship exists
        mock_follow = UserFollows(follower_id=follower_id, following_id=following_id)
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_follow
        mock_db.execute.return_value = mock_result
        
        result = await self.user_service.unfollow_user(follower_id, following_id, mock_db)
        
        assert result["message"] == "Successfully unfollowed user"
        mock_db.delete.assert_called_once_with(mock_follow)
        mock_db.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_add_to_watchlist_success(self):
        """Test adding movie to watchlist"""
        mock_db = AsyncMock()
        
        # Mock user and movie exist, no existing watchlist entry
        mock_user = User(id=self.test_user_id, email="test@example.com", name="Test User")
        mock_movie = Movie(id=self.test_movie_id, title="Test Movie", type=ContentType.MOVIE)
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.side_effect = [mock_user, mock_movie, None]
        mock_db.execute.return_value = mock_result
        
        result = await self.user_service.add_to_watchlist(self.test_user_id, self.test_movie_id, mock_db)
        
        assert result["message"] == "Movie added to watchlist"
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_add_to_watchlist_already_exists(self):
        """Test adding movie to watchlist when already exists"""
        from fastapi import HTTPException
        
        mock_db = AsyncMock()
        
        # Mock user, movie, and existing watchlist entry
        mock_user = User(id=self.test_user_id, email="test@example.com", name="Test User")
        mock_movie = Movie(id=self.test_movie_id, title="Test Movie", type=ContentType.MOVIE)
        mock_watchlist = UserWatchlist(user_id=self.test_user_id, movie_id=self.test_movie_id)
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.side_effect = [mock_user, mock_movie, mock_watchlist]
        mock_db.execute.return_value = mock_result
        
        with pytest.raises(HTTPException) as exc_info:
            await self.user_service.add_to_watchlist(self.test_user_id, self.test_movie_id, mock_db)
        
        assert exc_info.value.status_code == 400
        assert "already in watchlist" in exc_info.value.detail
    
    @pytest.mark.asyncio
    async def test_remove_from_watchlist_success(self):
        """Test removing movie from watchlist"""
        mock_db = AsyncMock()
        
        # Mock existing watchlist entry
        mock_watchlist = UserWatchlist(user_id=self.test_user_id, movie_id=self.test_movie_id)
        
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_watchlist
        mock_db.execute.return_value = mock_result
        
        result = await self.user_service.remove_from_watchlist(self.test_user_id, self.test_movie_id, mock_db)
        
        assert result["message"] == "Movie removed from watchlist"
        mock_db.delete.assert_called_once_with(mock_watchlist)
        mock_db.commit.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_user_stats(self):
        """Test getting user statistics"""
        mock_db = AsyncMock()
        
        # Mock stats queries
        mock_results = [
            AsyncMock(scalar=lambda: 5),    # total_reviews
            AsyncMock(scalar=lambda: 7.5),  # average_rating
            AsyncMock(scalar=lambda: 10),   # followers_count
            AsyncMock(scalar=lambda: 8),    # following_count
            AsyncMock(scalar=lambda: 15),   # watchlist_count
        ]
        
        mock_db.execute.side_effect = mock_results
        
        stats = await self.user_service.get_user_stats(self.test_user_id, mock_db)
        
        assert isinstance(stats, UserStats)
        assert stats.total_reviews == 5
        assert stats.average_rating == 7.5
        assert stats.followers_count == 10
        assert stats.following_count == 8
        assert stats.movies_watched == 15
    
    @pytest.mark.asyncio
    async def test_get_user_activity_feed(self):
        """Test getting user activity feed"""
        mock_db = AsyncMock()
        
        # Mock activity results
        mock_activities = [
            {
                "type": "review",
                "user_name": "Friend 1",
                "movie_title": "Movie 1",
                "created_at": datetime.now()
            },
            {
                "type": "follow",
                "user_name": "Friend 2",
                "target_name": "User 3",
                "created_at": datetime.now()
            }
        ]
        
        mock_result = AsyncMock()
        mock_result.fetchall.return_value = mock_activities
        mock_db.execute.return_value = mock_result
        
        activities = await self.user_service.get_user_activity_feed(self.test_user_id, mock_db)
        
        assert len(activities) == 2
        assert activities[0]["type"] == "review"
        assert activities[1]["type"] == "follow"
    
    @pytest.mark.asyncio
    async def test_search_users(self):
        """Test user search functionality"""
        mock_db = AsyncMock()
        
        # Mock search results
        mock_users = [
            User(id=uuid4(), email="user1@example.com", name="John Doe", role=UserRole.USER),
            User(id=uuid4(), email="user2@example.com", name="Jane Doe", role=UserRole.CRITIC)
        ]
        
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = mock_users
        mock_db.execute.return_value = mock_result
        
        users = await self.user_service.search_users("Doe", mock_db)
        
        assert len(users) == 2
        assert users[0].name == "John Doe"
        assert users[1].name == "Jane Doe"
    
    @pytest.mark.asyncio
    async def test_get_followers_list(self):
        """Test getting user followers list"""
        mock_db = AsyncMock()
        
        # Mock followers
        mock_followers = [
            User(id=uuid4(), email="follower1@example.com", name="Follower 1"),
            User(id=uuid4(), email="follower2@example.com", name="Follower 2")
        ]
        
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = mock_followers
        mock_db.execute.return_value = mock_result
        
        followers = await self.user_service.get_followers(self.test_user_id, mock_db)
        
        assert len(followers) == 2
        assert followers[0].name == "Follower 1"
        assert followers[1].name == "Follower 2"
    
    @pytest.mark.asyncio
    async def test_get_following_list(self):
        """Test getting user following list"""
        mock_db = AsyncMock()
        
        # Mock following
        mock_following = [
            User(id=uuid4(), email="following1@example.com", name="Following 1"),
            User(id=uuid4(), email="following2@example.com", name="Following 2")
        ]
        
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = mock_following
        mock_db.execute.return_value = mock_result
        
        following = await self.user_service.get_following(self.test_user_id, mock_db)
        
        assert len(following) == 2
        assert following[0].name == "Following 1"
        assert following[1].name == "Following 2"