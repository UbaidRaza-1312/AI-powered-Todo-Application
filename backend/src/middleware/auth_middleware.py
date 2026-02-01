# src/middleware/auth_middleware.py

from fastapi import HTTPException, status, Request
from ..utils.auth import verify_token
from typing import Dict
import uuid


async def get_current_user(request: Request) -> Dict:
    """
    Extract full user context from JWT:
    {
      user_id,
      email,
      name
    }
    """

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = auth_header.split(" ")[1]
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    try:
        return {
            "user_id": uuid.UUID(payload["sub"]),
            "email": payload.get("email"),
            "name": payload.get("name"),
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )


async def get_current_user_id(request: Request) -> uuid.UUID:
    """
    Extract user_id from JWT token
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = auth_header.split(" ")[1]
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    try:
        user_id = uuid.UUID(payload["sub"])
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
