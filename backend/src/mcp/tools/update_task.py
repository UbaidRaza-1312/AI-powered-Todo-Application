"""
MCP Tool: update_task
Updates an existing task for a user
"""
from typing import Dict, Any
import uuid
from sqlmodel import select
from ...models.task import Task
from ...db.database import get_session_maker


async def update_task(task_id: str, user_id: str, title: str = None, description: str = None, completed: bool = None) -> Dict[str, Any]:
    """
    Updates an existing task for the specified user

    Args:
        task_id: The ID of the task to update
        user_id: The ID of the user who owns the task
        title: New title for the task (optional)
        description: New description for the task (optional)
        completed: New completion status for the task (optional)

    Returns:
        Dictionary with update result
    """
    task_uuid = uuid.UUID(task_id)
    user_uuid = uuid.UUID(user_id)

    session_maker = get_session_maker()
    async with session_maker() as session:
        # Verify that the task belongs to the user
        statement = select(Task).where(Task.id == task_uuid).where(Task.user_id == user_uuid)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return {
                "success": False,
                "error": "Task not found or does not belong to user"
            }

        # Update the task with provided values
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "updated_task": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            },
            "message": "Task updated successfully"
        }


# Import and register this tool with the MCP server later to avoid circular imports
def register_tool():
    from ..server import mcp_server
    mcp_server.register_tool("update_task", update_task)