"""
Privacy settings model for LemonNPie Backend API
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.database import Base


class UserPrivacySettings(Base):
    __tablename__ = "user_privacy_settings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # Profile visibility settings
    profile_visibility = Column(String(20), default="public", nullable=False)  # public, friends, private
    watchlist_visibility = Column(String(20), default="public", nullable=False)  # public, friends, private
    
    # Data and analytics settings
    analytics_tracking = Column(Boolean, default=True, nullable=False)
    personalized_recommendations = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="privacy_settings")
    
    def __repr__(self):
        return f"<UserPrivacySettings(user_id={self.user_id}, profile_visibility={self.profile_visibility})>"