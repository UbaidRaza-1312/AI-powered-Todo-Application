from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import Mapped
from typing import List, Optional
from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = Field(default=True)
    email_verified: bool = Field(default=False)


class User(UserBase, table=True):
    __tablename__ = "user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, onupdate=datetime.utcnow, nullable=False)
    )

    # Relationships - temporarily commented out to fix authentication issues
    # tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)
    # conversations: List["Conversation"] = Relationship(back_populates="user")
    # messages: List["Message"] = Relationship(back_populates="user")


