#!/usr/bin/env python3
"""
Test script to verify that the MCP tools are properly registered
"""
import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the MCP module to trigger registration
import backend.src.mcp

# Access the server and check registered tools
from backend.src.mcp.server import mcp_server

print(f"Number of registered tools: {len(mcp_server.tools)}")
print("Registered tools:", list(mcp_server.tools.keys()))

# Test that all expected tools are registered
expected_tools = ["add_task", "list_tasks", "update_task", "complete_task", "delete_task"]
missing_tools = [tool for tool in expected_tools if tool not in mcp_server.tools]

if missing_tools:
    print(f"Missing tools: {missing_tools}")
else:
    print("All expected tools are registered!")

async def test_tool():
    print("\nTesting a simple tool execution...")
    try:
        result = await mcp_server.execute_tool("list_tasks", {"user_id": "123e4567-e89b-12d3-a456-426614174000"})
        print(f"Tool execution result: {result}")
    except Exception as e:
        print(f"Tool execution error: {e}")

if __name__ == "__main__":
    asyncio.run(test_tool())