"""Abstract email provider interface — implement for Gmail, IMAP, etc."""

from __future__ import annotations

import abc
from typing import Optional

from src.models.email import Email


class EmailProvider(abc.ABC):
    """Pluggable email backend."""

    @abc.abstractmethod
    def list_emails(self, limit: int = 50, offset: int = 0) -> list[Email]:
        ...

    @abc.abstractmethod
    def get_email(self, email_id: str) -> Optional[Email]:
        ...

    @abc.abstractmethod
    def get_thread(self, thread_id: str) -> list[Email]:
        ...

    @abc.abstractmethod
    def mark_read(self, email_id: str) -> None:
        ...

    @abc.abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> Email:
        ...
