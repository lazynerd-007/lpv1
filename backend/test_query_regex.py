#!/usr/bin/env python3
"""
Test Query regex parameters to isolate the FastAPIError
"""
import sys
import traceback
from fastapi import FastAPI, Query

def test_query_regex():
    """Test Query parameters with regex"""
    try:
        print("Testing Query regex parameters...")
        
        # Create a test FastAPI app
        app = FastAPI()
        
        # Test endpoint with regex Query parameters
        @app.get("/test1/")
        async def test_endpoint1(
            sort_field: str = Query("created_at", regex="^(created_at|updated_at|lemon_pie_rating|helpful_votes|helpfulness_score)$", description="Sort field"),
            sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order")
        ):
            """Test endpoint with regex Query parameters"""
            return {"sort_field": sort_field, "sort_order": sort_order}
        
        print("  ✓ Endpoint with regex Query parameters created successfully")
        
        # Test endpoint with regex and response model
        from app.schemas.review import PaginatedReviewResponse
        
        @app.get("/test2/", response_model=PaginatedReviewResponse)
        async def test_endpoint2(
            sort_field: str = Query("created_at", regex="^(created_at|updated_at|lemon_pie_rating|helpful_votes|helpfulness_score)$", description="Sort field"),
            sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order")
        ):
            """Test endpoint with regex Query parameters and response model"""
            return {"message": "test"}
        
        print("  ✓ Endpoint with regex Query + response model created successfully")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Query regex test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Test Query regex parameters"""
    success = test_query_regex()
    if success:
        print("\n✓ Query regex test passed")
    else:
        print("\n✗ Query regex test failed")
        sys.exit(1)

if __name__ == "__main__":
    main()