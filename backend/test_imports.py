#!/usr/bin/env python3
"""
Test imports to isolate the FastAPI error
"""
import sys
import traceback

def test_import(module_name, description):
    """Test importing a module and report any errors"""
    try:
        print(f"Testing {description}...")
        if module_name == "app.main":
            from app.main import create_app
            app = create_app()
            print(f"✓ {description} - SUCCESS")
            return True
        else:
            __import__(module_name)
            print(f"✓ {description} - SUCCESS")
            return True
    except Exception as e:
        print(f"✗ {description} - FAILED: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing imports to isolate FastAPI error...\n")
    
    # Test basic imports first
    test_import("fastapi", "FastAPI")
    test_import("uvicorn", "Uvicorn")
    test_import("pydantic", "Pydantic")
    test_import("sqlalchemy", "SQLAlchemy")
    
    print("\nTesting app modules...")
    test_import("app.core.config", "Config")
    test_import("app.core.logging", "Logging")
    test_import("app.core.exceptions", "Exceptions")
    test_import("app.db.database", "Database")
    test_import("app.models.user", "User Model")
    test_import("app.models.movie", "Movie Model")
    test_import("app.models.review", "Review Model")
    
    print("\nTesting services...")
    test_import("app.services.user_service", "User Service")
    test_import("app.services.movie_service", "Movie Service")
    test_import("app.services.review_service", "Review Service")
    
    print("\nTesting API routers...")
    test_import("app.api.v1.auth", "Auth Router")
    test_import("app.api.v1.users", "Users Router")
    test_import("app.api.v1.movies", "Movies Router")
    test_import("app.api.v1.reviews", "Reviews Router")
    
    print("\nTesting main application...")
    test_import("app.main", "Main Application")
    
    print("\nImport testing complete!")