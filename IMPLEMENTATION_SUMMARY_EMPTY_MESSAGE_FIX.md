# Fix for Empty Message Handling in Chatbot

## Problem
When users sent empty messages to the chatbot (like pressing enter without typing anything), the system was not handling them properly. Instead of returning a meaningful response, the chatbot was likely showing a timestamp or behaving unexpectedly.

## Solution
Implemented empty message detection and handling at two levels:

### 1. API Route Level (`src/api/chat_routes.py`)
Added validation in the `/users/{user_id}/chat` endpoint to detect empty messages before they reach the AI agent:

```python
# Check if message is empty before storing
if not chat_request.message or not chat_request.message.strip():
    # Store empty user message
    user_message = Message(
        user_id=user_id,
        conversation_id=uuid.UUID(conversation_id),
        role=MessageRole.user,
        content=chat_request.message or ""
    )
    session.add(user_message)
    await session.commit()

    # Return appropriate response for empty message
    empty_response = "I didn't receive any message. Please send a message to continue our conversation."
    
    # Store assistant message
    assistant_message = Message(
        user_id=user_id,
        conversation_id=uuid.UUID(conversation_id),
        role=MessageRole.assistant,
        content=empty_response
    )
    session.add(assistant_message)
    await session.commit()

    return ChatResponse(
        conversation_id=conversation_id,
        response=empty_response,
        tool_calls=[]
    )
```

### 2. Agent Level (`src/agents/chat_agent.py`)
Added similar validation in the `process_message` method of the `ChatAgent` class as a backup measure:

```python
# Handle empty message case
if not message or not message.strip():
    # Save empty user message
    async with session_maker() as session:
        session.add(
            Message(
                id=uuid.uuid4(),
                user_id=uuid.UUID(user_id),
                conversation_id=uuid.UUID(conversation_id),
                role="user",
                content=message or "",
            )
        )
        await session.commit()

    # Return appropriate response for empty message
    empty_response = "I didn't receive any message. Please send a message to continue our conversation."
    
    # Save assistant response
    async with session_maker() as session:
        session.add(
            Message(
                id=uuid.uuid4(),
                user_id=uuid.UUID(user_id),
                conversation_id=uuid.UUID(conversation_id),
                role="assistant",
                content=empty_response,
            )
        )
        await session.commit()

    return {
        "response": empty_response,
        "tool_calls": [],
    }
```

## Result
Now when users send empty messages (empty string, whitespace-only, or null), the chatbot responds with:
"I didn't receive any message. Please send a message to continue our conversation."

This provides a clear, helpful response instead of showing timestamps or other unexpected behavior.

## Files Modified
1. `src/api/chat_routes.py` - Added empty message validation in the chat endpoint
2. `src/agents/chat_agent.py` - Added empty message validation in the agent's process_message method