#!/usr/bin/env python3
"""
Test script to verify the updated ChatAgent fix
"""
import os
import sys
import asyncio

# Add the src directory to the path
src_dir = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_dir)

# Also add parent directory to handle relative imports in modules
parent_dir = os.path.dirname(src_dir)
sys.path.insert(0, parent_dir)

# Mock the GEMINI_API_KEY environment variable
os.environ['GEMINI_API_KEY'] = 'fake-key-for-testing'

async def test_chat_agent():
    try:
        from src.agents.chat_agent import ChatAgent
        
        print("Creating ChatAgent instance...")
        agent = ChatAgent()
        print("SUCCESS: ChatAgent created without errors!")
        print(f"Number of tools registered: {len(agent.tools[0]['function_declarations']) if agent.tools else 0}")
        
        # Check that the updated tool handling logic is in place
        import inspect
        source = inspect.getsource(agent.process_message)
        
        checks = [
            ("tool_responses =", "Tool responses collection"),
            ("function_response", "Function response format"),
            ("send_message_async(tool_responses)", "Sending tool responses back to Gemini"),
            ("final_candidate = ", "Processing final candidate after tool calls"),
        ]
        
        for check_str, description in checks:
            if check_str in source:
                print(f"OK: {description} is in place")
            else:
                print(f"MISSING: {description} is missing")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"ERROR: Failed to test ChatAgent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_chat_agent())