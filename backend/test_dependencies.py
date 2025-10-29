#!/usr/bin/env python3
"""
Test script to check dependencies
"""

def test_dependencies():
    """Test if dependencies can be imported and work"""
    
    print("🔍 Testing dependencies...")
    
    try:
        from app.auth.dependencies import get_current_user, get_optional_current_user
        print("✅ Auth dependencies imported successfully")
    except Exception as e:
        print(f"❌ Error importing auth dependencies: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        from app.db.database import get_db
        print("✅ Database dependency imported successfully")
    except Exception as e:
        print(f"❌ Error importing database dependency: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        from app.services.user_service import user_service
        print("✅ User service imported successfully")
        
        # Check if the new methods exist
        methods = ['get_privacy_settings', 'update_privacy_settings', 'change_password', 
                  'get_2fa_status', 'setup_2fa', 'verify_2fa_setup', 'toggle_2fa']
        
        for method in methods:
            if hasattr(user_service, method):
                print(f"  ✅ {method} exists")
            else:
                print(f"  ❌ {method} missing")
                
    except Exception as e:
        print(f"❌ Error importing user service: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        from app.schemas.privacy import (
            PrivacySettingsUpdate,
            PrivacySettingsResponse,
            PasswordChangeRequest,
            PasswordChangeResponse,
            TwoFactorAuthStatus,
            TwoFactorAuthSetupRequest,
            TwoFactorAuthSetupResponse,
            TwoFactorAuthVerifyRequest,
            TwoFactorAuthToggleRequest
        )
        print("✅ Privacy schemas imported successfully")
    except Exception as e:
        print(f"❌ Error importing privacy schemas: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        from app.models.user import User
        print("✅ User model imported successfully")
    except Exception as e:
        print(f"❌ Error importing User model: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n🎉 All dependencies imported successfully!")

if __name__ == "__main__":
    test_dependencies()