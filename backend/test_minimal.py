#!/usr/bin/env python3
"""
Minimal test server to check if FastAPI works
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Test API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/api/v1/auth/login")
async def login():
    return {"message": "Login endpoint"}

if __name__ == "__main__":
    uvicorn.run(
        "test_minimal:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )