"""
Notification schemas for LemonNPie Backend API
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import NotificationType


class NotificationBase(BaseModel):
    type: NotificationType
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=1000)
    data: Optional[Dict[str, Any]] = None


class NotificationCreate(NotificationBase):
    user_id: UUID
    expires_at: Optional[datetime] = None


class NotificationBulkCreate(BaseModel):
    user_ids: List[UUID]
    type: NotificationType
    title: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=1, max_length=1000)
    data: Optional[Dict[str, Any]] = None
    expires_at: Optional[datetime] = None


class NotificationResponse(NotificationBase):
    id: UUID
    user_id: UUID
    is_read: bool
    read_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None


class NotificationPreferenceBase(BaseModel):
    notification_type: NotificationType
    email_enabled: bool = True
    push_enabled: bool = True
    in_app_enabled: bool = True


class NotificationPreferenceCreate(NotificationPreferenceBase):
    user_id: UUID


class NotificationPreferenceUpdate(BaseModel):
    email_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None
    in_app_enabled: Optional[bool] = None


class NotificationPreferenceResponse(NotificationPreferenceBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationStats(BaseModel):
    total_notifications: int
    unread_count: int
    read_count: int


class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]
    total: int
    unread_count: int
    has_more: bool