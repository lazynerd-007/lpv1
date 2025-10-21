"""
Review model for LemonNPie Backend API
"""
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey, Enum, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base
from app.models.enums import ModerationStatus


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    lemon_pie_rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=False)
    review_language = Column(String(10), default="en", nullable=False)
    spoiler_warning = Column(Boolean, default=False, nullable=False)
    cultural_authenticity_rating = Column(Integer)
    production_quality_rating = Column(Integer)
    story_rating = Column(Integer)
    acting_rating = Column(Integer)
    cinematography_rating = Column(Integer)
    helpful_votes = Column(Integer, default=0, nullable=False)
    unhelpful_votes = Column(Integer, default=0, nullable=False)
    is_flagged = Column(Boolean, default=False, nullable=False)
    moderation_status = Column(Enum(ModerationStatus), default=ModerationStatus.APPROVED, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")
    votes = relationship("ReviewVote", back_populates="review", cascade="all, delete-orphan")
    reports = relationship("UserReport", back_populates="reported_review", cascade="all, delete-orphan")
    
    # Add constraints
    __table_args__ = (
        CheckConstraint('lemon_pie_rating >= 1 AND lemon_pie_rating <= 10', name='check_lemon_pie_rating'),
        CheckConstraint('cultural_authenticity_rating >= 1 AND cultural_authenticity_rating <= 10', name='check_cultural_authenticity_rating'),
        CheckConstraint('production_quality_rating >= 1 AND production_quality_rating <= 10', name='check_production_quality_rating'),
        CheckConstraint('story_rating >= 1 AND story_rating <= 10', name='check_story_rating'),
        CheckConstraint('acting_rating >= 1 AND acting_rating <= 10', name='check_acting_rating'),
        CheckConstraint('cinematography_rating >= 1 AND cinematography_rating <= 10', name='check_cinematography_rating'),
        UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_review'),
    )
    
    def __repr__(self):
        return f"<Review(id={self.id}, user_id={self.user_id}, movie_id={self.movie_id}, rating={self.lemon_pie_rating})>"