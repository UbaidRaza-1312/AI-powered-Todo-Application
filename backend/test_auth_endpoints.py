"""
Test script to verify authentication endpoints work properly
"""
import asyncio
import os
from sqlmodel.ext.asyncio.session import AsyncSession
from dotenv import load_dotenv
from src.services.auth_service import AuthService
from src.models.user import User, UserBase
from src.utils.auth import get_password_hash
from src.api.auth_routes import UserCreate, UserLogin
from uuid import UUID

# Load environment variables
load_dotenv()

async def test_auth_endpoints():
    """Test the authentication endpoints"""
    print("Testing authentication endpoints...")
    
    # Import the database engine
    from src.db.database import get_engine, get_session_maker
    from sqlmodel import SQLModel
    
    # Create engine and tables
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    # Create a session
    session_maker = get_session_maker()
    async with session_maker() as session:
        # Create auth service
        auth_service = AuthService(session)
        
        # Clean up any existing test user
        from sqlmodel import select
        existing_user = await auth_service.get_user_by_email("testuser@example.com")
        if existing_user:
            print("Removing existing test user...")
            await session.delete(existing_user)
            await session.commit()
        
        # Test user registration
        print("\n1. Testing user registration...")
        user_data = UserBase(
            email="testuser@example.com",
            first_name="Test",
            last_name="User"
        )
        new_user = await auth_service.create_user(user_data, "securepassword123")
        await session.commit()
        await session.refresh(new_user)
        
        print(f"SUCCESS: User registered successfully: {new_user.email}")

        # Test user login
        print("\n2. Testing user login...")
        authenticated_user = await auth_service.authenticate_user("testuser@example.com", "securepassword123")

        if authenticated_user:
            print(f"SUCCESS: User logged in successfully: {authenticated_user.email}")

            # Test token creation
            print("\n3. Testing token creation...")
            token = await auth_service.create_access_token_for_user(authenticated_user)
            print(f"SUCCESS: Access token created: {token[:30]}...")
        else:
            print("ERROR: Login failed!")
            return False

        # Test login with wrong password
        print("\n4. Testing failed login with wrong password...")
        failed_login = await auth_service.authenticate_user("testuser@example.com", "wrongpassword")

        if not failed_login:
            print("SUCCESS: Correctly failed login with wrong password")
        else:
            print("ERROR: Should have failed with wrong password")
            return False

        # Test getting user by ID
        print("\n5. Testing get user by ID...")
        retrieved_user = await auth_service.get_user_by_id(new_user.id)
        if retrieved_user and retrieved_user.email == "testuser@example.com":
            print(f"SUCCESS: Retrieved user by ID successfully: {retrieved_user.email}")
        else:
            print("ERROR: Failed to retrieve user by ID")
            return False

        print("\nSUCCESS: All authentication tests passed!")
        return True

if __name__ == "__main__":
    success = asyncio.run(test_auth_endpoints())
    if success:
        print("\nV All authentication endpoint tests completed successfully!")
    else:
        print("\nX Some authentication tests failed!")