"""Local JSON-file email provider for demo / development."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.models.email import Email
from src.providers.base import EmailProvider

_DEFAULT_DATA = Path(__file__).resolve().parent.parent.parent / "data" / "sample_emails.json"


class LocalEmailProvider(EmailProvider):
    """Reads/writes emails from a local JSON file."""

    def __init__(self, path: Path | str | None = None) -> None:
        self._path = Path(path) if path else _DEFAULT_DATA
        self._emails: list[Email] = []
        self._load()

    # -- public interface --------------------------------------------------

    def list_emails(self, limit: int = 50, offset: int = 0) -> list[Email]:
        sorted_emails = sorted(self._emails, key=lambda e: e.date, reverse=True)
        return sorted_emails[offset : offset + limit]

    def get_email(self, email_id: str) -> Optional[Email]:
        return next((e for e in self._emails if e.id == email_id), None)

    def get_thread(self, thread_id: str) -> list[Email]:
        thread = [e for e in self._emails if e.thread_id == thread_id]
        return sorted(thread, key=lambda e: e.date)

    def mark_read(self, email_id: str) -> None:
        email = self.get_email(email_id)
        if email:
            email.is_read = True
            self._save()

    def send_email(self, to: str, subject: str, body: str) -> Email:
        email = Email(
            id=str(uuid.uuid4())[:8],
            thread_id=str(uuid.uuid4())[:8],
            from_addr="you@example.com",
            to_addr=to,
            subject=subject,
            body=body,
            date=datetime.now(timezone.utc),
            is_read=True,
            labels=["sent"],
        )
        self._emails.append(email)
        self._save()
        return email

    # -- internals ---------------------------------------------------------

    def _load(self) -> None:
        if self._path.exists():
            raw = json.loads(self._path.read_text())
            self._emails = [Email(**e) for e in raw]

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = [e.model_dump(mode="json") for e in self._emails]
        self._path.write_text(json.dumps(data, indent=2, default=str))
