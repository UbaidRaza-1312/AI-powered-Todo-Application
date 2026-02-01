"""
Test script to verify the fix for delete_task_by_reference function
"""
import asyncio
import uuid
import re
from src.mcp.tools.delete_task_by_reference import delete_task_by_reference

async def test_regex_patterns():
    """Test the regex pattern with different inputs"""
    print("=== Testing Regex Patterns ===")
    
    test_inputs = [
        "task1",
        "task 1", 
        "task  1",  # multiple spaces
        "1",
        "task2",
        "task 2",
        "delete task 1",
        "remove task 2"
    ]
    
    for test_input in test_inputs:
        # This is the new regex pattern we implemented
        position_match = re.search(r'(?:task\s*)?(\d+)', test_input.lower())
        if position_match:
            position = int(position_match.group(1))
            print(f"'{test_input}' -> matches position {position}")
        else:
            print(f"'{test_input}' -> no match")


async def test_delete_functionality():
    """Test the actual delete functionality"""
    print("\n=== Testing Delete Functionality ===")
    
    # Use a test user_id
    user_id = "5807fcba-83e4-4328-b0ea-6c851ea2db99"
    
    print("Testing various delete commands:")
    
    # Test different formats
    test_cases = [
        "task1",
        "task 1",
        "1"
    ]
    
    for task_ref in test_cases:
        print(f"\nTesting delete_task_by_reference with '{task_ref}':")
        try:
            result = await delete_task_by_reference(task_reference=task_ref, user_id=user_id)
            print(f"  Result: {result}")
        except Exception as e:
            print(f"  Error: {e}")


async def main():
    await test_regex_patterns()
    await test_delete_functionality()

if __name__ == "__main__":
    asyncio.run(main())