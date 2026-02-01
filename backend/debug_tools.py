"""
Debug script to check MCP tools and schema generation
"""
import inspect
from src.mcp.server import mcp_server

def debug_mcp_tools():
    print("=== MCP TOOLS DEBUG ===")
    print(f"Total registered tools: {len(mcp_server.tools)}")
    print("\nRegistered tools:")
    
    for name, func in mcp_server.tools.items():
        print(f"\nTool: {name}")
        print(f"  Function: {func}")
        print(f"  Docstring: {func.__doc__}")
        
        # Get function signature
        sig = inspect.signature(func)
        print(f"  Parameters: {sig}")
        
        # Generate schema like the agent does
        schema = {"type": "object", "properties": {}, "required": []}
        
        for param in sig.parameters.values():
            if param.default == inspect.Parameter.empty:
                schema["required"].append(param.name)
            # Determine type based on annotation
            param_type = "string"  # default
            if param.annotation != param.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == bool:
                    param_type = "boolean"
                # Add more type mappings as needed
            schema["properties"][param.name] = {"type": param_type}
        
        print(f"  Generated schema: {schema}")

if __name__ == "__main__":
    debug_mcp_tools()