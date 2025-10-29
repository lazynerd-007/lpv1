#!/usr/bin/env python3
"""
Test dependencies in isolation to find the FastAPIError source
"""
import sys
import traceback
from fastapi import FastAPI, Depends
from typing import Optional
from uuid import UUID

def test_dependencies_isolation():
    """Test each dependency individually"""
    try:
        print("Testing dependencies in isolation...")
        
        # Create a test FastAPI app
        app = FastAPI()
        
        # Test 1: Basic dependencies
        print("  - Testing basic dependencies...")
        from sqlalchemy.ext.asyncio import AsyncSession
        from app.db.database import get_db
        
        @app.get("/test1/")
        async def test_endpoint1(db: AsyncSession = Depends(get_db)):
            return {"message": "test1"}
        
        print("  ✓ Basic database dependency works")
        
        # Test 2: Auth dependencies
        print("  - Testing auth dependencies...")
        from app.auth.dependencies import get_optional_current_user
        from app.models.user import User
        
        @app.get("/test2/")
        async def test_endpoint2(
            current_user: Optional[User] = Depends(get_optional_current_user),
            db: AsyncSession = Depends(get_db)
        ):
            return {"message": "test2"}
        
        print("  ✓ Auth dependencies work")
        
        # Test 3: Service dependencies
        print("  - Testing service dependencies...")
        from app.services.review_service import get_review_service, ReviewService
        
        @app.get("/test3/")
        async def test_endpoint3(
            review_service: ReviewService = Depends(get_review_service),
            db: AsyncSession = Depends(get_db)
        ):
            return {"message": "test3"}
        
        print("  ✓ Service dependencies work")
        
        # Test 4: Combined dependencies without response model
        print("  - Testing combined dependencies...")
        
        @app.get("/test4/")
        async def test_endpoint4(
            current_user: Optional[User] = Depends(get_optional_current_user),
            db: AsyncSession = Depends(get_db),
            review_service: ReviewService = Depends(get_review_service)
        ):
            return {"message": "test4"}
        
        print("  ✓ Combined dependencies work")
        
        # Test 5: Add response model
        print("  - Testing with response model...")
        from app.schemas.review import PaginatedReviewResponse
        
        @app.get("/test5/", response_model=PaginatedReviewResponse)
        async def test_endpoint5(
            current_user: Optional[User] = Depends(get_optional_current_user),
            db: AsyncSession = Depends(get_db),
            review_service: ReviewService = Depends(get_review_service)
        ):
            return {"message": "test5"}
        
        print("  ✓ Response model with dependencies works")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Dependency isolation test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Test dependency isolation"""
    success = test_dependencies_isolation()
    if success:
        print("\n✓ All dependency tests passed")
    else:
        print("\n✗ Dependency tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()