"""
Simple test server to verify basic FastAPI setup with authentication
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import jwt
from datetime import datetime, timedelta, date
import uuid

app = FastAPI(title="LemonNPie Test API", version="1.0.0")
security = HTTPBearer()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock user data (matching the frontend mock data)
MOCK_USERS = {
    "admin@admin.com": {
        "id": "1",
        "name": "Adebayo Johnson",
        "email": "admin@admin.com",
        "password": "admin123",
        "bio": "Passionate Nollywood enthusiast and film critic",
        "location": "Lagos, Nigeria",
        "role": "admin",
        "isActive": True,
        "loginAttempts": 0
    },
    "user@test.com": {
        "id": "2",
        "name": "Funmi Adebayo",
        "email": "user@test.com",
        "password": "password123",
        "bio": "Movie lover and weekend binge-watcher",
        "location": "Abuja, Nigeria",
        "role": "user",
        "isActive": True,
        "loginAttempts": 0
    },
    "moderator@test.com": {
        "id": "3",
        "name": "Kemi Okafor",
        "email": "moderator@test.com",
        "password": "mod123456",
        "bio": "Community moderator and film enthusiast",
        "location": "Port Harcourt, Nigeria",
        "role": "moderator",
        "isActive": True,
        "loginAttempts": 0
    }
}

SECRET_KEY = "test-secret-key-for-development"

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    bio: Optional[str] = None
    location: Optional[str] = None
    role: str
    isActive: bool

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800

class AuthResponse(BaseModel):
    user: UserResponse
    tokens: TokenResponse

# Movie models
class MovieBase(BaseModel):
    title: str
    local_title: Optional[str] = None
    release_date: Optional[date] = None
    runtime: Optional[int] = None
    plot_summary: Optional[str] = None
    director: Optional[str] = None
    producer: Optional[str] = None
    production_company: Optional[str] = None
    production_state: Optional[str] = None
    box_office_ng: Optional[str] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    type: str = "movie"

class MovieCreate(MovieBase):
    genres: Optional[List[str]] = []
    languages: Optional[List[str]] = []
    cast: Optional[List[dict]] = []

class MovieResponse(MovieBase):
    id: str
    created_at: datetime
    updated_at: datetime
    genres: List[str] = []
    languages: List[str] = []
    cast: List[dict] = []

class MovieListResponse(BaseModel):
    movies: List[MovieResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

# Mock movie data
MOCK_MOVIES = {}

def create_access_token(user_data: dict):
    """Create a JWT access token"""
    payload = {
        "user_id": user_data["id"],
        "email": user_data["email"],
        "role": user_data["role"],
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
async def root():
    return {"message": "LemonNPie Backend Test Server is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "LemonNPie Backend"}

@app.get("/api/v1/test")
async def test_endpoint():
    return {"message": "API is working!", "version": "1.0.0"}

@app.post("/api/v1/auth/login", response_model=AuthResponse)
async def login(login_data: LoginRequest):
    """Authenticate user and return tokens"""
    user = MOCK_USERS.get(login_data.email)
    
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Invalid email or password"
        )
    
    if not user["isActive"]:
        raise HTTPException(
            status_code=401, 
            detail="Account is deactivated"
        )
    
    if user["password"] != login_data.password:
        # Increment login attempts (in real app, this would be persisted)
        user["loginAttempts"] += 1
        remaining_attempts = 5 - user["loginAttempts"]
        
        if remaining_attempts <= 0:
            user["isActive"] = False
            raise HTTPException(
                status_code=423, 
                detail="Account locked due to too many failed attempts"
            )
        
        raise HTTPException(
            status_code=401, 
            detail=f"Invalid email or password ({remaining_attempts} attempts remaining)"
        )
    
    # Reset login attempts on successful login
    user["loginAttempts"] = 0
    
    # Create tokens
    access_token = create_access_token(user)
    refresh_token = create_access_token(user)  # Simplified - same as access token for testing
    
    return AuthResponse(
        user=UserResponse(**user),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    )

@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user(token_data: dict = Depends(verify_token)):
    """Get current user information"""
    user = MOCK_USERS.get(token_data["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**user)

@app.post("/api/v1/auth/logout")
async def logout(token_data: dict = Depends(verify_token)):
    """Logout user (in real app, would invalidate token)"""
    return {"message": "Successfully logged out"}

# Movie endpoints
@app.get("/api/v1/movies", response_model=MovieListResponse)
async def get_movies(
    page: int = 1,
    per_page: int = 20,
    genre: Optional[str] = None,
    year: Optional[int] = None,
    director: Optional[str] = None
):
    """Get paginated list of movies"""
    movies = list(MOCK_MOVIES.values())
    
    # Apply filters
    if genre:
        movies = [m for m in movies if genre.lower() in [g.lower() for g in m.genres]]
    if year:
        movies = [m for m in movies if m.release_date and m.release_date.year == year]
    if director:
        movies = [m for m in movies if m.director and director.lower() in m.director.lower()]
    
    total = len(movies)
    total_pages = (total + per_page - 1) // per_page
    
    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated_movies = movies[start:end]
    
    return MovieListResponse(
        movies=paginated_movies,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@app.post("/api/v1/movies", response_model=MovieResponse)
async def create_movie(movie_data: MovieCreate, token_data: dict = Depends(verify_token)):
    """Create a new movie (admin only)"""
    # Check if user is admin
    user = MOCK_USERS.get(token_data["email"])
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    movie_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    movie = MovieResponse(
        id=movie_id,
        created_at=now,
        updated_at=now,
        **movie_data.dict()
    )
    
    MOCK_MOVIES[movie_id] = movie
    return movie

@app.get("/api/v1/movies/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: str):
    """Get a specific movie by ID"""
    movie = MOCK_MOVIES.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.delete("/api/v1/movies/{movie_id}")
async def delete_movie(movie_id: str, token_data: dict = Depends(verify_token)):
    """Delete a movie (admin only)"""
    # Check if user is admin
    user = MOCK_USERS.get(token_data["email"])
    if not user or user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    if movie_id not in MOCK_MOVIES:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    del MOCK_MOVIES[movie_id]
    return {"message": "Movie deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)