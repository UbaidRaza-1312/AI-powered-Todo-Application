# Data Model: AI Chatbot with MCP Integration

## Entity: Task
**Description**: Represents a user's todo item

**Fields**:
- id: UUID (Primary Key, auto-generated)
- user_id: UUID (Foreign Key to user, indexed)
- title: String (max 255 chars, required)
- description: Text (optional)
- completed: Boolean (default: false)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated, updates on change)

**Validation Rules**:
- user_id must match authenticated user
- title cannot be empty
- completed defaults to false

**State Transitions**:
- pending → completed (via complete_task tool)
- completed → pending (via update_task tool)

## Entity: Conversation
**Description**: Represents a chat session between user and AI

**Fields**:
- id: UUID (Primary Key, auto-generated)
- user_id: UUID (Foreign Key to user, indexed)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated, updates on change)

**Validation Rules**:
- user_id must match authenticated user

## Entity: Message
**Description**: Represents individual chat messages in a conversation

**Fields**:
- id: UUID (Primary Key, auto-generated)
- user_id: UUID (Foreign Key to user, indexed)
- conversation_id: UUID (Foreign Key to conversation, indexed)
- role: String (enum: "user", "assistant", required)
- content: Text (required)
- created_at: DateTime (auto-generated)

**Validation Rules**:
- user_id must match authenticated user
- conversation_id must exist and belong to user
- role must be either "user" or "assistant"
- content cannot be empty

## Relationships:
- User (1) → Conversations (Many)
- User (1) → Tasks (Many)
- User (1) → Messages (Many)
- Conversation (1) → Messages (Many)
- Task (belongs to) → User (1)
- Message (belongs to) → Conversation (1)