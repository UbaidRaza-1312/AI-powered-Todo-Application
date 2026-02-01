"""
Conversation model for AI Chatbot
Represents a conversation between a user and the AI assistant
"""
from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime


class ConversationBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="user.id")


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversation"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    )

    # Relationships temporarily commented out to fix authentication issues
    # user: "User" = Relationship(back_populates="conversations")
    # messages: List["Message"] = Relationship(back_populates="conversation")