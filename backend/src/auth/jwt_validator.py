"""
JWT Validator for AI Chatbot with MCP Integration
Provides dependency functions for validating JWT tokens in API endpoints
"""
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
from ..utils.auth import verify_token


security = HTTPBearer()


def validate_user_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Dependency function to validate JWT tokens and extract user information
    
    Args:
        credentials: HTTP authorization credentials containing the JWT
        
    Returns:
        Dictionary containing user information from the token payload
        
    Raises:
        HTTPException: If the token is invalid or expired
    """
    token = credentials.credentials
    
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user information from the payload
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Return the user information
    return {
        "user_id": user_id,
        "email": payload.get("email")
    }