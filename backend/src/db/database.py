from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
import os
import logging

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Global variables - will be initialized when needed
_engine = None
_AsyncSessionLocal = None

def get_engine():
    """Get the database engine, initializing it if necessary"""
    global _engine
    if _engine is None:
        # Get database URL from environment - defaults to local SQLite for development
        DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://neondb_owner:npg_ZGuc2zkhn5Mv@ep-ancient-rice-ahzcklrv-pooler.c-3.us-east-1.aws.neon.tech/neondb")
        
        # Determine database type and configure accordingly
        if "postgresql" in DATABASE_URL.lower():
            # PostgreSQL/Neon DB configuration
            try:
                from sqlalchemy.orm import sessionmaker
                _engine = create_async_engine(
                    DATABASE_URL,
                    echo=True,  # Set to False in production
                    pool_size=5,
                    max_overflow=10,
                    pool_pre_ping=True,  # Verify connections before use
                    pool_recycle=300,    # Recycle connections every 5 minutes
                    connect_args={
                        "server_settings": {
                            "application_name": "todo-app",
                        },
                    }
                )
                logging.info("Successfully connected to PostgreSQL/Neon DB")
            except Exception as e:
                logging.error(f"Failed to connect to PostgreSQL/Neon DB: {e}")
                raise
        elif "sqlite" in DATABASE_URL.lower():
            # SQLite configuration for local development
            try:
                from sqlalchemy.orm import sessionmaker
                _engine = create_async_engine(
                    DATABASE_URL,
                    echo=True,
                    connect_args={"check_same_thread": False}
                )
                logging.info("Successfully connected to SQLite DB")
            except Exception as e:
                logging.error(f"Failed to connect to SQLite DB: {e}")
                raise
        else:
            raise ValueError(f"Unsupported database type in DATABASE_URL: {DATABASE_URL}")
    
    return _engine

def get_session_maker():
    """Get the session maker, initializing it if necessary"""
    global _AsyncSessionLocal
    if _AsyncSessionLocal is None:
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.ext.asyncio import AsyncSession
        
        engine = get_engine()
        _AsyncSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            class_=AsyncSession
        )
    return _AsyncSessionLocal

async def create_db_and_tables():
    """Create database tables"""
    try:
        from ..models.user import User  # noqa: F401
        from ..models.task import Task  # noqa: F401

        engine = get_engine()

        # Try to connect and create tables
        async with engine.begin() as conn:
            # Create tables
            await conn.run_sync(SQLModel.metadata.create_all)

        # Commit and close the connection properly
        await engine.dispose()

        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
        raise

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    session_maker = get_session_maker()
    async with session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logging.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()