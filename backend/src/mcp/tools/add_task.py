"""
MCP Tool: add_task
Creates a new task for a user
"""
from typing import Dict, Any
import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ...models.task import Task
from ...db.database import get_session_maker
from contextlib import asynccontextmanager


async def add_task(user_id: str, title: str, description: str = None) -> Dict[str, Any]:
    """
    Creates a new task for the specified user

    Args:
        user_id: The ID of the user creating the task
        title: The title of the task
        description: Optional description of the task

    Returns:
        Dictionary with task creation result
    """
    user_uuid = uuid.UUID(user_id)

    # Create a new task
    task = Task(
        user_id=user_uuid,
        title=title,
        description=description,
        completed=False
    )

    # Get session maker and create session
    session_maker = get_session_maker()
    async with session_maker() as session:
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "task_id": str(task.id),
            "message": f"Task '{task.title}' created successfully"
        }


# Import and register this tool with the MCP server later to avoid circular imports
def register_tool():
    from ..server import mcp_server
    mcp_server.register_tool("add_task", add_task)