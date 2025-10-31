#!/usr/bin/env python3
"""
Debug JWT token to see what's inside
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jose import jwt
from app.core.config import settings

# The token we generated
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlNTQxNGQzNi1jNDVhLTQ4NjMtYTFmNS1iYmIxNDg5MWFiYWYiLCJlbWFpbCI6ImFkbWluQGFkbWluLmNvbSIsInJvbGUiOiJBRE1JTiIsImV4cCI6MTc2MTk3MTA3NX0.T6k_I8avu6b6RDAGpWwL4qx6YWGk6nlMrAqKtdAPxqA"

try:
    # Decode the token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print("Token payload:")
    for key, value in payload.items():
        print(f"  {key}: {value}")
    
    print(f"\nUser ID: {payload.get('sub')}")
    print(f"Email: {payload.get('email')}")
    print(f"Role: {payload.get('role')}")
    print(f"Expiration: {payload.get('exp')}")
    
except Exception as e:
    print(f"Error decoding token: {e}")