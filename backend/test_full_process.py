"""
Test the full chat agent process
"""
import asyncio
from src.mcp.server import mcp_server

async def test_full_process():
    print("=== TESTING FULL PROCESS ===")
    
    # Simulate what happens in the chat agent
    fn = "delete_task_by_reference"
    args = {
        "task_reference": "task2",
        "user_id": "5807fcba-83e4-4328-b0ea-6c851ea2db99"
    }
    
    print(f"Calling tool: {fn} with args: {args}")
    
    result = await mcp_server.execute_tool(fn, args)
    print(f"MCP server result: {result}")
    
    # Simulate the chat agent's response processing
    tool_calls = []
    tool_calls.append(result)
    
    if result["success"]:
        final_text = result["result"].get(
            "message", "✅ Action completed successfully"
        )
    else:
        final_text = result.get("error", "❌ Action failed")
    
    print(f"Final text to user: {final_text}")

if __name__ == "__main__":
    asyncio.run(test_full_process())