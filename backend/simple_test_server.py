#!/usr/bin/env python3
"""
Simple test server to verify login endpoint works
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_simple_app():
    """Create a simple FastAPI app for testing"""
    app = FastAPI(title="Simple Test Server")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Simple test endpoint
    @app.get("/")
    async def root():
        return {"message": "Simple test server running"}
    
    # Test login endpoint (simplified)
    @app.post("/api/v1/auth/login")
    async def test_login(data: dict):
        return {
            "message": "Login endpoint is working",
            "received_data": data,
            "status": "POST request accepted"
        }
    
    return app

if __name__ == "__main__":
    app = create_simple_app()
    print("Starting simple test server on http://localhost:8000")
    print("Test the login endpoint with: POST http://localhost:8000/api/v1/auth/login")
    uvicorn.run(app, host="0.0.0.0", port=8000)