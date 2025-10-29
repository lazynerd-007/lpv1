"""
Privacy settings schemas for LemonNPie Backend API
"""
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class PrivacySettingsBase(BaseModel):
    """Base privacy settings schema"""
    profile_visibility: Literal["public", "friends", "private"] = Field(
        default="public",
        description="Who can view the user's profile"
    )
    watchlist_visibility: Literal["public", "friends", "private"] = Field(
        default="public", 
        description="Who can view the user's watchlist"
    )
    analytics_tracking: bool = Field(
        default=True,
        description="Whether to allow analytics tracking"
    )
    personalized_recommendations: bool = Field(
        default=True,
        description="Whether to enable personalized recommendations"
    )


class PrivacySettingsUpdate(PrivacySettingsBase):
    """Schema for updating privacy settings"""
    pass


class PrivacySettingsResponse(PrivacySettingsBase):
    """Schema for privacy settings response"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PasswordChangeRequest(BaseModel):
    """Schema for password change request"""
    current_password: str = Field(..., min_length=1, description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")
    confirm_password: str = Field(..., min_length=8, description="Confirm new password")
    
    def validate_passwords_match(self):
        """Validate that new password and confirm password match"""
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirm password do not match")
        return self


class PasswordChangeResponse(BaseModel):
    """Schema for password change response"""
    message: str
    success: bool


class TwoFactorAuthStatus(BaseModel):
    """Schema for 2FA status response"""
    enabled: bool
    backup_codes_count: int = 0


class TwoFactorAuthSetupRequest(BaseModel):
    """Schema for 2FA setup request"""
    password: str = Field(..., description="Current password for verification")


class TwoFactorAuthSetupResponse(BaseModel):
    """Schema for 2FA setup response"""
    qr_code_url: str
    secret_key: str
    backup_codes: list[str]


class TwoFactorAuthVerifyRequest(BaseModel):
    """Schema for 2FA verification request"""
    code: str = Field(..., min_length=6, max_length=6, description="6-digit verification code")


class TwoFactorAuthToggleRequest(BaseModel):
    """Schema for enabling/disabling 2FA"""
    password: str = Field(..., description="Current password for verification")
    code: str = Field(..., min_length=6, max_length=6, description="6-digit verification code")
    enabled: bool = Field(..., description="Whether to enable or disable 2FA")