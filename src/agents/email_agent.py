"""High-level Email Agent — orchestrates provider + AI chains."""

from __future__ import annotations

from typing import Optional

from src.models.email import Email, EmailAnalysis, DraftReply
from src.providers.base import EmailProvider
from src.chains.triage import triage_chain
from src.chains.reply import reply_chain
from src.chains.summarize import summarize_chain


class EmailAgent:
    """Facade that ties the email provider to AI capabilities."""

    def __init__(self, provider: EmailProvider) -> None:
        self.provider = provider
        self._analysis_cache: dict[str, EmailAnalysis] = {}

    # -- inbox -------------------------------------------------------------

    def inbox(self, limit: int = 50, offset: int = 0) -> list[Email]:
        return self.provider.list_emails(limit=limit, offset=offset)

    def get_email(self, email_id: str) -> Optional[Email]:
        return self.provider.get_email(email_id)

    def get_thread(self, thread_id: str) -> list[Email]:
        return self.provider.get_thread(thread_id)

    # -- AI features -------------------------------------------------------

    def analyze(self, email_id: str, force: bool = False) -> EmailAnalysis:
        """Triage/categorize a single email (cached)."""
        if not force and email_id in self._analysis_cache:
            return self._analysis_cache[email_id]
        email = self.provider.get_email(email_id)
        if not email:
            raise ValueError(f"Email {email_id} not found")
        analysis = triage_chain(email)
        self._analysis_cache[email_id] = analysis
        return analysis

    def draft_reply(
        self,
        email_id: str,
        tone: str = "professional",
        instructions: str = "",
    ) -> DraftReply:
        email = self.provider.get_email(email_id)
        if not email:
            raise ValueError(f"Email {email_id} not found")
        return reply_chain(email, tone=tone, instructions=instructions)

    def summarize_thread(self, thread_id: str) -> str:
        thread = self.provider.get_thread(thread_id)
        if not thread:
            raise ValueError(f"Thread {thread_id} not found")
        return summarize_chain(thread)

    def mark_read(self, email_id: str) -> None:
        self.provider.mark_read(email_id)
