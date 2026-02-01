"""
Test to verify the chat agent properly handles delete commands
"""
import asyncio
import uuid
from unittest.mock import AsyncMock, patch
from src.agents.chat_agent import ChatAgent
from src.mcp.server import mcp_server

async def test_chat_agent_with_mock():
    print("=== TESTING CHAT AGENT WITH MOCKED TOOLS ===")
    
    # Create a chat agent
    agent = ChatAgent()
    
    # Mock user and conversation IDs
    user_id = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())
    
    # Mock the session maker to avoid database calls
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker:
        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value
        
        # Mock the MCP server's execute_tool to track what gets called
        with patch.object(mcp_server, 'execute_tool', new_callable=AsyncMock) as mock_execute:
            # Mock the tool response for delete_task_by_reference
            mock_execute.return_value = {
                "success": True,
                "result": {
                    "success": True,
                    "message": "Task 'Sample task' deleted successfully"
                }
            }
            
            print(f"Testing 'delete task 1' command...")
            result = await agent.process_message(
                user_id=user_id,
                message="delete task 1",
                conversation_id=conversation_id
            )
            
            print(f"Response: {result['response']}")
            print(f"Tool calls made: {len(result['tool_calls'])}")
            
            # Verify that the correct tool was called
            if mock_execute.called:
                call_args = mock_execute.call_args
                tool_name = call_args[0][0]  # First positional argument is tool name
                tool_args = call_args[1]     # Keyword arguments
                
                print(f"Tool called: {tool_name}")
                print(f"Tool arguments: {tool_args}")
                
                if tool_name == "delete_task_by_reference":
                    print("✅ Correct tool (delete_task_by_reference) was called!")
                    if "task_reference" in tool_args and tool_args["task_reference"] == "task 1":
                        print("✅ Correct task reference ('task 1') was passed!")
                    else:
                        print(f"⚠️  Unexpected task reference: {tool_args.get('task_reference', 'NOT FOUND')}")
                else:
                    print(f"❌ Wrong tool called: {tool_name}")
            else:
                print("❌ No tool was called - this is the problem!")
                
            print(f"\nFull result: {result}")

if __name__ == "__main__":
    asyncio.run(test_chat_agent_with_mock())