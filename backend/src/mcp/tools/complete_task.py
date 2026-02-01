"""
MCP Tool: complete_task
Marks a task as complete for a user
"""
from typing import Dict, Any
import uuid
from sqlmodel import select
from ...models.task import Task
from ...db.database import get_session_maker


async def complete_task(task_id: str, user_id: str) -> Dict[str, Any]:
    """
    Marks a task as complete for the specified user

    Args:
        task_id: The ID of the task to mark as complete
        user_id: The ID of the user who owns the task

    Returns:
        Dictionary with completion result
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

        # Update the task completion status
        task.completed = True
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "message": f"Task '{task.title}' marked as complete"
        }


# Import and register this tool with the MCP server later to avoid circular imports
def register_tool():
    from ..server import mcp_server
    mcp_server.register_tool("complete_task", complete_task)