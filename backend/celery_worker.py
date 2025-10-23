#!/usr/bin/env python3
"""
Celery worker for LemonNPie Backend API
"""
import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.celery_app import celery_app

if __name__ == "__main__":
    celery_app.start()