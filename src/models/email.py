"""Core email domain models."""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EmailCategory(str, enum.Enum):
    URGENT = "urgent"
    CLIENT = "client"
    ROUTINE = "routine"
    NEWSLETTER = "newsletter"
    SPAM = "spam"


class EmailPriority(int, enum.Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    MINIMAL = 5


class Email(BaseModel):
    """A single email message."""

    id: str
    thread_id: str
    from_addr: str
    to_addr: str
    subject: str
    body: str
    date: datetime
    is_read: bool = False
    labels: list[str] = Field(default_factory=list)


class EmailAnalysis(BaseModel):
    """AI-generated analysis of an email."""

    email_id: str
    category: EmailCategory
    priority: EmailPriority
    summary: str
    key_points: list[str] = Field(default_factory=list)
    suggested_action: str = ""
    requires_reply: bool = False


class DraftReply(BaseModel):
    """AI-generated draft reply."""

    email_id: str
    subject: str
    body: str
    tone: str = "professional"
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
