"""
Test script to verify Neon DB connection
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select
from src.models.user import User
from src.db.database import get_async_session
from contextlib import asynccontextmanager

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://neondb_owner:npg_ZGuc2zkhn5Mv@ep-ancient-rice-ahzcklrv-pooler.c-3.us-east-1.aws.neon.tech/neondb")

async def test_connection():
    """Test the Neon DB connection"""
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={
            "server_settings": {
                "application_name": "todo-app-test",
            },
        }
    )
    
    try:
        # Test basic connection by trying to count users
        async with engine.begin() as conn:
            result = await conn.execute(select(User))
            users = result.fetchall()
            print(f"Connection successful! Found {len(users)} users in the database.")
        
        print("Neon DB connection test completed successfully!")
        return True
    except Exception as e:
        print(f"Error connecting to Neon DB: {e}")
        return False
    finally:
        await engine.dispose()

if __name__ == "__main__":
    print("Testing Neon DB connection...")
    asyncio.run(test_connection())