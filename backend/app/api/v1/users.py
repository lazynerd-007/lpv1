"""
User management API routes
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.auth.dependencies import get_current_user, get_optional_current_user
from app.services.user_service import user_service
from app.schemas.user import (
    UserProfileUpdate,
    UserProfileResponse,
    UserPublicProfile,
    UserStats,
    UserListResponse,
    ActivityFeedResponse,
    MovieListResponse
)
from app.schemas.privacy import (
    PrivacySettingsUpdate,
    PrivacySettingsResponse,
    PasswordChangeRequest,
    PasswordChangeResponse,
    TwoFactorAuthStatus,
    TwoFactorAuthSetupRequest,
    TwoFactorAuthSetupResponse,
    TwoFactorAuthVerifyRequest,
    TwoFactorAuthToggleRequest
)
from app.models.user import User


router = APIRouter(tags=["User Management"])


@router.get("/profile", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's profile with statistics
    
    Returns the authenticated user's complete profile including:
    - Personal information
    - Statistics (reviews, followers, etc.)
    - Account status
    """
    return await user_service.get_user_profile(
        current_user.id, 
        db, 
        requesting_user_id=current_user.id
    )


@router.put("/profile", response_model=UserProfileResponse)
async def update_current_user_profile(
    update_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user's profile
    
    - **name**: Full name (2-255 characters, letters/spaces/hyphens/apostrophes only)
    - **bio**: User biography (max 1000 characters)
    - **location**: User location (max 255 characters)
    - **avatar_url**: URL to user's avatar image (max 500 characters)
    
    All fields are optional. Only provided fields will be updated.
    """
    # Update the user profile
    updated_user = await user_service.update_user_profile(
        current_user.id, 
        update_data, 
        db
    )
    
    # Return updated profile with statistics
    return await user_service.get_user_profile(
        updated_user.id, 
        db, 
        requesting_user_id=current_user.id
    )


@router.get("/{user_id}", response_model=UserPublicProfile)
async def get_user_profile(
    user_id: UUID,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get public profile of a specific user
    
    - **user_id**: UUID of the user to retrieve
    
    Returns public profile information including:
    - Basic information (name, bio, location, avatar)
    - User role and verification status
    - Public statistics (review count, followers, etc.)
    
    Note: Email address is not included in public profiles.
    """
    return await user_service.get_public_profile(user_id, db)


@router.get("/{user_id}/stats", response_model=UserStats)
async def get_user_statistics(
    user_id: UUID,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get statistics for a specific user
    
    - **user_id**: UUID of the user
    
    Returns user statistics including:
    - Total number of reviews
    - Average rating given
    - Follower and following counts
    - Watchlist and favorites counts
    """
    # Verify user exists
    user = await user_service.get_user_by_id(user_id, db, include_stats=False)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return await user_service.get_user_stats(user_id, db)


@router.post("/{user_id}/follow")
async def follow_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Follow a user
    
    - **user_id**: UUID of the user to follow
    
    Creates a following relationship between the current user and the target user.
    Users cannot follow themselves.
    """
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot follow yourself"
        )
    
    await user_service.follow_user(current_user.id, user_id, db)
    return {"message": "User followed successfully"}


@router.delete("/{user_id}/follow")
async def unfollow_user(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Unfollow a user
    
    - **user_id**: UUID of the user to unfollow
    
    Removes the following relationship between the current user and the target user.
    """
    await user_service.unfollow_user(current_user.id, user_id, db)
    return {"message": "User unfollowed successfully"}


@router.get("/{user_id}/followers", response_model=UserListResponse)
async def get_user_followers(
    user_id: UUID,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of users following the specified user
    
    - **user_id**: UUID of the user
    - **page**: Page number (default: 1)
    - **per_page**: Items per page (default: 20, max: 100)
    
    Returns paginated list of followers with their public profiles.
    """
    # Verify user exists
    user = await user_service.get_user_by_id(user_id, db, include_stats=False)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return await user_service.get_user_followers(user_id, page, per_page, db)


@router.get("/{user_id}/following", response_model=UserListResponse)
async def get_user_following(
    user_id: UUID,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of users that the specified user is following
    
    - **user_id**: UUID of the user
    - **page**: Page number (default: 1)
    - **per_page**: Items per page (default: 20, max: 100)
    
    Returns paginated list of users being followed with their public profiles.
    """
    # Verify user exists
    user = await user_service.get_user_by_id(user_id, db, include_stats=False)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return await user_service.get_user_following(user_id, page, per_page, db)


@router.get("/activity-feed", response_model=ActivityFeedResponse)
async def get_activity_feed(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get activity feed for the current user
    
    - **page**: Page number (default: 1)
    - **per_page**: Items per page (default: 20, max: 100)
    
    Returns recent activities from users that the current user follows, including:
    - New reviews posted
    - New users followed
    - Movies added to watchlist/favorites
    
    Activities are ordered by creation time (most recent first).
    """
    return await user_service.get_activity_feed(current_user.id, page, per_page, db)


@router.post("/watchlist/{movie_id}")
async def add_to_watchlist(
    movie_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a movie to the user's watchlist
    
    - **movie_id**: UUID of the movie to add to watchlist
    
    Adds the specified movie to the current user's watchlist.
    Movies cannot be added twice to the same watchlist.
    """
    await user_service.add_to_watchlist(current_user.id, movie_id, db)
    return {"message": "Movie added to watchlist successfully"}


@router.delete("/watchlist/{movie_id}")
async def remove_from_watchlist(
    movie_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove a movie from the user's watchlist
    
    - **movie_id**: UUID of the movie to remove from watchlist
    
    Removes the specified movie from the current user's watchlist.
    """
    await user_service.remove_from_watchlist(current_user.id, movie_id, db)
    return {"message": "Movie removed from watchlist successfully"}


@router.get("/watchlist", response_model=MovieListResponse)
async def get_user_watchlist(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user's watchlist
    
    - **page**: Page number (default: 1)
    - **per_page**: Items per page (default: 20, max: 100)
    
    Returns paginated list of movies in the user's watchlist with movie details.
    """
    return await user_service.get_user_watchlist(current_user.id, page, per_page, db)


@router.post("/favorites/{movie_id}")
async def add_to_favorites(
    movie_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add a movie to the user's favorites
    
    - **movie_id**: UUID of the movie to add to favorites
    
    Adds the specified movie to the current user's favorites list.
    Movies cannot be added twice to the same favorites list.
    """
    await user_service.add_to_favorites(current_user.id, movie_id, db)
    return {"message": "Movie added to favorites successfully"}


@router.delete("/favorites/{movie_id}")
async def remove_from_favorites(
    movie_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove a movie from the user's favorites
    
    - **movie_id**: UUID of the movie to remove from favorites
    
    Removes the specified movie from the current user's favorites list.
    """
    await user_service.remove_from_favorites(current_user.id, movie_id, db)
    return {"message": "Movie removed from favorites successfully"}


@router.get("/favorites", response_model=MovieListResponse)
async def get_user_favorites(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user's favorites
    
    - **page**: Page number (default: 1)
    - **per_page**: Items per page (default: 20, max: 100)
    
    Returns paginated list of movies in the user's favorites with movie details.
    """
    return await user_service.get_user_favorites(current_user.id, page, per_page, db)


# Privacy Settings Endpoints

@router.get("/privacy-settings", response_model=PrivacySettingsResponse)
async def get_privacy_settings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user's privacy settings
    
    Returns the user's privacy settings including profile visibility,
    watchlist visibility, analytics tracking, and personalized recommendations.
    """
    return await user_service.get_privacy_settings(current_user.id, db)


@router.put("/privacy-settings", response_model=PrivacySettingsResponse)
async def update_privacy_settings(
    settings: PrivacySettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update the current user's privacy settings
    
    - **profile_visibility**: Who can view the user's profile (public, friends, private)
    - **watchlist_visibility**: Who can view the user's watchlist (public, friends, private)
    - **analytics_tracking**: Whether to allow analytics tracking
    - **personalized_recommendations**: Whether to enable personalized recommendations
    
    Updates the user's privacy settings with the provided values.
    """
    return await user_service.update_privacy_settings(current_user.id, settings, db)


# Account Management Endpoints

@router.post("/change-password", response_model=PasswordChangeResponse)
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Change the current user's password
    
    - **current_password**: The user's current password
    - **new_password**: The new password (minimum 8 characters)
    - **confirm_password**: Confirmation of the new password
    
    Changes the user's password after verifying the current password.
    """
    # Validate passwords match
    password_data.validate_passwords_match()
    return await user_service.change_password(current_user.id, password_data, db)


@router.get("/2fa/status", response_model=TwoFactorAuthStatus)
async def get_2fa_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user's 2FA status
    
    Returns whether 2FA is enabled and the number of backup codes available.
    """
    return await user_service.get_2fa_status(current_user.id, db)


@router.post("/2fa/setup", response_model=TwoFactorAuthSetupResponse)
async def setup_2fa(
    setup_data: TwoFactorAuthSetupRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Setup 2FA for the current user
    
    - **password**: Current password for verification
    
    Generates a QR code and secret key for setting up 2FA authentication.
    Also provides backup codes for account recovery.
    """
    return await user_service.setup_2fa(current_user.id, setup_data, db)


@router.post("/2fa/verify")
async def verify_2fa_setup(
    verify_data: TwoFactorAuthVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Verify and enable 2FA setup
    
    - **code**: 6-digit verification code from authenticator app
    
    Verifies the 2FA setup and enables 2FA for the user account.
    """
    return await user_service.verify_2fa_setup(current_user.id, verify_data, db)


@router.post("/2fa/toggle")
async def toggle_2fa(
    toggle_data: TwoFactorAuthToggleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Enable or disable 2FA
    
    - **password**: Current password for verification
    - **code**: 6-digit verification code from authenticator app
    - **enabled**: Whether to enable or disable 2FA
    
    Enables or disables 2FA for the user account after verification.
    """
    return await user_service.toggle_2fa(current_user.id, toggle_data, db)