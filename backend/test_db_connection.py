"""
Test script to verify Neon DB connection when configured
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select
from src.models.user import User
from src.db.database import DATABASE_URL, engine
from contextlib import asynccontextmanager

async def test_connection():
    """Test the database connection"""
    print(f"Testing database connection with URL: {DATABASE_URL}")
    
    try:
        # Test basic connection by trying to count users
        async with engine.begin() as conn:
            result = await conn.execute(select(User))
            users = result.fetchall()
            print(f"Connection successful! Found {len(users)} users in the database.")
        
        print("Database connection test completed successfully!")
        return True
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    asyncio.run(test_connection())