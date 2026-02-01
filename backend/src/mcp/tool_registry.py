"""
Tool Registry for MCP Server
Registers all MCP tools with the server
"""

def register_all_tools():
    """Register all MCP tools with the server"""
    # Import and register all tools
    from .tools.add_task import register_tool as register_add_task
    from .tools.list_tasks import register_tool as register_list_tasks
    from .tools.get_task import register_tool as register_get_task
    from .tools.update_task import register_tool as register_update_task
    from .tools.complete_task import register_tool as register_complete_task
    from .tools.delete_task import register_tool as register_delete_task
    from .tools.delete_task_by_reference import register_tool as register_delete_task_by_reference

    # Register each tool
    register_add_task()
    register_list_tasks()
    register_get_task()
    register_update_task()
    register_complete_task()
    register_delete_task()
    register_delete_task_by_reference()