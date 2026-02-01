"""
MCP Tool: delete_task_by_reference
Deletes a task for a user by reference (ID, title, or position)
"""
from typing import Dict, Any
import uuid
import re
from sqlmodel import select
from ...models.task import Task
from ...db.database import get_session_maker
from ...utils.logging import log_info, log_error


async def delete_task_by_reference(task_reference: str, user_id: str) -> Dict[str, Any]:
    """
    Deletes a task for the specified user by reference (ID, title, or position)

    Args:
        task_reference: The ID, title, or position (e.g., "task2") of the task to delete
        user_id: The ID of the user who owns the task

    Returns:
        Dictionary with deletion result
    """
    try:
        user_uuid = uuid.UUID(user_id)

        session_maker = get_session_maker()
        async with session_maker() as session:
            # Check if the reference is a UUID
            try:
                task_uuid = uuid.UUID(task_reference)
                # Direct UUID lookup
                statement = select(Task).where(Task.id == task_uuid).where(Task.user_id == user_uuid)
                result = await session.execute(statement)
                task = result.scalar_one_or_none()

                if task:
                    await session.delete(task)
                    await session.commit()
                    log_info(f"Task {task.id} ('{task.title}') deleted by UUID for user {user_id}")
                    return {
                        "success": True,
                        "message": f"Task '{task.title}' deleted successfully"
                    }
                else:
                    log_info(f"UUID task {task_reference} not found for user {user_id}")
            except ValueError:
                # Not a UUID, could be a position reference or title
                pass

            # Check if the reference is a position reference (e.g., "task2", "task 2", "2", "second")
            # Handle both "task2" and "task 2" formats
            position_match = re.search(r'(?:task\s*)?(\d+)', task_reference.lower())
            if position_match:
                position = int(position_match.group(1)) - 1  # Convert to 0-indexed

                # Get all tasks for the user ordered by creation date
                statement = select(Task).where(Task.user_id == user_uuid).order_by(Task.created_at)
                result = await session.execute(statement)
                tasks = result.scalars().all()

                if 0 <= position < len(tasks):
                    task = tasks[position]
                    await session.delete(task)
                    await session.commit()
                    log_info(f"Task {task.id} ('{task.title}') deleted by position {position+1} for user {user_id}")
                    return {
                        "success": True,
                        "message": f"Task '{task.title}' deleted successfully"
                    }
                else:
                    log_info(f"Position {position + 1} is out of range for user {user_id} (has {len(tasks)} tasks)")
                    return {
                        "success": False,
                        "error": f"Position {position + 1} is out of range. You only have {len(tasks)} tasks."
                    }

            # If not a position reference, try to match by title
            statement = select(Task).where(Task.title.ilike(f'%{task_reference}%')).where(Task.user_id == user_uuid)
            result = await session.execute(statement)
            tasks = result.scalars().all()

            if len(tasks) == 0:
                log_info(f"No tasks found matching '{task_reference}' for user {user_id}")
                return {
                    "success": False,
                    "error": "Task not found or does not belong to user"
                }
            elif len(tasks) == 1:
                task = tasks[0]
                await session.delete(task)
                await session.commit()
                log_info(f"Task {task.id} ('{task.title}') deleted by title for user {user_id}")
                return {
                    "success": True,
                    "message": f"Task '{task.title}' deleted successfully"
                }
            else:
                # Multiple tasks match, return a list of possibilities
                task_titles = [task.title for task in tasks[:5]]  # Limit to first 5 matches
                log_info(f"Multiple tasks ({len(tasks)}) match '{task_reference}' for user {user_id}")
                return {
                    "success": False,
                    "error": f"Multiple tasks match '{task_reference}'. Please be more specific. Matches: {', '.join(task_titles)}"
                }
    except ValueError:
        # Invalid UUID format for user_id
        log_error(f"Invalid UUID format for user_id: {user_id}")
        return {
            "success": False,
            "error": "Invalid user ID format"
        }
    except Exception as e:
        log_error(f"Error deleting task by reference '{task_reference}' for user {user_id}: {str(e)}")
        return {
            "success": False,
            "error": f"An error occurred while deleting the task: {str(e)}"
        }


# Import and register this tool with the MCP server later to avoid circular imports
def register_tool():
    from ..server import mcp_server
    mcp_server.register_tool("delete_task_by_reference", delete_task_by_reference)