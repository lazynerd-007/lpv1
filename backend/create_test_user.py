#!/usr/bin/env python3
"""
Create test user for login testing
"""
import asyncio
from sqlalchemy import select
from app.db.database import init_db, get_db
from app.models.user import User, UserRole
from app.auth.jwt_service import jwt_service

async def create_test_user():
    """Create the test user for login testing"""
    print("Creating test user...")
    
    # Initialize database
    await init_db()
    
    async for session in get_db():
        try:
            # Check if user already exists
            email = "john.doe.test.1737998968@example.com"
            result = await session.execute(select(User).where(User.email == email))
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"✅ User {email} already exists")
                print(f"User ID: {existing_user.id}")
                print(f"User Name: {existing_user.name}")
                print(f"User Role: {existing_user.role}")
                print(f"Is Active: {existing_user.is_active}")
                return
            
            # Create the test user
            password_hash = jwt_service.hash_password("TestPassword123!")
            
            test_user = User(
                email=email,
                password_hash=password_hash,
                name="John Doe Test",
                bio="Test user for authentication testing",
                location="Test City",
                role=UserRole.USER,
                is_active=True,
                is_verified=True  # Make sure user is verified
            )
            
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)
            
            print(f"✅ Created test user: {test_user.email}")
            print(f"User ID: {test_user.id}")
            print(f"User Name: {test_user.name}")
            print(f"User Role: {test_user.role}")
            print(f"Is Active: {test_user.is_active}")
            print(f"Is Verified: {test_user.is_verified}")
            
        except Exception as e:
            print(f"❌ Error creating test user: {e}")
            await session.rollback()
            raise
        finally:
            break

if __name__ == "__main__":
    asyncio.run(create_test_user())