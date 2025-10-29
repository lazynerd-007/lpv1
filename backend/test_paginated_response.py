#!/usr/bin/env python3
"""
Test PaginatedReviewResponse schema to isolate the FastAPIError
"""
import sys
import traceback
from fastapi import FastAPI

def test_paginated_response():
    """Test PaginatedReviewResponse as response model"""
    try:
        print("Testing PaginatedReviewResponse...")
        
        # Create a test FastAPI app
        app = FastAPI()
        
        # Import the schema
        from app.schemas.review import PaginatedReviewResponse
        print("  ✓ PaginatedReviewResponse imported successfully")
        
        # Test using it as response_model
        @app.get("/test1/", response_model=PaginatedReviewResponse)
        async def test_endpoint1():
            """Test endpoint with PaginatedReviewResponse"""
            return {"message": "test"}
        
        print("  ✓ Endpoint with PaginatedReviewResponse created successfully")
        
        # Test with ReviewListResponse directly
        from app.schemas.review import ReviewListResponse
        from typing import List
        
        @app.get("/test2/", response_model=List[ReviewListResponse])
        async def test_endpoint2():
            """Test endpoint with List[ReviewListResponse]"""
            return {"message": "test"}
        
        print("  ✓ Endpoint with List[ReviewListResponse] created successfully")
        
        # Test with ReviewResponse
        from app.schemas.review import ReviewResponse
        
        @app.get("/test3/", response_model=ReviewResponse)
        async def test_endpoint3():
            """Test endpoint with ReviewResponse"""
            return {"message": "test"}
        
        print("  ✓ Endpoint with ReviewResponse created successfully")
        
        return True
        
    except Exception as e:
        print(f"  ✗ PaginatedReviewResponse test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Test PaginatedReviewResponse"""
    success = test_paginated_response()
    if success:
        print("\n✓ PaginatedReviewResponse test passed")
    else:
        print("\n✗ PaginatedReviewResponse test failed")
        sys.exit(1)

if __name__ == "__main__":
    main()