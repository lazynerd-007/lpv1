#!/usr/bin/env python3
"""
Test script to debug admin dashboard endpoint
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
from app.services.admin_service import AdminService
from app.core.config import settings

async def test_admin_dashboard():
    """Test the admin dashboard service directly"""
    try:
        # Create database connection
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True
        )
        
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        async with async_session() as session:
            admin_service = AdminService(session)
            
            print("Testing system metrics...")
            system_metrics = await admin_service.get_system_metrics()
            print(f"System metrics: {system_metrics}")
            
            print("\nTesting user analytics...")
            user_analytics = await admin_service.get_user_analytics()
            print(f"User analytics: {user_analytics}")
            
            print("\nTesting content analytics...")
            content_analytics = await admin_service.get_content_analytics()
            print(f"Content analytics: {content_analytics}")
            
            print("\nTesting full dashboard...")
            dashboard = await admin_service.get_admin_dashboard()
            print(f"Dashboard: {dashboard}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_admin_dashboard())