# src/api/task_routes.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
import uuid
from datetime import datetime

from ..db.database import get_async_session
from ..models.task import TaskBase
from ..services.task_service import TaskService
from ..middleware.auth_middleware import get_current_user


def parse_datetime(date_str: Optional[str]) -> Optional[datetime]:
    """Parse a date string to datetime object"""
    if not date_str:
        return None

    try:
        # Try to parse the date string - assuming ISO format
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        # If parsing fails, try other common formats
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # If all parsing fails, return None
            return None

router = APIRouter()


# ---------- Schemas ----------

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: int = 1


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[str] = None
    priority: Optional[int] = None


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    completed: bool
    user_id: uuid.UUID
    created_at: str
    updated_at: str
    due_date: Optional[str]
    priority: int


# ---------- Routes ----------

@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    completed: Optional[bool] = Query(None),
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get all tasks for logged-in user"""

    user_id: UUID = user["user_id"]

    async with session.begin():
        service = TaskService(session)
        tasks = await service.get_tasks_by_user(user_id, completed)

        return [
            TaskResponse(
                id=t.id,
                title=t.title,
                description=t.description,
                completed=t.completed,
                user_id=t.user_id,
                created_at=t.created_at.isoformat(),
                updated_at=t.updated_at.isoformat(),
                due_date=t.due_date.isoformat() if t.due_date else None,
                priority=t.priority,
            )
            for t in tasks
        ]


@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Create task for logged-in user"""

    user_id: UUID = user["user_id"]

    async with session.begin():
        service = TaskService(session)

        # Convert due_date string to datetime if provided
        due_date = parse_datetime(task_data.due_date)

        task_base = TaskBase(
            title=task_data.title,
            description=task_data.description,
            completed=False,  # Explicitly set the completed field
            user_id=user_id,
            due_date=due_date,
            priority=task_data.priority,
        )

        task = await service.create_task(task_base, user_id)

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
            due_date=task.due_date.isoformat() if task.due_date else None,
            priority=task.priority,
        )


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Get single task"""

    user_id: UUID = user["user_id"]

    async with session.begin():
        service = TaskService(session)
        task = await service.get_task_by_id(task_id, user_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
            due_date=task.due_date.isoformat() if task.due_date else None,
            priority=task.priority,
        )


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Update task"""

    user_id: UUID = user["user_id"]

    async with session.begin():
        service = TaskService(session)

        # Convert due_date string to datetime if provided
        due_date = parse_datetime(task_data.due_date)

        task_base = TaskBase(
            title=task_data.title or "",
            description=task_data.description,
            completed=task_data.completed if task_data.completed is not None else False,
            user_id=user_id,
            due_date=due_date,
            priority=task_data.priority or 1,
        )

        task = await service.update_task(task_id, task_base, user_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
            due_date=task.due_date.isoformat() if task.due_date else None,
            priority=task.priority,
        )


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: UUID,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Delete task"""

    user_id: UUID = user["user_id"]

    async with session.begin():
        service = TaskService(session)
        success = await service.delete_task(task_id, user_id)

        if not success:
            raise HTTPException(status_code=404, detail="Task not found")

        return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: UUID,
    user=Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Toggle completion"""

    user_id: UUID = user["user_id"]

    async with session.begin():
        service = TaskService(session)
        task = await service.toggle_task_completion(task_id, user_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat(),
            due_date=task.due_date.isoformat() if task.due_date else None,
            priority=task.priority,
        )
