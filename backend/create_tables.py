import asyncio
from src.db.database import create_db_and_tables

async def create_tables():
    print("Creating database tables...")
    try:
        await create_db_and_tables()
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(create_tables())