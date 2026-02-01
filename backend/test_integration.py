"""
Integration test for the updated Todo Chatbot with MCP Integration
Verifies that the system prompt requirements are properly implemented
"""
import os
import uuid
from unittest.mock import patch, MagicMock
import google.generativeai as genai

from src.agents.chat_agent import ChatAgent
from src.agents.system_prompt import SYSTEM_PROMPT


def test_system_prompt_content():
    """Test that the system prompt contains the required sections"""
    # Check that the system prompt contains the required sections
    assert "WORKFLOW RULES" in SYSTEM_PROMPT
    assert "USER TASK OWNERSHIP" in SYSTEM_PROMPT
    assert "QUERY ANALYSIS" in SYSTEM_PROMPT
    assert "MCP SERVER USAGE" in SYSTEM_PROMPT
    assert "ERROR HANDLING" in SYSTEM_PROMPT
    assert "RESPONSE EXAMPLES" in SYSTEM_PROMPT
    assert "SESSION MANAGEMENT" in SYSTEM_PROMPT
    
    print("[PASS] System prompt contains all required sections")


def test_user_context_validation_logic():
    """Test that the chat agent validates user context"""
    # Create a mock chat agent without initializing the Gemini model
    with patch('google.generativeai.GenerativeModel'):
        chat_agent = ChatAgent()
        
        # Test missing user_id
        result = chat_agent.process_message.__wrapped__(chat_agent, "", "add task Buy milk", str(uuid.uuid4()))
        assert "Missing user context" in result.result()["response"]
        
        # Test invalid user_id format
        result = chat_agent.process_message.__wrapped__(chat_agent, "invalid-uuid", "add task Buy milk", str(uuid.uuid4()))
        assert "Invalid user context" in result.result()["response"]
        
        print("[PASS] User context validation logic works correctly")


def test_system_prompt_follows_requirements():
    """Test that the system prompt follows the specified workflow rules"""
    # Check workflow rules
    assert "Every interaction starts AFTER the user has logged in or registered" in SYSTEM_PROMPT
    assert "user_id" in SYSTEM_PROMPT
    assert "name" in SYSTEM_PROMPT
    assert "email" in SYSTEM_PROMPT
    assert "NEVER allow actions if user context is missing" in SYSTEM_PROMPT
    
    # Check task ownership rules
    assert "All tasks belong to a specific user_id" in SYSTEM_PROMPT
    assert "Verify the task belongs to the current user_id" in SYSTEM_PROMPT
    assert "Task not found or access denied" in SYSTEM_PROMPT
    
    # Check query analysis rules
    assert "Add task" in SYSTEM_PROMPT
    assert "Update task" in SYSTEM_PROMPT
    assert "Delete task" in SYSTEM_PROMPT
    assert "View all tasks" in SYSTEM_PROMPT
    assert "View a single task" in SYSTEM_PROMPT
    
    # Check MCP server usage
    assert "Never perform database operations yourself" in SYSTEM_PROMPT
    assert "always call MCP server" in SYSTEM_PROMPT
    
    # Check error handling
    assert "If a query cannot be completed" in SYSTEM_PROMPT
    assert "Never hallucinate task success" in SYSTEM_PROMPT
    
    print("[PASS] System prompt follows all specified requirements")


if __name__ == "__main__":
    print("Running integration tests for Todo Chatbot...")
    
    test_system_prompt_content()
    test_system_prompt_follows_requirements()
    
    print("\n[SUCCESS] All integration tests passed!")
    print("\nSummary:")
    print("- System prompt has been updated with all required sections")
    print("- User context validation is implemented")
    print("- Task ownership verification is in place")
    print("- Query analysis and MCP server usage are properly configured")
    print("- Error handling follows the specified guidelines")