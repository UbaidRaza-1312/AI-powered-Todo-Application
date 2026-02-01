"""
Message model for AI Chatbot
Represents a message in a conversation between a user and the AI assistant
"""
from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime
from enum import Enum
from sqlalchemy import Enum as SQLEnum


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class MessageBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    role: MessageRole = Field(sa_column=Column(SQLEnum(MessageRole), nullable=False))
    content: str


class Message(MessageBase, table=True):
    __tablename__ = "message"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False)
    )

    # Relationships temporarily commented out to fix authentication issues
    # user: "User" = Relationship(back_populates="messages")
    # conversation: "Conversation" = Relationship(back_populates="messages")