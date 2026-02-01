"""
MCP Server for AI Chatbot with MCP Integration
Implements the Model Context Protocol server to handle tool requests from AI agents
"""
import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager


class MCPServer:
    def __init__(self):
        self.tools = {}
        
    def register_tool(self, name: str, handler):
        """Register an MCP tool with its handler function"""
        self.tools[name] = handler
        
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool with the given arguments"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")

        handler = self.tools[tool_name]
        try:
            result = await handler(**arguments)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Global MCP server instance
mcp_server = MCPServer()


# Register all tools when the module is loaded
from . import tool_registry
tool_registry.register_all_tools()


def create_app():
    """Create and configure the FastAPI app for the MCP server"""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        yield
        # Shutdown

    app = FastAPI(lifespan=lifespan, title="MCP Server for AI Chatbot", version="1.0.0")

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "tools_count": len(mcp_server.tools)}

    @app.post("/execute-tool")
    async def execute_tool(tool_name: str, arguments: Dict[str, Any]):
        result = await mcp_server.execute_tool(tool_name, arguments)
        return result

    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8001)