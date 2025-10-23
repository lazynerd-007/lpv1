"""
JWT Authentication Service for LemonNPie Backend API
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID
import uuid

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.core.config import settings
from app.models.enums import UserRole


class JWTService:
    """Service for handling JWT token operations"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        # Bcrypt has a 72-byte limit, so we truncate if necessary
        if len(password.encode('utf-8')) > 72:
            password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        # Bcrypt has a 72-byte limit, so we truncate if necessary
        if len(plain_password.encode('utf-8')) > 72:
            plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(
        self, 
        user_id: UUID, 
        email: str, 
        role: UserRole,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        # Generate unique token ID for tracking
        token_id = str(uuid.uuid4())
        
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "role": role.value,
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": token_id,
            "type": "access"
        }
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(
        self, 
        user_id: UUID, 
        email: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT refresh token"""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        # Generate unique token ID for tracking
        token_id = str(uuid.uuid4())
        
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": token_id,
            "type": "refresh"
        }
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
    
    def get_user_id_from_token(self, token: str) -> UUID:
        """Extract user ID from JWT token"""
        payload = self.verify_token(token)
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        try:
            return UUID(user_id_str)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
    
    def get_user_role_from_token(self, token: str) -> UserRole:
        """Extract user role from JWT token"""
        payload = self.verify_token(token)
        role_str = payload.get("role")
        if role_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        try:
            return UserRole(role_str)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid role in token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
    
    def is_token_expired(self, token: str) -> bool:
        """Check if a token is expired"""
        try:
            payload = self.verify_token(token)
            exp = payload.get("exp")
            if exp is None:
                return True
            
            return datetime.utcnow() > datetime.fromtimestamp(exp)
        except HTTPException:
            return True
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """Create a new access token using a refresh token"""
        payload = self.verify_token(refresh_token)
        
        # Verify this is a refresh token
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id_str = payload.get("sub")
        email = payload.get("email")
        
        if not user_id_str or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Note: In a real implementation, you would fetch the user from the database
        # to get the current role and verify the user is still active
        # For now, we'll assume the role hasn't changed
        user_id = UUID(user_id_str)
        
        # Create new access token (role would be fetched from database in real implementation)
        return self.create_access_token(user_id, email, UserRole.USER)


# Global instance
jwt_service = JWTService()