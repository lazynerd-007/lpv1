"""
Relationship models for LemonNPie Backend API
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base
from app.models.enums import VoteType, CastRole


class UserFollow(Base):
    __tablename__ = "user_follows"
    
    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    following_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")
    
    def __repr__(self):
        return f"<UserFollow(follower_id={self.follower_id}, following_id={self.following_id})>"


class UserWatchlist(Base):
    __tablename__ = "user_watchlist"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="watchlist")
    movie = relationship("Movie", back_populates="watchlist_entries")
    
    def __repr__(self):
        return f"<UserWatchlist(user_id={self.user_id}, movie_id={self.movie_id})>"


class UserFavorite(Base):
    __tablename__ = "user_favorites"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="favorites")
    movie = relationship("Movie", back_populates="favorite_entries")
    
    def __repr__(self):
        return f"<UserFavorite(user_id={self.user_id}, movie_id={self.movie_id})>"


class ReviewVote(Base):
    __tablename__ = "review_votes"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    review_id = Column(UUID(as_uuid=True), ForeignKey("reviews.id", ondelete="CASCADE"), primary_key=True)
    vote_type = Column(Enum(VoteType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="review_votes")
    review = relationship("Review", back_populates="votes")
    
    def __repr__(self):
        return f"<ReviewVote(user_id={self.user_id}, review_id={self.review_id}, vote_type={self.vote_type})>"


class MovieGenre(Base):
    __tablename__ = "movie_genres"
    
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    genre = Column(String(100), primary_key=True, nullable=False)
    
    # Relationships
    movie = relationship("Movie", back_populates="genres")
    
    def __repr__(self):
        return f"<MovieGenre(movie_id={self.movie_id}, genre={self.genre})>"


class MovieLanguage(Base):
    __tablename__ = "movie_languages"
    
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    language = Column(String(50), primary_key=True, nullable=False)
    
    # Relationships
    movie = relationship("Movie", back_populates="languages")
    
    def __repr__(self):
        return f"<MovieLanguage(movie_id={self.movie_id}, language={self.language})>"


class MovieCast(Base):
    __tablename__ = "movie_cast"
    
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    actor_name = Column(String(255), primary_key=True, nullable=False)
    character_name = Column(String(255), primary_key=True)
    role_type = Column(Enum(CastRole), default=CastRole.ACTOR, nullable=False)
    
    # Relationships
    movie = relationship("Movie", back_populates="cast")
    
    def __repr__(self):
        return f"<MovieCast(movie_id={self.movie_id}, actor_name={self.actor_name}, character_name={self.character_name})>"