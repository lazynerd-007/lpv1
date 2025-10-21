"""
Movie model for LemonNPie Backend API
"""
from sqlalchemy import Column, String, Date, Integer, Text, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base
from app.models.enums import ContentType


class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False, index=True)
    local_title = Column(String(500))
    release_date = Column(Date, nullable=False, index=True)
    runtime = Column(Integer)
    plot_summary = Column(Text)
    poster_url = Column(String(500))
    trailer_url = Column(String(500))
    director = Column(String(255), index=True)
    producer = Column(String(255))
    production_company = Column(String(255))
    production_state = Column(String(100))
    box_office_ng = Column(String(100))
    type = Column(Enum(ContentType), default=ContentType.MOVIE, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")
    genres = relationship("MovieGenre", back_populates="movie", cascade="all, delete-orphan")
    languages = relationship("MovieLanguage", back_populates="movie", cascade="all, delete-orphan")
    cast = relationship("MovieCast", back_populates="movie", cascade="all, delete-orphan")
    watchlist_entries = relationship("UserWatchlist", back_populates="movie", cascade="all, delete-orphan")
    favorite_entries = relationship("UserFavorite", back_populates="movie", cascade="all, delete-orphan")
    search_index = relationship("MovieSearchIndex", back_populates="movie", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Movie(id={self.id}, title={self.title}, type={self.type})>"