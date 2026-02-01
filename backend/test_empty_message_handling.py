#!/usr/bin/env python3
"""
Test script to verify that empty messages are properly handled by the backend
"""
import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock

# Add the src directory to the path
src_dir = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_dir)

async def test_empty_message_handling():
    """Test that the chat endpoint properly handles empty messages"""
    print("Testing empty message handling in chat endpoint...")
    
    # Import the chat endpoint function
    from src.api.chat_routes import chat, ChatRequest
    from sqlmodel.ext.asyncio.session import AsyncSession
    from uuid import UUID
    
    # Create mock objects
    mock_session = AsyncMock(spec=AsyncSession)
    mock_user_id = UUID("12345678-1234-5678-1234-567812345678")
    
    # Test with empty string message
    empty_request = ChatRequest(conversation_id=None, message="")
    
    # Mock the response from the session.get and other methods
    mock_session.get.return_value = None
    
    # Mock the conversation creation
    from src.models.conversation import Conversation
    mock_conversation = Conversation(user_id=mock_user_id)
    mock_conversation.id = UUID("87654321-4321-8765-4321-87654321dcba")
    
    # Patch the session.add and commit methods
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    try:
        # Call the chat endpoint with an empty message
        result = await chat(
            user_id=mock_user_id,
            chat_request=empty_request,
            current_user_id=mock_user_id,
            session=mock_session
        )
        
        print(f"[PASS] Successfully processed empty message")
        print(f"  Response: {result.response}")
        print(f"  Expected: 'I didn't receive any message. Please send a message to continue our conversation.'")

        expected_response = "I didn't receive any message. Please send a message to continue our conversation."
        if result.response == expected_response:
            print("[PASS] Empty message handling is working correctly!")
            return True
        else:
            print(f"[FAIL] Unexpected response: {result.response}")
            return False
            
    except Exception as e:
        print(f"[FAIL] Error testing empty message handling: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_whitespace_only_message():
    """Test that the chat endpoint properly handles whitespace-only messages"""
    print("\nTesting whitespace-only message handling...")
    
    from src.api.chat_routes import chat, ChatRequest
    from sqlmodel.ext.asyncio.session import AsyncSession
    from uuid import UUID
    
    # Create mock objects
    mock_session = AsyncMock(spec=AsyncSession)
    mock_user_id = UUID("12345678-1234-5678-1234-567812345678")
    
    # Test with whitespace-only message
    whitespace_request = ChatRequest(conversation_id=None, message="   \t\n   ")
    
    # Mock the response from the session.get and other methods
    mock_session.get.return_value = None
    
    # Mock the conversation creation
    from src.models.conversation import Conversation
    mock_conversation = Conversation(user_id=mock_user_id)
    mock_conversation.id = UUID("87654321-4321-8765-4321-87654321dcba")
    
    # Patch the session.add and commit methods
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    try:
        # Call the chat endpoint with a whitespace-only message
        result = await chat(
            user_id=mock_user_id,
            chat_request=whitespace_request,
            current_user_id=mock_user_id,
            session=mock_session
        )
        
        print(f"[PASS] Successfully processed whitespace-only message")
        print(f"  Response: {result.response}")
        print(f"  Expected: 'I didn't receive any message. Please send a message to continue our conversation.'")

        expected_response = "I didn't receive any message. Please send a message to continue our conversation."
        if result.response == expected_response:
            print("[PASS] Whitespace-only message handling is working correctly!")
            return True
        else:
            print(f"[FAIL] Unexpected response: {result.response}")
            return False
            
    except Exception as e:
        print(f"[FAIL] Error testing whitespace-only message handling: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("Running tests for empty message handling...\n")
    
    test1_passed = await test_empty_message_handling()
    test2_passed = await test_whitespace_only_message()
    
    print(f"\nTest Results:")
    print(f"- Empty message test: {'PASS' if test1_passed else 'FAIL'}")
    print(f"- Whitespace-only message test: {'PASS' if test2_passed else 'FAIL'}")

    if test1_passed and test2_passed:
        print("\n[PASS] All tests passed! Empty message handling is working correctly.")
        return True
    else:
        print("\n[FAIL] Some tests failed!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)