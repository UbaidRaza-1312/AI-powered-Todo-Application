"""
Debug script to test the delete functionality more thoroughly
"""
import asyncio
import uuid
from src.mcp.tools.delete_task_by_reference import delete_task_by_reference

async def debug_delete():
    print("=== DEBUGGING DELETE FUNCTIONALITY ===")
    
    # Use a known user_id from your test data
    user_id = "5807fcba-83e4-4328-b0ea-6c851ea2db99"
    
    print(f"\nTesting delete_task_by_reference with 'task 1' for user {user_id}")
    result = await delete_task_by_reference(task_reference="task 1", user_id=user_id)
    print(f"Result: {result}")
    
    print(f"\nTesting delete_task_by_reference with '1' for user {user_id}")
    result = await delete_task_by_reference(task_reference="1", user_id=user_id)
    print(f"Result: {result}")
    
    # Let's also test listing tasks to see what's available
    from src.mcp.tools.list_tasks import list_tasks
    print(f"\nListing tasks for user {user_id}")
    tasks_result = await list_tasks(user_id=user_id)
    print(f"Tasks: {tasks_result}")

if __name__ == "__main__":
    asyncio.run(debug_delete())