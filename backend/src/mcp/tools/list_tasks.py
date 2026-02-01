"""
MCP Tool: list_tasks
Lists tasks for a user with optional filtering
"""
from typing import Dict, Any, List
import uuid
from sqlmodel import select
from ...models.task import Task
from ...db.database import get_session_maker


async def list_tasks(user_id: str, status: str = "all") -> Dict[str, Any]:
    """
    Lists tasks for the specified user with optional status filtering

    Args:
        user_id: The ID of the user whose tasks to list
        status: Filter by status - "all", "pending", or "completed"

    Returns:
        Dictionary with list of tasks
    """
    user_uuid = uuid.UUID(user_id)

    session_maker = get_session_maker()
    async with session_maker() as session:
        # Build query based on status filter
        query = select(Task).where(Task.user_id == user_uuid)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        result = await session.execute(query)
        tasks = result.scalars().all()

        task_list = []
        for task in tasks:
            task_list.append({
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            })

        return {
            "success": True,
            "tasks": task_list
        }


# Import and register this tool with the MCP server later to avoid circular imports
def register_tool():
    from ..server import mcp_server
    mcp_server.register_tool("list_tasks", list_tasks)