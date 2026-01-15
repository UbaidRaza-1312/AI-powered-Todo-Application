"""
Quick test to verify database configuration works with both SQLite and PostgreSQL
"""
import os
from src.db.database import DATABASE_URL, engine
import asyncio
from sqlalchemy import text

async def quick_test():
    print(f"Current DATABASE_URL: {DATABASE_URL}")
    print(f"Database type detected: {'PostgreSQL/Neon' if 'postgresql' in DATABASE_URL.lower() else 'SQLite'}")
    
    try:
        async with engine.begin() as conn:
            # Simple test query
            result = await conn.execute(text("SELECT 1"))
            print("[SUCCESS] Database connection successful!")

        # Show the actual database URL being used (without credentials for security)
        if 'postgresql' in DATABASE_URL.lower():
            # Mask the credentials for display
            import re
            masked_url = re.sub(r':\/\/.*?:.*?@', '://***:***@', DATABASE_URL)
            print(f"Using database: {masked_url}")
        else:
            print(f"Using database: {DATABASE_URL}")

    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(quick_test())