from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
import uuid
from datetime import datetime
from sqlmodel import select

from ..db.database import get_async_session
from ..models.conversation import Conversation
from ..models.message import Message, MessageRole
from ..middleware.auth_middleware import get_current_user_id
from ..agents.chat_agent import ChatAgent

router = APIRouter()

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[dict]

@router.post("/users/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: UUID,
    chat_request: ChatRequest,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Handle chat messages and return AI responses"""
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this chat"
        )

    # Get or create conversation
    conversation_id = chat_request.conversation_id
    if conversation_id:
        try:
            conv_uuid = uuid.UUID(conversation_id)
            conversation = await session.get(Conversation, conv_uuid)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )
    else:
        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        conversation_id = str(conversation.id)

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


    # Process with AI agent
    agent = ChatAgent()
    result = await agent.process_message(str(user_id), chat_request.message, conversation_id)



    return ChatResponse(
        conversation_id=conversation_id,
        response=result["response"],
        tool_calls=result.get("tool_calls", [])
    )

class ConversationListResponse(BaseModel):
    id: str
    created_at: str

@router.get("/users/{user_id}/conversations", response_model=List[ConversationListResponse])
async def get_conversations(
    user_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get all conversations for a user"""
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these conversations"
        )

    statement = select(Conversation).where(Conversation.user_id == user_id)
    result = await session.execute(statement)
    conversations = result.scalars().all()

    return [
        ConversationListResponse(
            id=str(conv.id),
            created_at=conv.created_at.isoformat()
        ) for conv in conversations
    ]

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: str

@router.get("/users/{user_id}/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    user_id: UUID,
    conversation_id: str,
    current_user_id: UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """Get all messages in a conversation"""
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these messages"
        )

    try:
        conv_uuid = uuid.UUID(conversation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )

    # Verify conversation belongs to user
    conversation = await session.get(Conversation, conv_uuid)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    statement = select(Message).where(
        Message.conversation_id == conv_uuid
    ).order_by(Message.created_at.asc())
    result = await session.execute(statement)
    messages = result.scalars().all()

    return [
        MessageResponse(
            id=str(msg.id),
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at.isoformat()
        ) for msg in messages
    ]