import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Testing database connection to: {DATABASE_URL}")

async def test_connection():
    try:
        # Create engine
        engine = create_async_engine(DATABASE_URL)

        # Try to connect
        async with engine.begin() as conn:
            print("Connected to database successfully!")

            # Test by executing a simple query using text()
            result = await conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"Database version: {version}")

        print("Connection test completed successfully!")

    except Exception as e:
        print(f"Error connecting to database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())