#!/usr/bin/env python3
"""Update database schema"""

import os
from app import create_app, db
from app.models import User, Rant, GeneratedContent

def update_database():
    """Update database schema"""
    app = create_app()
    with app.app_context():
        try:
            # Drop and recreate tables
            print("Dropping existing tables...")
            db.drop_all()
            
            print("Creating new tables...")
            db.create_all()
            
            print("Database schema updated successfully!")
            
            # Check if tables exist
            tables = db.engine.table_names()
            print(f"Available tables: {tables}")
            
        except Exception as e:
            print(f"Error updating database: {e}")
            
if __name__ == '__main__':
    update_database()
