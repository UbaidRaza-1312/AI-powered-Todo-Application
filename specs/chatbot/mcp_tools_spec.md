# MCP Tools Specification for AI Chatbot

## Overview
This document defines the Model Context Protocol (MCP) tools that enable the AI chatbot to interact with the todo management system. These tools provide a standardized interface for the AI agent to perform operations on user data.

## Tool Registration Process

All MCP tools are registered with the MCP server during application startup through the `tool_registry.py` module. Each tool follows a consistent pattern:

1. Define the tool function with proper type hints
2. Implement database operations using SQLModel/SQLAlchemy
3. Register the tool with the MCP server in the tool's module

## Tool Specifications

### 1. add_task

**Purpose**: Creates a new task for a user

**Function Signature**:
```python
async def add_task(user_id: str, title: str, description: str = None) -> Dict[str, Any]
```

**Parameters**:
- `user_id` (str): UUID string identifying the user
- `title` (str): Title of the task (required, 1-200 characters)
- `description` (str, optional): Detailed description of the task (up to 1000 characters)

**Return Value**:
```json
{
  "success": true,
  "task_id": "UUID string of created task",
  "message": "Success message"
}
```

**Implementation Details**:
- Validates input parameters
- Creates a new Task record with completed=False by default
- Persists to database using SQLModel session
- Returns success status and created task information

### 2. list_tasks

**Purpose**: Retrieves tasks for a user with optional filtering

**Function Signature**:
```python
async def list_tasks(user_id: str, status: str = "all") -> Dict[str, Any]
```

**Parameters**:
- `user_id` (str): UUID string identifying the user
- `status` (str, optional): Filter by completion status ("all", "pending", "completed")

**Return Value**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": "task UUID",
      "title": "task title",
      "description": "task description or null",
      "completed": true/false,
      "created_at": "ISO timestamp",
      "updated_at": "ISO timestamp"
    }
  ],
  "count": number of tasks returned
}
```

**Implementation Details**:
- Queries tasks filtered by user_id
- Applies status filter if specified
- Returns tasks in a structured format
- Handles empty results gracefully

### 3. complete_task

**Purpose**: Marks a task as completed

**Function Signature**:
```python
async def complete_task(user_id: str, task_id: int) -> Dict[str, Any]
```

**Parameters**:
- `user_id` (str): UUID string identifying the user
- `task_id` (int): ID of the task to complete

**Return Value**:
```json
{
  "success": true,
  "task_id": "ID of updated task",
  "message": "Confirmation message"
}
```

**Implementation Details**:
- Verifies task belongs to user
- Updates the completed field to True
- Returns confirmation of the operation
- Handles cases where task doesn't exist

### 4. delete_task

**Purpose**: Removes a task from the user's list

**Function Signature**:
```python
async def delete_task(user_id: str, task_id: int) -> Dict[str, Any]
```

**Parameters**:
- `user_id` (str): UUID string identifying the user
- `task_id` (int): ID of the task to delete

**Return Value**:
```json
{
  "success": true,
  "task_id": "ID of deleted task",
  "message": "Confirmation message"
}
```

**Implementation Details**:
- Verifies task belongs to user
- Performs soft or hard delete based on requirements
- Returns confirmation of deletion
- Handles cases where task doesn't exist

### 5. update_task

**Purpose**: Modifies properties of an existing task

**Function Signature**:
```python
async def update_task(user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]
```

**Parameters**:
- `user_id` (str): UUID string identifying the user
- `task_id` (int): ID of the task to update
- `title` (str, optional): New title for the task
- `description` (str, optional): New description for the task

**Return Value**:
```json
{
  "success": true,
  "task_id": "ID of updated task",
  "message": "Confirmation message"
}
```

**Implementation Details**:
- Verifies task belongs to user
- Updates only provided fields (partial update)
- Returns confirmation of the update
- Handles cases where task doesn't exist

## Error Handling

Each tool implements comprehensive error handling:

- **Validation Errors**: Invalid input parameters are caught and reported
- **Authorization Errors**: Attempts to access another user's data are prevented
- **Resource Not Found**: Missing tasks/users return appropriate error messages
- **Database Errors**: Connection issues and constraint violations are handled gracefully

## Security Considerations

- **User Isolation**: Each tool verifies that operations are performed on the correct user's data
- **Input Sanitization**: All inputs are validated before database operations
- **Access Control**: Tools enforce that users can only modify their own data
- **Audit Trail**: Operations may be logged for security monitoring

## Performance Considerations

- **Async Operations**: All tools use async/await for database operations
- **Connection Pooling**: Uses SQLModel's session management for efficiency
- **Indexing**: Database queries leverage existing indexes on user_id and task_id
- **Batch Operations**: Where applicable, tools minimize database round trips