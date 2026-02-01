import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select
from src.models.user import User
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://neondb_owner:npg_ZGuc2zkhn5Mv@ep-ancient-rice-ahzcklrv-pooler.c-3.us-east-1.aws.neon.tech/neondb")

async def test_connection():
    """Test the database connection"""
    print(f"Testing database connection with URL: {DATABASE_URL}")

    engine = create_async_engine(DATABASE_URL)
    
    try:
        # Test basic connection by trying to count users
        async with engine.begin() as conn:
            # Create tables first to avoid relationship issues
            from sqlmodel import SQLModel
            await conn.run_sync(SQLModel.metadata.create_all)
            
            result = await conn.execute(select(User))
            users = result.fetchall()
            print(f"Connection successful! Found {len(users)} users in the database.")
            
            # Print user details if any exist
            for user in users:
                print(f"  - User ID: {user.id}, Email: {user.email}")

        print("Database connection test completed successfully!")
        return True
    except Exception as e:
        print(f"Error connecting to database: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await engine.dispose()

if __name__ == "__main__":
    print("Testing database connection...")
    asyncio.run(test_connection())