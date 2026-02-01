#!/usr/bin/env python3
"""
Simple test script to verify ChatAgent can be instantiated without errors
"""
import os
import sys
import pathlib

# Add the src directory to the path
src_dir = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_dir)

# Also add parent directory to handle relative imports in modules
parent_dir = os.path.dirname(src_dir)
sys.path.insert(0, parent_dir)

# Mock the GEMINI_API_KEY environment variable
os.environ['GEMINI_API_KEY'] = 'fake-key-for-testing'

try:
    from src.agents.chat_agent import ChatAgent
    print("Creating ChatAgent instance...")
    agent = ChatAgent()
    print("SUCCESS: ChatAgent created without errors!")
    print(f"Number of tools registered: {len(agent.tools[0]['function_declarations']) if agent.tools else 0}")

    # Print the first few tools to verify they're properly structured
    if agent.tools and agent.tools[0]['function_declarations']:
        print("\nSample tools:")
        for i, tool in enumerate(agent.tools[0]['function_declarations'][:3]):  # Show first 3 tools
            print(f"  {i+1}. Name: {tool['name']}")
            print(f"     Description: {tool['description'][:60]}...")  # First 60 chars
            print(f"     Parameters: {list(tool['parameters'].get('properties', {}).keys())}")
            print()

except Exception as e:
    print(f"ERROR: Failed to create ChatAgent: {e}")
    import traceback
    traceback.print_exc()