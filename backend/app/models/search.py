"""
Search index models for LemonNPie Backend API
"""
from sqlalchemy import Column, DateTime, ForeignKey, text, Text
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class MovieSearchIndex(Base):
    __tablename__ = "movie_search_index"
    
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    # Use Text for SQLite compatibility, TSVECTOR for PostgreSQL in production
    search_vector = Column(Text)
    title_vector = Column(Text)
    content_vector = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    movie = relationship("Movie", back_populates="search_index")
    
    def __repr__(self):
        return f"<MovieSearchIndex(movie_id={self.movie_id})>"