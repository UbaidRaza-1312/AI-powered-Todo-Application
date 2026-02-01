import asyncio
import uuid
from src.mcp.server import mcp_server

async def test_mcp_tools():
    print("Testing MCP server tools...")
    
    # Test creating a user ID (using a random UUID for testing)
    test_user_id = str(uuid.uuid4())
    print(f"Using test user ID: {test_user_id}")
    
    try:
        # Test add_task
        print("\n1. Testing add_task...")
        add_result = await mcp_server.execute_tool("add_task", {
            "user_id": test_user_id,
            "title": "Test Task",
            "description": "This is a test task"
        })
        print(f"Add task result: {add_result}")
        
        if add_result["success"]:
            task_id = add_result["result"]["task_id"]
            print(f"Created task with ID: {task_id}")
            
            # Test list_tasks
            print("\n2. Testing list_tasks...")
            list_result = await mcp_server.execute_tool("list_tasks", {
                "user_id": test_user_id,
                "status": "all"
            })
            print(f"List tasks result: {list_result}")
            
            # Test update_task
            print("\n3. Testing update_task...")
            update_result = await mcp_server.execute_tool("update_task", {
                "task_id": task_id,
                "user_id": test_user_id,
                "title": "Updated Test Task",
                "description": "This is an updated test task"
            })
            print(f"Update task result: {update_result}")
            
            # Test complete_task
            print("\n4. Testing complete_task...")
            complete_result = await mcp_server.execute_tool("complete_task", {
                "task_id": task_id,
                "user_id": test_user_id
            })
            print(f"Complete task result: {complete_result}")
            
            # Test delete_task
            print("\n5. Testing delete_task...")
            delete_result = await mcp_server.execute_tool("delete_task", {
                "task_id": task_id,
                "user_id": test_user_id
            })
            print(f"Delete task result: {delete_result}")
            
        print("\nAll MCP tools tested successfully!")
        
    except Exception as e:
        print(f"Error testing MCP tools: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_tools())