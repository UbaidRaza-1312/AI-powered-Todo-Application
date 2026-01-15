"""
Migration script to create tables in Neon DB
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from src.models.user import User
from src.models.task import Task

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://your_username:your_password@ep-xxx.us-east-1.aws.neon.tech/your_database_name?sslmode=require")

async def create_tables():
    """Create all tables in Neon DB"""
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={
            "server_settings": {
                "application_name": "todo-app",
            },
        }
    )
    
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(SQLModel.metadata.create_all)
        print("Tables created successfully in Neon DB!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())