#!/usr/bin/env python3
"""
Test to identify specific router conflict
"""
import sys
import traceback
from fastapi import FastAPI

def test_specific_combination():
    """Test the specific combination that fails"""
    try:
        print("Testing Auth + Movies + Reviews combination...")
        
        # Create a test FastAPI app
        app = FastAPI()
        
        # Import and add auth router
        print("  Adding auth router...")
        from app.api.v1.auth import router as auth_router
        app.include_router(auth_router, prefix="/api/v1")
        print("  ✓ Auth router added")
        
        # Import and add movies router
        print("  Adding movies router...")
        from app.api.v1.movies import router as movies_router
        app.include_router(movies_router, prefix="/api/v1")
        print("  ✓ Movies router added")
        
        # Import and add reviews router (this should fail)
        print("  Adding reviews router...")
        from app.api.v1.reviews import router as reviews_router
        app.include_router(reviews_router, prefix="/api/v1")
        print("  ✓ Reviews router added")
        
        print("✓ All routers added successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Failed: {e}")
        traceback.print_exc()
        return False

def test_reviews_alone():
    """Test reviews router alone"""
    try:
        print("\nTesting Reviews router alone...")
        
        # Create a test FastAPI app
        app = FastAPI()
        
        # Import and add reviews router
        from app.api.v1.reviews import router as reviews_router
        app.include_router(reviews_router, prefix="/api/v1")
        print("✓ Reviews router works alone")
        return True
        
    except Exception as e:
        print(f"✗ Reviews router failed alone: {e}")
        traceback.print_exc()
        return False

def main():
    """Test router conflicts"""
    test_reviews_alone()
    test_specific_combination()

if __name__ == "__main__":
    main()