"""
Configuration settings for LemonNPie Backend API
"""
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import validator
from decouple import config


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "LemonNPie Backend API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = config("DEBUG", default=False, cast=bool)
    
    # Server settings
    HOST: str = config("HOST", default="0.0.0.0")
    PORT: int = config("PORT", default=8000, cast=int)
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = config(
        "ALLOWED_ORIGINS", 
        default="http://localhost:3000,http://localhost:5173",
        cast=lambda v: [s.strip() for s in v.split(",")]
    )
    
    # Database settings
    DATABASE_URL: str = config(
        "DATABASE_URL",
        default="postgresql+asyncpg://lemonnpie:password@localhost:5432/lemonnpie_db"
    )
    DATABASE_POOL_SIZE: int = config("DATABASE_POOL_SIZE", default=20, cast=int)
    DATABASE_MAX_OVERFLOW: int = config("DATABASE_MAX_OVERFLOW", default=30, cast=int)
    
    # Redis settings
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379/0")
    REDIS_POOL_SIZE: int = config("REDIS_POOL_SIZE", default=10, cast=int)
    
    # JWT settings
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    REFRESH_TOKEN_EXPIRE_DAYS: int = config("REFRESH_TOKEN_EXPIRE_DAYS", default=7, cast=int)
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = config("RATE_LIMIT_PER_MINUTE", default=60, cast=int)
    
    # Logging
    LOG_LEVEL: str = config("LOG_LEVEL", default="INFO")
    
    # File upload settings
    CLOUDINARY_CLOUD_NAME: Optional[str] = config("CLOUDINARY_CLOUD_NAME", default=None)
    CLOUDINARY_API_KEY: Optional[str] = config("CLOUDINARY_API_KEY", default=None)
    CLOUDINARY_API_SECRET: Optional[str] = config("CLOUDINARY_API_SECRET", default=None)
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if v == "your-secret-key-change-in-production":
            raise ValueError("Please change the SECRET_KEY in production")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()