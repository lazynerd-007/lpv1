#!/usr/bin/env python3
"""
Test the get_review_service dependency specifically
"""
import sys
import traceback
from fastapi import FastAPI, Depends

def test_service_dependency():
    """Test the review service dependency"""
    try:
        print("Testing review service dependency...")
        
        # Create a test FastAPI app
        app = FastAPI()
        
        # Import the dependency function
        from app.services.review_service import get_review_service
        print("  ✓ get_review_service imported successfully")
        
        # Check the function signature
        import inspect
        sig = inspect.signature(get_review_service)
        print(f"  - Function signature: {sig}")
        print(f"  - Return annotation: {sig.return_annotation}")
        
        # Test using it as a dependency
        @app.get("/test/")
        async def test_endpoint(review_service = Depends(get_review_service)):
            return {"message": "test"}
        
        print("  ✓ Dependency works without type annotation")
        
        # Test with type annotation
        from app.services.review_service import ReviewService
        
        @app.get("/test2/")
        async def test_endpoint2(review_service: ReviewService = Depends(get_review_service)):
            return {"message": "test2"}
        
        print("  ✓ Dependency works with type annotation")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Service dependency test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Test service dependency"""
    success = test_service_dependency()
    if success:
        print("\n✓ Service dependency test passed")
    else:
        print("\n✗ Service dependency test failed")
        sys.exit(1)

if __name__ == "__main__":
    main()