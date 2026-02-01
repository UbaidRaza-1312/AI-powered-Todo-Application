# API Contracts: AI Chatbot with MCP Integration

## Chat Endpoint

### POST /api/{user_id}/chat

**Description**: Main endpoint for chat interactions with the AI agent

**Path Parameters**:
- user_id (string, required): The ID of the authenticated user

**Request Body**:
```json
{
  "conversation_id": "string (optional)",
  "message": "string (required)"
}
```

**Headers**:
- Authorization: "Bearer {jwt_token}" (required)

**Response**:
```json
{
  "conversation_id": "string",
  "response": "string",
  "tool_calls": [
    {
      "tool_name": "string",
      "arguments": "object",
      "result": "object"
    }
  ]
}
```

**Success Response (200)**:
- Description: Chat message processed successfully
- Body: Contains AI response and any tool calls executed

**Error Responses**:
- 401: Unauthorized (invalid or missing JWT)
- 403: Forbidden (user_id in path doesn't match JWT)
- 404: Conversation not found (if specified conversation_id doesn't exist)
- 500: Internal server error

**Behavior**:
1. Validates JWT and ensures user_id matches token
2. If conversation_id not provided, creates new conversation
3. Fetches conversation history from database
4. Runs AI agent with message and context
5. Executes any MCP tool calls
6. Persists new messages to database
7. Returns AI response and tool call information

## MCP Tool Contracts

### add_task
**Description**: Creates a new task
**Input**: { title: string, description?: string }
**Output**: { task_id: string, success: boolean }

### list_tasks  
**Description**: Lists tasks for the user
**Input**: { status?: "all"|"pending"|"completed" }
**Output**: { tasks: Array<{id, title, description, completed, created_at, updated_at}> }

### update_task
**Description**: Updates an existing task
**Input**: { task_id: string, title?: string, description?: string, completed?: boolean }
**Output**: { success: boolean, updated_task?: object }

### complete_task
**Description**: Marks a task as complete
**Input**: { task_id: string }
**Output**: { success: boolean }

### delete_task
**Description**: Deletes a task
**Input**: { task_id: string }
**Output**: { success: boolean }