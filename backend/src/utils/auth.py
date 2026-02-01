from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
import bcrypt

# Secret key for JWT tokens - should come from environment
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    Truncate to 72 bytes to match bcrypt limit.
    """
    # Ensure password doesn't exceed bcrypt's 72-byte limit
    # First encode to bytes to check actual length
    encoded_password = plain_password.encode('utf-8')

    # If the encoded password is longer than 72 bytes, truncate it
    if len(encoded_password) > 72:
        encoded_password = encoded_password[:72]
        # Decode back to string, handling any incomplete character sequences
        safe_password = encoded_password.decode('utf-8', errors='ignore')
    else:
        # If it's within the limit, use the original password
        safe_password = plain_password

    # Use bcrypt to verify - hashed_password should be handled properly for SQLite
    try:
        return bcrypt.checkpw(safe_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        # Fallback for different encoding issues
        return bcrypt.checkpw(safe_password.encode('utf-8'), hashed_password.encode('ascii'))

def get_password_hash(password: str) -> str:
    """
    Hash a plaintext password.
    Truncate to 72 bytes to prevent bcrypt errors.
    """
    # Ensure password doesn't exceed bcrypt's 72-byte limit
    # First encode to bytes to check actual length
    encoded_password = password.encode('utf-8')

    # If the encoded password is longer than 72 bytes, truncate it
    if len(encoded_password) > 72:
        encoded_password = encoded_password[:72]
        # Decode back to string, handling any incomplete character sequences
        safe_password = encoded_password.decode('utf-8', errors='ignore')
    else:
        # If it's within the limit, use the original password
        safe_password = password

    # Use bcrypt to hash
    salt = bcrypt.gensalt(rounds=12)  # Increased rounds for better security
    hashed_bytes = bcrypt.hashpw(safe_password.encode('utf-8'), salt)
    # Convert bytes to string for storage
    return hashed_bytes.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the payload if valid.
    Returns None if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
