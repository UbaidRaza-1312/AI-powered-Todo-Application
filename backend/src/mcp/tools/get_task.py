"""
MCP Tool: get_task
Gets a specific task for a user
"""
from typing import Dict, Any
import uuid
from sqlmodel import select
from ...models.task import Task
from ...db.database import get_session_maker


async def get_task(task_id: str, user_id: str) -> Dict[str, Any]:
    """
    Gets a specific task for the specified user

    Args:
        task_id: The ID of the task to retrieve
        user_id: The ID of the user who owns the task

    Returns:
        Dictionary with task details
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

        return {
            "success": True,
            "task": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        }


# Import and register this tool with the MCP server later to avoid circular imports
def register_tool():
    from ..server import mcp_server
    mcp_server.register_tool("get_task", get_task)