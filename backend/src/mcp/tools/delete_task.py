"""
MCP Tool: delete_task
Deletes a task for a user
"""
from typing import Dict, Any
import uuid
from sqlmodel import select
from ...models.task import Task
from ...db.database import get_session_maker
from ...utils.logging import log_info, log_error


async def delete_task(task_id: str, user_id: str) -> Dict[str, Any]:
    """
    Deletes a task for the specified user

    Args:
        task_id: The ID of the task to delete
        user_id: The ID of the user who owns the task

    Returns:
        Dictionary with deletion result
    """
    try:
        task_uuid = uuid.UUID(task_id)
        user_uuid = uuid.UUID(user_id)

        session_maker = get_session_maker()
        async with session_maker() as session:
            # Verify that the task belongs to the user
            statement = select(Task).where(Task.id == task_uuid).where(Task.user_id == user_uuid)
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            if not task:
                log_info(f"Task {task_id} not found for user {user_id} during deletion")
                return {
                    "success": False,
                    "error": "Task not found or does not belong to user"
                }

            # Delete the task
            await session.delete(task)
            await session.commit()

            log_info(f"Task {task.id} ('{task.title}') deleted successfully for user {user_id}")

            return {
                "success": True,
                "message": f"Task '{task.title}' deleted successfully"
            }
    except ValueError:
        # Invalid UUID format
        log_error(f"Invalid UUID format for task_id: {task_id} or user_id: {user_id}")
        return {
            "success": False,
            "error": "Invalid task ID or user ID format"
        }
    except Exception as e:
        log_error(f"Error deleting task {task_id} for user {user_id}: {str(e)}")
        return {
            "success": False,
            "error": f"An error occurred while deleting the task: {str(e)}"
        }


# Import and register this tool with the MCP server later to avoid circular imports
def register_tool():
    from ..server import mcp_server
    mcp_server.register_tool("delete_task", delete_task)