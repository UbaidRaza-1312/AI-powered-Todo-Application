import asyncio
import os
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
from src.services.auth_service import AuthService
from src.models.user import User
from src.utils.auth import get_password_hash

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://neondb_owner:npg_ZGuc2zkhn5Mv@ep-ancient-rice-ahzcklrv-pooler.c-3.us-east-1.aws.neon.tech/neondb")

async def test_authentication():
    """Test the authentication process"""
    print("Testing authentication process...")
    
    # Create engine
    engine = create_async_engine(DATABASE_URL)
    
    try:
        # Create tables first
        from sqlmodel import SQLModel
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        
        # Create a session
        async with AsyncSession(engine) as session:
            # Create auth service
            auth_service = AuthService(session)
            
            # Check if there are any existing users
            result = await session.execute(text("SELECT COUNT(*) FROM user"))
            user_count = result.scalar()
            print(f"Current user count: {user_count}")
            
            # If no users exist, create a test user
            if user_count == 0:
                print("Creating a test user...")
                from src.models.user import UserBase
                user_data = UserBase(email="test@example.com", first_name="Test", last_name="User")
                hashed_password = get_password_hash("password123")
                
                # Create user directly in DB
                test_user = User(
                    email="test@example.com",
                    first_name="Test", 
                    last_name="User",
                    hashed_password=hashed_password
                )
                session.add(test_user)
                await session.commit()
                await session.refresh(test_user)
                print(f"Created test user with ID: {test_user.id}")
            
            # Now try to authenticate with the test user
            print("Attempting to authenticate user...")
            authenticated_user = await auth_service.authenticate_user("test@example.com", "password123")
            
            if authenticated_user:
                print(f"Authentication successful! User ID: {authenticated_user.id}")
                print(f"User email: {authenticated_user.email}")
            else:
                print("Authentication failed!")
                
            # Try with wrong password
            print("Attempting to authenticate with wrong password...")
            failed_auth = await auth_service.authenticate_user("test@example.com", "wrongpassword")
            if not failed_auth:
                print("Correctly failed authentication with wrong password")
            else:
                print("ERROR: Authentication should have failed with wrong password")
                
    except Exception as e:
        print(f"Error during authentication test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_authentication())