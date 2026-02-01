"""
Test the delete_task_by_reference function directly
"""
import asyncio
from src.mcp.tools.delete_task_by_reference import delete_task_by_reference

async def test_delete_function():
    print("=== TESTING DELETE FUNCTION DIRECTLY ===")
    
    # Test with a sample user_id and task_reference
    user_id = "5807fcba-83e4-4328-b0ea-6c851ea2db99"
    
    # First, let's see what happens when we try to delete a non-existent task
    result = await delete_task_by_reference(task_reference="task2", user_id=user_id)
    print(f"Result for 'task2': {result}")
    
    # Also test with a more specific reference
    result2 = await delete_task_by_reference(task_reference="task 2", user_id=user_id)
    print(f"Result for 'task 2': {result2}")

if __name__ == "__main__":
    asyncio.run(test_delete_function())