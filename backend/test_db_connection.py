"""
Simple script to test database connection
"""
import asyncio
import logging
from src.db.database import get_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_connection():
    try:
        logger.info("Testing database connection...")
        engine = get_engine()
        
        # Try to connect to the database
        async with engine.connect() as conn:
            logger.info("Connected to database successfully!")
            
            # Try a simple query
            from sqlalchemy import text
            result = await conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            logger.info(f"Query result: {row[0] if row else 'No result'}")
            
        logger.info("Database connection test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False
    finally:
        # Dispose of the engine
        engine = get_engine()
        await engine.dispose()

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    if success:
        print("\nV Database connection test passed!")
    else:
        print("\nX Database connection test failed!")