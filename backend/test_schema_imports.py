#!/usr/bin/env python3
"""
Test schema imports to isolate the FastAPIError
"""
import sys
import traceback

def test_schema_imports():
    """Test importing schemas individually"""
    try:
        print("Testing schema imports...")
        
        # Test user schemas
        print("  - Importing user schemas...")
        from app.schemas.user import UserPublicProfile, UserStats
        print("  ✓ User schemas imported successfully")
        
        # Test review schemas
        print("  - Importing review schemas...")
        from app.schemas.review import (
            ReviewResponse, 
            ReviewListResponse, 
            PaginatedReviewResponse,
            ReviewCreate,
            ReviewUpdate
        )
        print("  ✓ Review schemas imported successfully")
        
        # Test creating instances
        print("  - Testing schema instantiation...")
        from uuid import uuid4
        from datetime import datetime
        from app.models.enums import UserRole, ModerationStatus, VoteType
        
        # Create a UserPublicProfile instance
        user_data = {
            "id": uuid4(),
            "name": "Test User",
            "bio": "Test bio",
            "location": "Test location",
            "avatar_url": "https://example.com/avatar.jpg",
            "role": UserRole.USER,
            "is_verified": False,
            "created_at": datetime.now()
        }
        user_profile = UserPublicProfile(**user_data)
        print("  ✓ UserPublicProfile created successfully")
        
        # Create a ReviewResponse instance
        review_data = {
            "id": uuid4(),
            "user": user_profile,
            "movie_id": uuid4(),
            "lemon_pie_rating": 8,
            "review_text": "This is a test review with enough content to pass validation.",
            "spoiler_warning": False,
            "helpful_votes": 5,
            "unhelpful_votes": 1,
            "helpfulness_score": 4,
            "user_vote": VoteType.HELPFUL,
            "is_flagged": False,
            "moderation_status": ModerationStatus.APPROVED,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "review_language": "en"
        }
        review_response = ReviewResponse(**review_data)
        print("  ✓ ReviewResponse created successfully")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Schema import/instantiation failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Test schema imports"""
    success = test_schema_imports()
    if success:
        print("\n✓ All schema tests passed")
    else:
        print("\n✗ Schema tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()