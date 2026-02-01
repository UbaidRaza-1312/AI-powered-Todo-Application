"""
Test to verify the chat agent properly handles delete commands with full mocking
"""
import asyncio
import uuid
from unittest.mock import AsyncMock, patch, MagicMock
from src.agents.chat_agent import ChatAgent

async def test_chat_agent_fully_mocked():
    print("=== TESTING CHAT AGENT WITH FULL MOCKING ===")
    
    # Mock the Gemini API components before creating the agent
    with patch('src.agents.chat_agent.genai') as mock_genai:
        # Set up the mock model and chat
        mock_model_instance = MagicMock()
        mock_chat_instance = MagicMock()
        
        # Create a mock response that simulates a tool call for delete_task_by_reference
        mock_candidate = MagicMock()
        mock_candidate.finish_reason.name = "TOOL_CALL"
        
        # Create a mock function call part
        mock_function_call_part = MagicMock()
        mock_function_call_part.function_call.name = "delete_task_by_reference"
        mock_function_call_part.function_call.args = {"task_reference": "task 1"}
        
        mock_candidate.content.parts = [mock_function_call_part]
        
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        
        # Configure the mock chat to return our response
        mock_chat_instance.send_message_async = AsyncMock(return_value=mock_response)
        mock_model_instance.start_chat.return_value = mock_chat_instance
        
        # Configure the mock genai module
        mock_genai.configure = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model_instance
        
        # Now create the agent with mocked dependencies
        agent = ChatAgent()
        
        # Mock user and conversation IDs
        user_id = str(uuid.uuid4())
        conversation_id = str(uuid.uuid4())
        
        # Mock the session maker to avoid database calls
        with patch('src.agents.chat_agent.get_session_maker') as mock_session_maker:
            mock_session = AsyncMock()
            mock_session_maker.return_value = lambda: mock_session.__aenter__.return_value
            
            # Mock the MCP server's execute_tool to track what gets called
            with patch('src.agents.chat_agent.mcp_server') as mock_mcp_server:
                mock_mcp_server.execute_tool = AsyncMock(return_value={
                    "success": True,
                    "result": {
                        "success": True,
                        "message": "Task 'Sample task' deleted successfully"
                    }
                })
                
                print(f"Testing 'delete task 1' command...")
                result = await agent.process_message(
                    user_id=user_id,
                    message="delete task 1",
                    conversation_id=conversation_id
                )
                
                print(f"Response: {result['response']}")
                print(f"Tool calls made: {len(result['tool_calls'])}")
                
                # Verify that the MCP server execute_tool was called
                if mock_mcp_server.execute_tool.called:
                    call_args = mock_mcp_server.execute_tool.call_args
                    tool_name = call_args[0][0]  # First positional argument is tool name
                    tool_args = call_args[0][1]  # Second positional argument is args dict
                    
                    print(f"MCP Tool called: {tool_name}")
                    print(f"MCP Tool arguments: {tool_args}")
                    
                    if tool_name == "delete_task_by_reference":
                        print("✅ Correct tool (delete_task_by_reference) was called!")
                        if tool_args.get("task_reference") == "task 1":
                            print("✅ Correct task reference ('task 1') was passed!")
                        else:
                            print(f"⚠️  Unexpected task reference: {tool_args.get('task_reference', 'NOT FOUND')}")
                    else:
                        print(f"❌ Wrong tool called: {tool_name}")
                        
                    if tool_args.get("user_id") == user_id:
                        print("✅ Correct user_id was passed!")
                    else:
                        print(f"⚠️  Unexpected user_id: {tool_args.get('user_id', 'NOT FOUND')}")
                else:
                    print("❌ MCP execute_tool was not called - this is the problem!")
                    
                print(f"\nFull result: {result}")

if __name__ == "__main__":
    asyncio.run(test_chat_agent_fully_mocked())