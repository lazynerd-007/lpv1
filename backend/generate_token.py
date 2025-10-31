"""
Generate a JWT token for testing admin dashboard access
"""
import jwt
from datetime import datetime, timedelta
import uuid

# JWT settings (matching the app settings)
SECRET_KEY = "local-development-secret-key-for-testing-only-123456789"
ALGORITHM = "HS256"

# Create token payload
payload = {
    "sub": "e5414d36-c45a-4863-a1f5-bbb14891abaf",  # admin user ID from database
    "email": "admin@admin.com",
    "role": "ADMIN",
    "exp": datetime.utcnow() + timedelta(hours=24)  # 24 hours from now
}

# Generate token
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print(f"Generated JWT token:")
print(token)
print(f"\nToken expires at: {datetime.fromtimestamp(payload['exp'].timestamp())}")