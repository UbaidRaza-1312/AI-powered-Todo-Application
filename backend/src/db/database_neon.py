from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import os
from contextlib import asynccontextmanager
import logging

# Get database URL from environment - defaults to Neon DB connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://neondb_owner:npg_ZGuc2zkhn5Mv@ep-ancient-rice-ahzcklrv-pooler.c-3.us-east-1.aws.neon.tech/neondb")

# For PostgreSQL/Neon DB
try:
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,  # Set to False in production
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,    # Recycle connections every 5 minutes
        # Correct way to pass asyncpg-specific parameters
        connect_args={
            "server_settings": {
                "application_name": "todo-app",
            },
        }
    )
    logging.info("Successfully connected to Neon DB")
except Exception as e:
    logging.error(f"Failed to connect to Neon DB: {e}")
    raise

# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

async def create_db_and_tables():
    """Create database tables"""
    try:
        from ..models.user import User  # noqa: F401
        from ..models.task import Task  # noqa: F401

        async with engine.begin() as conn:
            # Create tables
            await conn.run_sync(SQLModel.metadata.create_all)
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
        raise

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logging.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()