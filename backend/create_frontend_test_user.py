#!/usr/bin/env python3
"""
Create test user with credentials that match frontend quick login buttons
"""
import asyncio
from sqlalchemy import select
from app.db.database import init_db, get_db
from app.models.user import User, UserRole
from app.auth.jwt_service import jwt_service

async def create_frontend_test_users():
    """Create test users that match frontend quick login buttons"""
    print("Creating frontend test users...")
    
    # Initialize database
    await init_db()
    
    # Test users that match frontend quick login buttons
    test_users = [
        {
            "email": "user@test.com",
            "password": "password123",
            "name": "Test User",
            "bio": "Regular test user for authentication testing",
            "location": "Test City",
            "role": UserRole.USER
        },
        {
            "email": "admin@admin.com", 
            "password": "admin123",
            "name": "Admin User",
            "bio": "Administrator test user",
            "location": "Admin City",
            "role": UserRole.ADMIN
        },
        {
            "email": "critic@test.com",
            "password": "critic123", 
            "name": "Critic User",
            "bio": "Film critic test user",
            "location": "Critic City",
            "role": UserRole.CRITIC
        }
    ]
    
    async for session in get_db():
        try:
            for user_data in test_users:
                # Check if user already exists
                result = await session.execute(select(User).where(User.email == user_data["email"]))
                existing_user = result.scalar_one_or_none()
                
                if existing_user:
                    print(f"✅ User {user_data['email']} already exists")
                    print(f"   ID: {existing_user.id}, Name: {existing_user.name}, Role: {existing_user.role}")
                    continue
                
                # Create the test user
                password_hash = jwt_service.hash_password(user_data["password"])
                
                test_user = User(
                    email=user_data["email"],
                    password_hash=password_hash,
                    name=user_data["name"],
                    bio=user_data["bio"],
                    location=user_data["location"],
                    role=user_data["role"],
                    is_active=True,
                    is_verified=True
                )
                
                session.add(test_user)
                await session.commit()
                await session.refresh(test_user)
                
                print(f"✅ Created user: {test_user.email}")
                print(f"   ID: {test_user.id}")
                print(f"   Name: {test_user.name}")
                print(f"   Role: {test_user.role}")
                print(f"   Password: {user_data['password']}")
                print()
                
        except Exception as e:
            print(f"❌ Error creating test users: {e}")
            await session.rollback()
        finally:
            break

if __name__ == "__main__":
    asyncio.run(create_frontend_test_users())