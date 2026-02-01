"""
More comprehensive debug script to test the full chatbot flow
"""
import asyncio
import uuid
from unittest.mock import patch, AsyncMock
from src.agents.chat_agent import ChatAgent
from src.mcp.server import mcp_server

async def debug_chat_flow():
    print("=== DEBUGGING CHATBOT FLOW FOR DELETE ===")
    
    # Create a chat agent
    chat_agent = ChatAgent()
    
    # Mock user context
    user_id = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())
    
    print(f"Using user_id: {user_id}")
    print(f"Using conversation_id: {conversation_id}")
    
    # Test the specific command that's problematic
    with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker:
        # Create a mock session
        mock_session = AsyncMock()
        mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value
        
        # Mock the MCP server's execute_tool method to see what's happening
        with patch.object(mcp_server, 'execute_tool', new_callable=AsyncMock) as mock_execute:
            # Mock the tool to return success (this simulates what might be happening)
            mock_execute.return_value = {
                "success": True,
                "result": {
                    "success": True,
                    "message": "Task 'Sample task' deleted successfully"
                }
            }
            
            print(f"\nTesting command: 'delete task 1'")
            result = await chat_agent.process_message(
                user_id,
                "delete task 1",
                conversation_id
            )
            
            print(f"Chatbot response: {result['response']}")
            print(f"Tool calls: {result['tool_calls']}")
            
            # Check what tool was actually called
            if mock_execute.called:
                call_args = mock_execute.call_args
                print(f"Tool called: {call_args[0][0]}")  # First argument is tool name
                print(f"Arguments: {call_args[1]}")  # Keyword arguments

if __name__ == "__main__":
    asyncio.run(debug_chat_flow())