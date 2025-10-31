#!/usr/bin/env python3
"""
Check what users exist in the database
"""
import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.models.user import User
from app.core.config import settings

async def check_users():
    """Check what users exist in the database"""
    try:
        # Create database connection
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=False
        )
        
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with async_session() as session:
            # Get all users
            result = await session.execute(select(User))
            users = result.scalars().all()
            
            print(f"Found {len(users)} users:")
            for user in users:
                print(f"- ID: {user.id}")
                print(f"  Email: {user.email}")
                print(f"  Name: {user.name}")
                print(f"  Role: {user.role}")
                print(f"  Active: {user.is_active}")
                print()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_users())