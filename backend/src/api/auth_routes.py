from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional
from ..db.database import get_async_session
from ..models.user import User, UserBase
from ..services.auth_service import AuthService
from ..utils.auth import verify_password, get_password_hash
from ..middleware.auth_middleware import get_current_user_id
from pydantic import BaseModel
from uuid import UUID
import uuid
from sqlmodel import select
from sqlalchemy import func
from ..models.task import Task

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: str

@router.post("/auth/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    """Register a new user"""
    auth_service = AuthService(session)

    # Check if user already exists
    existing_user = await auth_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user
    user_base = UserBase(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    new_user = await auth_service.create_user(user_base, user_data.password)

    await session.commit()
    await session.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        created_at=new_user.created_at.isoformat()
    )

@router.post("/auth/login", response_model=TokenResponse)
async def login_user(user_data: UserLogin, session: AsyncSession = Depends(get_async_session)):
    """Login a user and return access token"""
    auth_service = AuthService(session)

    user = await auth_service.authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = await auth_service.create_access_token_for_user(user)

    return TokenResponse(access_token=access_token, token_type="bearer")

@router.get("/auth/me", response_model=UserResponse)
async def get_current_user(
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get current user information"""
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_id(current_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at.isoformat()
    )


@router.post("/auth/logout")
async def logout_user():
    """Logout a user (currently just a confirmation endpoint)"""
    # In a stateful session system, we would invalidate the session here
    # For JWT tokens, the client handles removal of the token
    # This endpoint serves as a confirmation that logout was initiated

    return {"message": "Logged out successfully"}

class UserProfileWithStats(BaseModel):
    id: uuid.UUID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: str
    total_tasks: int
    completed_tasks: int
    pending_tasks: int

@router.get("/auth/profile", response_model=UserProfileWithStats)
async def get_user_profile_with_stats(
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get current user information with task statistics"""
    auth_service = AuthService(session)
    user = await auth_service.get_user_by_id(current_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Count user's tasks
    total_tasks_stmt = select(Task).where(Task.user_id == current_user_id)
    total_tasks_result = await session.execute(select(func.count(Task.id)).where(Task.user_id == current_user_id))
    total_tasks = total_tasks_result.scalar() or 0

    completed_tasks_stmt = select(func.count(Task.id)).where(Task.user_id == current_user_id, Task.completed == True)
    completed_tasks_result = await session.execute(completed_tasks_stmt)
    completed_tasks = completed_tasks_result.scalar() or 0

    pending_tasks = total_tasks - completed_tasks

    return UserProfileWithStats(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at.isoformat(),
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks
    )