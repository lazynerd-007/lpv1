#!/usr/bin/env python3
"""
Create admin test user for admin dashboard testing
"""
import asyncio
import time
from sqlalchemy import select
from app.db.database import init_db, get_db
from app.models.user import User, UserRole
from app.auth.jwt_service import jwt_service

async def create_admin_user():
    """Create an admin test user for testing"""
    print("Creating admin test user...")
    
    # Initialize database
    await init_db()
    
    async for session in get_db():
        try:
            # Create unique email with timestamp
            timestamp = int(time.time())
            email = f"admin.test.{timestamp}@example.com"
            
            # Check if user already exists (shouldn't with timestamp)
            result = await session.execute(select(User).where(User.email == email))
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"✅ Admin user {email} already exists")
                print(f"User ID: {existing_user.id}")
                print(f"User Name: {existing_user.name}")
                print(f"User Role: {existing_user.role}")
                print(f"Is Active: {existing_user.is_active}")
                return existing_user
            
            # Create the admin test user
            password_hash = jwt_service.hash_password("AdminPassword123!")
            
            admin_user = User(
                email=email,
                password_hash=password_hash,
                name="Admin Test User",
                bio="Admin test user for dashboard testing",
                location="Admin City",
                role=UserRole.ADMIN,  # Set as ADMIN
                is_active=True,
                is_verified=True
            )
            
            session.add(admin_user)
            await session.commit()
            await session.refresh(admin_user)
            
            print(f"✅ Created admin test user: {admin_user.email}")
            print(f"User ID: {admin_user.id}")
            print(f"User Name: {admin_user.name}")
            print(f"User Role: {admin_user.role}")
            print(f"Is Active: {admin_user.is_active}")
            print(f"Is Verified: {admin_user.is_verified}")
            print(f"Password: AdminPassword123!")
            
            return admin_user
            
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            await session.rollback()
            raise
        finally:
            break

if __name__ == "__main__":
    asyncio.run(create_admin_user())