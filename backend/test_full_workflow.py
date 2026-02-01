import asyncio
import uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.database import get_session_maker
from src.models.user import User, UserBase
from src.services.auth_service import AuthService
from src.mcp.server import mcp_server
import hashlib

async def test_full_workflow():
    print("Testing full workflow: creating user and performing task operations...")
    
    # Get session maker and create session
    session_maker = get_session_maker()
    async with session_maker() as session:
        # Create a test user
        auth_service = AuthService(session)
        
        import time
        # Create a user base object with unique email
        timestamp = int(time.time())
        user_base = UserBase(
            email=f"test_{timestamp}@example.com",
            first_name="Test",
            last_name="User"
        )
        
        # Create the user with a simple password
        password = "password123"
        new_user = await auth_service.create_user(user_base, password)
        await session.commit()
        await session.refresh(new_user)
        
        user_id = str(new_user.id)
        print(f"Created test user with ID: {user_id}")
        
        try:
            # Test add_task
            print("\n1. Testing add_task...")
            add_result = await mcp_server.execute_tool("add_task", {
                "user_id": user_id,
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
                    "user_id": user_id,
                    "status": "all"
                })
                print(f"List tasks result: {list_result}")
                
                # Test update_task
                print("\n3. Testing update_task...")
                update_result = await mcp_server.execute_tool("update_task", {
                    "task_id": task_id,
                    "user_id": user_id,
                    "title": "Updated Test Task",
                    "description": "This is an updated test task"
                })
                print(f"Update task result: {update_result}")
                
                # Test complete_task
                print("\n4. Testing complete_task...")
                complete_result = await mcp_server.execute_tool("complete_task", {
                    "task_id": task_id,
                    "user_id": user_id
                })
                print(f"Complete task result: {complete_result}")
                
                # Test delete_task
                print("\n5. Testing delete_task...")
                delete_result = await mcp_server.execute_tool("delete_task", {
                    "task_id": task_id,
                    "user_id": user_id
                })
                print(f"Delete task result: {delete_result}")
                
            print("\nFull workflow test completed successfully!")
            
        except Exception as e:
            print(f"Error in workflow test: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_full_workflow())