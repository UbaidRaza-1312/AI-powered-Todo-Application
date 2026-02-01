import asyncio
import os
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
from src.services.auth_service import AuthService
from src.models.user import User
from src.utils.auth import get_password_hash, verify_password

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://neondb_owner:npg_ZGuc2zkhn5Mv@ep-ancient-rice-ahzcklrv-pooler.c-3.us-east-1.aws.neon.tech/neondb")

async def test_password_verification():
    """Test the password verification process"""
    print("Testing password verification process...")
    
    # Create engine
    engine = create_async_engine(DATABASE_URL)
    
    try:
        # Create a session
        async with AsyncSession(engine) as session:
            # Create auth service
            auth_service = AuthService(session)
            
            # Test password hashing and verification directly
            test_password = "password123"
            wrong_password = "wrongpassword"
            
            # Hash the password
            hashed = get_password_hash(test_password)
            print(f"Password '{test_password}' hashed successfully")
            
            # Verify the correct password
            is_correct = verify_password(test_password, hashed)
            print(f"Verification of correct password: {is_correct}")
            
            # Verify the wrong password
            is_wrong = verify_password(wrong_password, hashed)
            print(f"Verification of wrong password: {is_wrong}")
            
            # Check if there are any existing users in the database
            result = await session.execute(text("SELECT email, hashed_password FROM user LIMIT 1"))
            row = result.fetchone()
            
            if row:
                email, db_hashed_password = row
                print(f"\nFound user in database: {email}")
                
                # Test authentication with the existing user
                print(f"Testing authentication with correct password...")
                authenticated_user = await auth_service.authenticate_user(email, "password123")
                
                if authenticated_user:
                    print(f"Authentication successful! User ID: {authenticated_user.id}")
                    print(f"User email: {authenticated_user.email}")
                else:
                    print("Authentication failed with correct password!")
                    
                # Test with wrong password
                print(f"Testing authentication with wrong password...")
                failed_auth = await auth_service.authenticate_user(email, "wrongpassword")
                if not failed_auth:
                    print("Correctly failed authentication with wrong password")
                else:
                    print("ERROR: Authentication should have failed with wrong password")
            else:
                print("No users found in database")
                
    except Exception as e:
        print(f"Error during password verification test: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_password_verification())