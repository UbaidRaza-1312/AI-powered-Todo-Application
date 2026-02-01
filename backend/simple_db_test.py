import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
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
        # Test basic connection
        async with engine.begin() as conn:
            # Execute a simple query to test connection
            result = await conn.execute(text("SELECT version()"))
            version = result.fetchone()
            print(f"Connection successful! Database version: {version[0][:50]}...")

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