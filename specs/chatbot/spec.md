# AI-Powered Todo Chatbot Specification

## Overview
An AI-powered chatbot that allows users to manage their todos through natural language interactions. The system uses Google's Gemini API to interpret user requests and executes corresponding actions via MCP (Model Context Protocol) tools.

## Architecture Components

### 1. State Management
- **Stateless Server**: The chat server maintains no in-memory state between requests
- **Database Persistence**: All conversation state is stored in the database
- **Context Reconstruction**: Conversation context is rebuilt from database on each request
- **Restart Resilience**: System survives restarts without losing context

### 2. AI Engine
- **Gemini API**: Uses Google's Gemini via official Python SDK
- **Per-Request Initialization**: Agent initialized per request with user context
- **User Context Injection**: Includes user_id, name, and email in agent context
- **MCP Integration**: Uses tool-calling to interact with MCP server

### 3. MCP Server
- **Official SDK**: Built using the official MCP SDK
- **Tool Exposure**: Exposes Todo operations as MCP tools
- **Stateless Operations**: Tools are stateless and persist data via database
- **Security**: Enforces user data isolation

## Database Models

### Task (Existing)
- Fields: user_id, id, title, description, completed, created_at, updated_at
- Note: This model already exists and should not be modified

### Conversation
- id (UUID, Primary Key)
- user_id (Foreign Key to User)
- created_at (Timestamp)
- updated_at (Timestamp)

### Message
- id (UUID, Primary Key)
- user_id (Foreign Key to User)
- conversation_id (Foreign Key to Conversation)
- role (user | assistant | system)
- content (Text)
- created_at (Timestamp)

## API Endpoints

### POST /api/users/{user_id}/chat
**Description**: Handles chat messages and returns AI responses

**Request Body**:
```json
{
  "conversation_id": "optional UUID string",
  "message": "string (required)"
}
```

**Response**:
```json
{
  "conversation_id": "UUID string",
  "response": "AI response text",
  "tool_calls": "array of MCP tools invoked"
}
```

### GET /api/users/{user_id}/conversations
**Description**: Retrieves all conversations for a user

**Response**:
```json
[
  {
    "id": "UUID string",
    "created_at": "ISO timestamp"
  }
]
```

### GET /api/users/{user_id}/conversations/{conversation_id}/messages
**Description**: Retrieves all messages in a conversation

**Response**:
```json
[
  {
    "id": "UUID string",
    "role": "user|assistant|system",
    "content": "message content",
    "created_at": "ISO timestamp"
  }
]
```

## MCP Tools Specification

### Tool: add_task
**Description**: Creates a new task for a user

**Parameters**:
- user_id (string): User identifier
- title (string): Task title
- description (optional string): Task description

**Returns**:
- task_id (string): Created task ID
- status (string): Operation status
- title (string): Task title

### Tool: list_tasks
**Description**: Lists tasks for a user

**Parameters**:
- user_id (string): User identifier
- status (string): "all" | "pending" | "completed"

**Returns**:
- Array of tasks with id, title, description, completed status

### Tool: complete_task
**Description**: Marks a task as complete

**Parameters**:
- user_id (string): User identifier
- task_id (integer): Task identifier

**Returns**:
- task_id (string): Task ID
- status (string): Operation status
- title (string): Task title

### Tool: delete_task
**Description**: Deletes a task

**Parameters**:
- user_id (string): User identifier
- task_id (integer): Task identifier

**Returns**:
- task_id (string): Task ID
- status (string): Operation status
- title (string): Task title

### Tool: update_task
**Description**: Updates a task

**Parameters**:
- user_id (string): User identifier
- task_id (integer): Task identifier
- title (optional string): New title
- description (optional string): New description

**Returns**:
- task_id (string): Task ID
- status (string): Operation status
- title (string): Task title

## Agent Behavior Specification

### Natural Language Processing
- **Add/Create/Remember**: Triggers `add_task` tool
- **List/Show/See**: Triggers `list_tasks` tool
- **Complete/Done/Finished**: Triggers `complete_task` tool
- **Delete/Remove**: Triggers `delete_task` tool
- **Update/Change/Rename**: Triggers `update_task` tool

### Response Handling
- Always confirms actions in friendly language
- Gracefully handles errors (task not found, invalid input)
- Provides clear, helpful responses based on tool results
- Asks for clarification when uncertain

## Stateless Request Flow

1. **Receive**: User message with conversation context
2. **Fetch**: Conversation and message history from database
3. **Build**: Agent input with system prompts, history, and new message
4. **Store**: User message in database
5. **Run**: Gemini agent processes the message
6. **Invoke**: Agent calls MCP tools as needed
7. **Persist**: Tool results are saved to database
8. **Store**: Assistant response in database
9. **Return**: Response to client

## Security Rules

- **User Isolation**: Agent can access only logged-in user's data
- **No Cross-Access**: No access to other users' data
- **Authentication**: Maintains existing authentication logic
- **Authorization**: Verifies user permissions for all operations

## Frontend Requirements

- **Protected Route**: Add `/chat` protected route
- **Chat UI**: Simple interface with conversation list and message display
- **API Reuse**: Reuse existing API client
- **No Auth Changes**: Maintain existing authentication flow