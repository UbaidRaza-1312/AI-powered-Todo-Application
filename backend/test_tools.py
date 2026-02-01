"""
Test to see if the AI is properly calling the delete_task_by_reference tool
"""
import asyncio
import uuid
from unittest.mock import AsyncMock, patch
from src.mcp.server import mcp_server

async def test_tool_registration():
    print("=== CHECKING REGISTERED TOOLS ===")
    print(f"Total tools registered: {len(mcp_server.tools)}")
    print("Registered tools:")
    for tool_name in mcp_server.tools.keys():
        print(f"  - {tool_name}")
    
    # Check if our specific tools are there
    expected_tools = ["delete_task", "delete_task_by_reference"]
    for tool in expected_tools:
        if tool in mcp_server.tools:
            print(f"[OK] {tool} is registered")
        else:
            print(f"[ERROR] {tool} is NOT registered")
    
    # Test calling the delete_task_by_reference function directly
    print("\n=== TESTING delete_task_by_reference DIRECTLY ===")
    try:
        # This will test if the function can be imported and called
        from src.mcp.tools.delete_task_by_reference import delete_task_by_reference
        
        # Create a fake user_id for testing
        test_user_id = str(uuid.uuid4())
        
        # Test with a non-existent task to see the error response
        result = await delete_task_by_reference(task_reference="1", user_id=test_user_id)
        print(f"Direct call result: {result}")
        
    except Exception as e:
        print(f"Error in direct call: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_tool_registration())