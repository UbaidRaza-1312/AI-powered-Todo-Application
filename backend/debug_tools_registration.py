"""
Debug script to check how tools are being registered and passed to Gemini
"""
import asyncio
from src.agents.chat_agent import ChatAgent
from src.mcp.server import mcp_server

def debug_tools():
    print("=== DEBUGGING TOOLS REGISTRATION ===")
    
    print(f"Total tools registered in MCP server: {len(mcp_server.tools)}")
    print("Registered tools:")
    for name, func in mcp_server.tools.items():
        print(f"  - {name}: {func.__name__ if hasattr(func, '__name__') else type(func)}")
    
    # Test the get_mcp_tools function
    from src.agents.chat_agent import get_mcp_tools
    tools_schema = get_mcp_tools()
    
    print(f"\nTools schema generated for Gemini: {len(tools_schema)}")
    for tool in tools_schema:
        print(f"  - {tool['name']}")
        print(f"    Description: {tool['description'][:50]}...")
        print(f"    Parameters: {tool['parameters']}")
    
    # Create a chat agent to see the model configuration
    import os
    os.environ['GEMINI_API_KEY'] = 'dummy-key-for-debug'  # Set dummy key for debugging
    
    try:
        agent = ChatAgent()
        print(f"\nModel tools configured: {len(agent.model._tools) if hasattr(agent.model, '_tools') else 'Unknown'}")
    except Exception as e:
        print(f"Could not create agent for debugging: {e}")

if __name__ == "__main__":
    debug_tools()