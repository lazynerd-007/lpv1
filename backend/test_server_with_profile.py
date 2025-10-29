"""
Test server with profile update endpoint for testing frontend functionality
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
import uvicorn
import jwt
import json
import os

app = FastAPI(title="Test Server with Profile Update")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Mock JWT secret (for testing only)
JWT_SECRET = "test-secret-key"

# Mock user data storage (in-memory for testing)
mock_users = {
    "test@example.com": {
        "id": 1,
        "email": "test@example.com",
        "name": "Test User",
        "avatar": None,
        "bio": "Test bio",
        "location": "Test City",
        "is_active": True
    },
    "user@test.com": {
        "id": 2,
        "email": "user@test.com",
        "name": "Demo User",
        "avatar": None,
        "bio": "Demo user for testing",
        "location": "Lagos, Nigeria",
        "is_active": True
    }
}

# Mock notification preferences data (in-memory for testing)
mock_notification_preferences = {
    "new-reviews": {
        "id": "new-reviews",
        "name": "New Reviews",
        "description": "Get notified when someone reviews a movie you've watched",
        "enabled": True
    },
    "watchlist-updates": {
        "id": "watchlist-updates", 
        "name": "Watchlist Updates",
        "description": "Notifications about new releases in your watchlist",
        "enabled": True
    },
    "recommendations": {
        "id": "recommendations",
        "name": "Recommendations", 
        "description": "Weekly personalized movie recommendations",
        "enabled": False
    },
    "newsletter": {
        "id": "newsletter",
        "name": "Newsletter",
        "description": "Monthly newsletter with movie news and updates", 
        "enabled": True
    }
}

# Pydantic models
class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar: Optional[str] = None

class UserProfileResponse(BaseModel):
    id: int
    email: str
    name: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    is_active: bool

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserProfileResponse

class NotificationPreferenceUpdate(BaseModel):
    enabled: bool

class NotificationPreference(BaseModel):
    id: str
    name: str
    description: str
    enabled: bool

# Helper functions
def create_access_token(email: str) -> str:
    """Create a simple JWT token for testing"""
    payload = {"sub": email, "type": "access"}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify JWT token and return user email"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(email: str = Depends(verify_token)) -> dict:
    """Get current user from mock data"""
    user = mock_users.get(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Routes
@app.get("/")
async def root():
    return {"message": "Test Server with Profile Update - Running"}

@app.post("/api/v1/auth/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """Mock login endpoint"""
    # For testing, accept any email/password combination
    email = login_data.email
    
    # Create or get user
    if email not in mock_users:
        mock_users[email] = {
            "id": len(mock_users) + 1,
            "email": email,
            "name": email.split("@")[0].title(),
            "avatar": None,
            "bio": "Default bio",
            "location": "Default City",
            "is_active": True
        }
    
    user = mock_users[email]
    access_token = create_access_token(email)
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserProfileResponse(**user)
    )

@app.get("/api/v1/auth/me", response_model=UserProfileResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    return UserProfileResponse(**current_user)

@app.put("/api/v1/users/profile", response_model=UserProfileResponse)
async def update_current_user_profile(
    profile_update: UserProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update current user profile"""
    email = current_user["email"]
    
    # Update user data
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            mock_users[email][field] = value
    
    print(f"Profile updated for {email}: {update_data}")
    
    return UserProfileResponse(**mock_users[email])

@app.post("/api/v1/auth/logout")
async def logout():
    """Mock logout endpoint"""
    return {"message": "Successfully logged out"}

@app.get("/api/v1/notifications/preferences")
async def get_notification_preferences(current_user: dict = Depends(get_current_user)):
    """Get all notification preferences"""
    return list(mock_notification_preferences.values())

@app.patch("/api/v1/notifications/preferences/{notification_type}")
async def update_notification_preference(
    notification_type: str,
    preference_update: NotificationPreferenceUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a specific notification preference"""
    if notification_type not in mock_notification_preferences:
        raise HTTPException(status_code=404, detail="Notification preference not found")
    
    # Update the preference
    mock_notification_preferences[notification_type]["enabled"] = preference_update.enabled
    
    print(f"Notification preference updated for {current_user['email']}: {notification_type} = {preference_update.enabled}")
    
    return NotificationPreference(**mock_notification_preferences[notification_type])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)