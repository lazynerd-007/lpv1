"""
User service for LemonNPie Backend API
"""
from typing import Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.user import User
from app.models.relationships import UserFollow, UserWatchlist, UserFavorite
from app.models.review import Review
from app.models.movie import Movie
from app.schemas.user import UserProfileUpdate, UserStats, UserProfileResponse, UserPublicProfile, UserListResponse, ActivityFeedResponse, ActivityItem, MovieListResponse, MovieListItem
from app.core.exceptions import LemonPieException


class UserService:
    """Service class for user-related operations"""
    
    async def get_user_by_id(
        self, 
        user_id: UUID, 
        db: AsyncSession,
        include_stats: bool = True
    ) -> Optional[User]:
        """Get user by ID with optional statistics"""
        query = select(User).where(User.id == user_id, User.is_active == True)
        
        if include_stats:
            query = query.options(
                selectinload(User.reviews),
                selectinload(User.followers),
                selectinload(User.following),
                selectinload(User.watchlist),
                selectinload(User.favorites)
            )
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_stats(self, user_id: UUID, db: AsyncSession) -> UserStats:
        """Calculate user statistics"""
        # Get review count and average rating
        review_stats_query = select(
            func.count(Review.id).label('total_reviews'),
            func.avg(Review.lemon_pie_rating).label('average_rating')
        ).where(Review.user_id == user_id)
        
        review_result = await db.execute(review_stats_query)
        review_stats = review_result.first()
        
        # Get followers count
        followers_query = select(func.count(UserFollow.follower_id)).where(
            UserFollow.following_id == user_id
        )
        followers_result = await db.execute(followers_query)
        followers_count = followers_result.scalar() or 0
        
        # Get following count
        following_query = select(func.count(UserFollow.following_id)).where(
            UserFollow.follower_id == user_id
        )
        following_result = await db.execute(following_query)
        following_count = following_result.scalar() or 0
        
        # Get watchlist count
        watchlist_query = select(func.count(UserWatchlist.movie_id)).where(
            UserWatchlist.user_id == user_id
        )
        watchlist_result = await db.execute(watchlist_query)
        watchlist_count = watchlist_result.scalar() or 0
        
        # Get favorites count
        favorites_query = select(func.count(UserFavorite.movie_id)).where(
            UserFavorite.user_id == user_id
        )
        favorites_result = await db.execute(favorites_query)
        favorites_count = favorites_result.scalar() or 0
        
        return UserStats(
            total_reviews=review_stats.total_reviews or 0,
            average_rating=float(review_stats.average_rating) if review_stats.average_rating else None,
            followers_count=followers_count,
            following_count=following_count,
            watchlist_count=watchlist_count,
            favorites_count=favorites_count
        )
    
    async def update_user_profile(
        self, 
        user_id: UUID, 
        update_data: UserProfileUpdate, 
        db: AsyncSession
    ) -> User:
        """Update user profile"""
        # Get user
        user = await self.get_user_by_id(user_id, db, include_stats=False)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields that are provided
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(user, field, value)
        
        # Commit changes
        await db.commit()
        await db.refresh(user)
        
        return user
    
    async def get_user_profile(
        self, 
        user_id: UUID, 
        db: AsyncSession,
        requesting_user_id: Optional[UUID] = None
    ) -> UserProfileResponse:
        """Get user profile with statistics"""
        user = await self.get_user_by_id(user_id, db, include_stats=False)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get user statistics
        stats = await self.get_user_stats(user_id, db)
        
        # If requesting user is the same as the profile user, return full profile
        # Otherwise, return public profile (same for now, but can be extended)
        return UserProfileResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            bio=user.bio,
            location=user.location,
            avatar_url=user.avatar_url,
            role=user.role,
            is_verified=user.is_verified,
            created_at=user.created_at,
            stats=stats
        )
    
    async def get_public_profile(
        self, 
        user_id: UUID, 
        db: AsyncSession
    ) -> UserPublicProfile:
        """Get public user profile (limited information)"""
        user = await self.get_user_by_id(user_id, db, include_stats=False)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get user statistics
        stats = await self.get_user_stats(user_id, db)
        
        return UserPublicProfile(
            id=user.id,
            name=user.name,
            bio=user.bio,
            location=user.location,
            avatar_url=user.avatar_url,
            role=user.role,
            is_verified=user.is_verified,
            created_at=user.created_at,
            stats=stats
        )
    
    async def follow_user(
        self, 
        follower_id: UUID, 
        following_id: UUID, 
        db: AsyncSession
    ) -> None:
        """Follow a user"""
        # Check if target user exists
        target_user = await self.get_user_by_id(following_id, db, include_stats=False)
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if already following
        existing_follow = await db.execute(
            select(UserFollow).where(
                and_(
                    UserFollow.follower_id == follower_id,
                    UserFollow.following_id == following_id
                )
            )
        )
        if existing_follow.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Already following this user"
            )
        
        # Create follow relationship
        follow = UserFollow(follower_id=follower_id, following_id=following_id)
        db.add(follow)
        await db.commit()
    
    async def unfollow_user(
        self, 
        follower_id: UUID, 
        following_id: UUID, 
        db: AsyncSession
    ) -> None:
        """Unfollow a user"""
        # Find and delete the follow relationship
        follow = await db.execute(
            select(UserFollow).where(
                and_(
                    UserFollow.follower_id == follower_id,
                    UserFollow.following_id == following_id
                )
            )
        )
        follow_obj = follow.scalar_one_or_none()
        
        if not follow_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not following this user"
            )
        
        await db.delete(follow_obj)
        await db.commit()
    
    async def get_user_followers(
        self, 
        user_id: UUID, 
        page: int, 
        per_page: int, 
        db: AsyncSession
    ) -> UserListResponse:
        """Get paginated list of user followers"""
        offset = (page - 1) * per_page
        
        # Get total count
        total_query = select(func.count(UserFollow.follower_id)).where(
            UserFollow.following_id == user_id
        )
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0
        
        # Get followers with user details
        followers_query = (
            select(User)
            .join(UserFollow, User.id == UserFollow.follower_id)
            .where(UserFollow.following_id == user_id)
            .order_by(UserFollow.created_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        
        followers_result = await db.execute(followers_query)
        followers = followers_result.scalars().all()
        
        # Convert to public profiles
        follower_profiles = []
        for follower in followers:
            stats = await self.get_user_stats(follower.id, db)
            follower_profiles.append(
                UserPublicProfile(
                    id=follower.id,
                    name=follower.name,
                    bio=follower.bio,
                    location=follower.location,
                    avatar_url=follower.avatar_url,
                    role=follower.role,
                    is_verified=follower.is_verified,
                    created_at=follower.created_at,
                    stats=stats
                )
            )
        
        return UserListResponse(
            users=follower_profiles,
            total=total,
            page=page,
            per_page=per_page,
            has_next=(offset + per_page) < total,
            has_prev=page > 1
        )
    
    async def get_user_following(
        self, 
        user_id: UUID, 
        page: int, 
        per_page: int, 
        db: AsyncSession
    ) -> UserListResponse:
        """Get paginated list of users that the user is following"""
        offset = (page - 1) * per_page
        
        # Get total count
        total_query = select(func.count(UserFollow.following_id)).where(
            UserFollow.follower_id == user_id
        )
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0
        
        # Get following with user details
        following_query = (
            select(User)
            .join(UserFollow, User.id == UserFollow.following_id)
            .where(UserFollow.follower_id == user_id)
            .order_by(UserFollow.created_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        
        following_result = await db.execute(following_query)
        following = following_result.scalars().all()
        
        # Convert to public profiles
        following_profiles = []
        for followed_user in following:
            stats = await self.get_user_stats(followed_user.id, db)
            following_profiles.append(
                UserPublicProfile(
                    id=followed_user.id,
                    name=followed_user.name,
                    bio=followed_user.bio,
                    location=followed_user.location,
                    avatar_url=followed_user.avatar_url,
                    role=followed_user.role,
                    is_verified=followed_user.is_verified,
                    created_at=followed_user.created_at,
                    stats=stats
                )
            )
        
        return UserListResponse(
            users=following_profiles,
            total=total,
            page=page,
            per_page=per_page,
            has_next=(offset + per_page) < total,
            has_prev=page > 1
        )
    
    async def get_activity_feed(
        self, 
        user_id: UUID, 
        page: int, 
        per_page: int, 
        db: AsyncSession
    ) -> ActivityFeedResponse:
        """Get activity feed for a user based on who they follow"""
        offset = (page - 1) * per_page
        
        # Get list of users that this user follows
        following_query = select(UserFollow.following_id).where(
            UserFollow.follower_id == user_id
        )
        following_result = await db.execute(following_query)
        following_ids = [row[0] for row in following_result.fetchall()]
        
        if not following_ids:
            # User doesn't follow anyone, return empty feed
            return ActivityFeedResponse(
                activities=[],
                total=0,
                page=page,
                per_page=per_page,
                has_next=False,
                has_prev=False
            )
        
        activities = []
        
        # Get recent reviews from followed users
        reviews_query = (
            select(Review, User, Movie)
            .join(User, Review.user_id == User.id)
            .join(Movie, Review.movie_id == Movie.id)
            .where(Review.user_id.in_(following_ids))
            .order_by(Review.created_at.desc())
            .limit(per_page * 2)  # Get more to mix with other activities
        )
        
        reviews_result = await db.execute(reviews_query)
        reviews = reviews_result.fetchall()
        
        for review, user, movie in reviews:
            user_stats = await self.get_user_stats(user.id, db)
            user_profile = UserPublicProfile(
                id=user.id,
                name=user.name,
                bio=user.bio,
                location=user.location,
                avatar_url=user.avatar_url,
                role=user.role,
                is_verified=user.is_verified,
                created_at=user.created_at,
                stats=user_stats
            )
            
            activities.append(ActivityItem(
                id=review.id,
                type="review_posted",
                user=user_profile,
                title=f"{user.name} reviewed {movie.title}",
                description=f"Rated {review.lemon_pie_rating}/10: {review.review_text[:100]}{'...' if len(review.review_text) > 100 else ''}",
                data={
                    "movie_id": str(movie.id),
                    "movie_title": movie.title,
                    "rating": review.lemon_pie_rating,
                    "review_id": str(review.id)
                },
                created_at=review.created_at
            ))
        
        # Get recent follows from followed users
        from sqlalchemy.orm import aliased
        follower_alias = aliased(User)
        followed_alias = aliased(User)
        
        follows_query = (
            select(UserFollow, follower_alias, followed_alias)
            .join(follower_alias, UserFollow.follower_id == follower_alias.id)
            .join(followed_alias, UserFollow.following_id == followed_alias.id)
            .where(UserFollow.follower_id.in_(following_ids))
            .order_by(UserFollow.created_at.desc())
            .limit(per_page)
        )
        
        follows_result = await db.execute(follows_query)
        follows = follows_result.fetchall()
        
        for follow, follower, followed in follows:
            follower_stats = await self.get_user_stats(follower.id, db)
            follower_profile = UserPublicProfile(
                id=follower.id,
                name=follower.name,
                bio=follower.bio,
                location=follower.location,
                avatar_url=follower.avatar_url,
                role=follower.role,
                is_verified=follower.is_verified,
                created_at=follower.created_at,
                stats=follower_stats
            )
            
            activities.append(ActivityItem(
                id=follow.follower_id,  # Using follower_id as unique identifier
                type="user_followed",
                user=follower_profile,
                title=f"{follower.name} followed {followed.name}",
                description=f"{follower.name} started following {followed.name}",
                data={
                    "followed_user_id": str(followed.id),
                    "followed_user_name": followed.name
                },
                created_at=follow.created_at
            ))
        
        # Get recent watchlist additions from followed users
        watchlist_query = (
            select(UserWatchlist, User, Movie)
            .join(User, UserWatchlist.user_id == User.id)
            .join(Movie, UserWatchlist.movie_id == Movie.id)
            .where(UserWatchlist.user_id.in_(following_ids))
            .order_by(UserWatchlist.added_at.desc())
            .limit(per_page)
        )
        
        watchlist_result = await db.execute(watchlist_query)
        watchlist_items = watchlist_result.fetchall()
        
        for watchlist_item, user, movie in watchlist_items:
            user_stats = await self.get_user_stats(user.id, db)
            user_profile = UserPublicProfile(
                id=user.id,
                name=user.name,
                bio=user.bio,
                location=user.location,
                avatar_url=user.avatar_url,
                role=user.role,
                is_verified=user.is_verified,
                created_at=user.created_at,
                stats=user_stats
            )
            
            activities.append(ActivityItem(
                id=watchlist_item.user_id,  # Using combination as unique identifier
                type="movie_watchlisted",
                user=user_profile,
                title=f"{user.name} added {movie.title} to watchlist",
                description=f"{user.name} wants to watch {movie.title}",
                data={
                    "movie_id": str(movie.id),
                    "movie_title": movie.title
                },
                created_at=watchlist_item.added_at
            ))
        
        # Sort all activities by creation time and paginate
        activities.sort(key=lambda x: x.created_at, reverse=True)
        total = len(activities)
        
        # Apply pagination
        paginated_activities = activities[offset:offset + per_page]
        
        return ActivityFeedResponse(
            activities=paginated_activities,
            total=total,
            page=page,
            per_page=per_page,
            has_next=(offset + per_page) < total,
            has_prev=page > 1
        )
    
    async def add_to_watchlist(
        self, 
        user_id: UUID, 
        movie_id: UUID, 
        db: AsyncSession
    ) -> None:
        """Add a movie to user's watchlist"""
        # Check if movie exists
        movie = await db.execute(select(Movie).where(Movie.id == movie_id))
        if not movie.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found"
            )
        
        # Check if already in watchlist
        existing = await db.execute(
            select(UserWatchlist).where(
                and_(
                    UserWatchlist.user_id == user_id,
                    UserWatchlist.movie_id == movie_id
                )
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Movie already in watchlist"
            )
        
        # Add to watchlist
        watchlist_item = UserWatchlist(user_id=user_id, movie_id=movie_id)
        db.add(watchlist_item)
        await db.commit()
    
    async def remove_from_watchlist(
        self, 
        user_id: UUID, 
        movie_id: UUID, 
        db: AsyncSession
    ) -> None:
        """Remove a movie from user's watchlist"""
        # Find and delete the watchlist item
        watchlist_item = await db.execute(
            select(UserWatchlist).where(
                and_(
                    UserWatchlist.user_id == user_id,
                    UserWatchlist.movie_id == movie_id
                )
            )
        )
        item = watchlist_item.scalar_one_or_none()
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not in watchlist"
            )
        
        await db.delete(item)
        await db.commit()
    
    async def get_user_watchlist(
        self, 
        user_id: UUID, 
        page: int, 
        per_page: int, 
        db: AsyncSession
    ) -> MovieListResponse:
        """Get user's watchlist with pagination"""
        offset = (page - 1) * per_page
        
        # Get total count
        total_query = select(func.count(UserWatchlist.movie_id)).where(
            UserWatchlist.user_id == user_id
        )
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0
        
        # Get watchlist items with movie details
        watchlist_query = (
            select(UserWatchlist, Movie)
            .join(Movie, UserWatchlist.movie_id == Movie.id)
            .where(UserWatchlist.user_id == user_id)
            .order_by(UserWatchlist.added_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        
        watchlist_result = await db.execute(watchlist_query)
        watchlist_items = watchlist_result.fetchall()
        
        # Convert to movie list items
        movies = []
        for watchlist_item, movie in watchlist_items:
            movies.append(
                MovieListItem(
                    id=movie.id,
                    title=movie.title,
                    local_title=movie.local_title,
                    release_date=movie.release_date,
                    runtime=movie.runtime,
                    plot_summary=movie.plot_summary,
                    poster_url=movie.poster_url,
                    director=movie.director,
                    added_at=watchlist_item.added_at
                )
            )
        
        return MovieListResponse(
            movies=movies,
            total=total,
            page=page,
            per_page=per_page,
            has_next=(offset + per_page) < total,
            has_prev=page > 1
        )
    
    async def add_to_favorites(
        self, 
        user_id: UUID, 
        movie_id: UUID, 
        db: AsyncSession
    ) -> None:
        """Add a movie to user's favorites"""
        # Check if movie exists
        movie = await db.execute(select(Movie).where(Movie.id == movie_id))
        if not movie.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found"
            )
        
        # Check if already in favorites
        existing = await db.execute(
            select(UserFavorite).where(
                and_(
                    UserFavorite.user_id == user_id,
                    UserFavorite.movie_id == movie_id
                )
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Movie already in favorites"
            )
        
        # Add to favorites
        favorite_item = UserFavorite(user_id=user_id, movie_id=movie_id)
        db.add(favorite_item)
        await db.commit()
    
    async def remove_from_favorites(
        self, 
        user_id: UUID, 
        movie_id: UUID, 
        db: AsyncSession
    ) -> None:
        """Remove a movie from user's favorites"""
        # Find and delete the favorite item
        favorite_item = await db.execute(
            select(UserFavorite).where(
                and_(
                    UserFavorite.user_id == user_id,
                    UserFavorite.movie_id == movie_id
                )
            )
        )
        item = favorite_item.scalar_one_or_none()
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not in favorites"
            )
        
        await db.delete(item)
        await db.commit()
    
    async def get_user_favorites(
        self, 
        user_id: UUID, 
        page: int, 
        per_page: int, 
        db: AsyncSession
    ) -> MovieListResponse:
        """Get user's favorites with pagination"""
        offset = (page - 1) * per_page
        
        # Get total count
        total_query = select(func.count(UserFavorite.movie_id)).where(
            UserFavorite.user_id == user_id
        )
        total_result = await db.execute(total_query)
        total = total_result.scalar() or 0
        
        # Get favorite items with movie details
        favorites_query = (
            select(UserFavorite, Movie)
            .join(Movie, UserFavorite.movie_id == Movie.id)
            .where(UserFavorite.user_id == user_id)
            .order_by(UserFavorite.added_at.desc())
            .offset(offset)
            .limit(per_page)
        )
        
        favorites_result = await db.execute(favorites_query)
        favorite_items = favorites_result.fetchall()
        
        # Convert to movie list items
        movies = []
        for favorite_item, movie in favorite_items:
            movies.append(
                MovieListItem(
                    id=movie.id,
                    title=movie.title,
                    local_title=movie.local_title,
                    release_date=movie.release_date,
                    runtime=movie.runtime,
                    plot_summary=movie.plot_summary,
                    poster_url=movie.poster_url,
                    director=movie.director,
                    added_at=favorite_item.added_at
                )
            )
        
        return MovieListResponse(
            movies=movies,
            total=total,
            page=page,
            per_page=per_page,
            has_next=(offset + per_page) < total,
            has_prev=page > 1
        )


# Create service instance
user_service = UserService()