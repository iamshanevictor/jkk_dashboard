#!/usr/bin/env python3
"""
Database initialization script for Render deployment
"""
import os
import sys

def init_database():
    """Initialize the database with proper schema"""
    try:
        print("Starting database initialization...")
        
        # Import Flask app and database
        from app import create_app
        from app.models import db
        
        # Create app with production config
        app = create_app('production')
        
        with app.app_context():
            print("Dropping existing tables...")
            db.drop_all()
            
            print("Creating new tables...")
            db.create_all()
            
            print("Database initialization completed successfully!")
            return True
            
    except Exception as e:
        print(f"ERROR: Database initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    if not success:
        sys.exit(1)
    print("Database is ready!")
