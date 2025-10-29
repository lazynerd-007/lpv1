#!/usr/bin/env python3
"""
Test endpoint parameter validation to isolate the FastAPIError
"""
import sys
import traceback
from fastapi import FastAPI, Depends, Query
from typing import Optional
from uuid import UUID

def test_endpoint_parameters():
    """Test endpoint parameter validation"""
    try:
        print("Testing endpoint parameter validation...")
        
        # Create a test FastAPI app
        app = FastAPI()
        
        # Import dependencies
        from app.auth.dependencies import get_optional_current_user
        from app.models.user import User
        from sqlalchemy.ext.asyncio import AsyncSession
        from app.db.database import get_db
        from app.services.review_service import get_review_service, ReviewService
        from app.schemas.review import PaginatedReviewResponse
        
        print("  ✓ Dependencies imported successfully")
        
        # Test the problematic endpoint signature
        @app.get("/test-reviews/", response_model=PaginatedReviewResponse)
        async def test_get_reviews(
            page: int = Query(1, ge=1, description="Page number"),
            limit: int = Query(20, ge=1, le=100, description="Items per page"),
            movie_id: Optional[UUID] = Query(None, description="Filter by movie ID"),
            user_id: Optional[UUID] = Query(None, description="Filter by user ID"),
            rating_min: Optional[int] = Query(None, ge=1, le=10, description="Minimum rating filter"),
            rating_max: Optional[int] = Query(None, ge=1, le=10, description="Maximum rating filter"),
            spoiler_warning: Optional[bool] = Query(None, description="Filter by spoiler warning"),
            sort_field: str = Query("created_at", regex="^(created_at|updated_at|lemon_pie_rating|helpful_votes|helpfulness_score)$", description="Sort field"),
            sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
            current_user: Optional[User] = Depends(get_optional_current_user),
            db: AsyncSession = Depends(get_db),
            review_service: ReviewService = Depends(get_review_service)
        ):
            """Test endpoint with same signature as problematic one"""
            return {"message": "test"}
        
        print("  ✓ Test endpoint created successfully")
        
        # Get all routes to verify
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                routes.append(f"  - {route.methods} {route.path}")
        
        print(f"  ✓ Found {len(routes)} routes")
        for route in routes:
            print(route)
        
        return True
        
    except Exception as e:
        print(f"  ✗ Endpoint parameter validation failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Test endpoint parameter validation"""
    success = test_endpoint_parameters()
    if success:
        print("\n✓ Endpoint parameter validation passed")
    else:
        print("\n✗ Endpoint parameter validation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()