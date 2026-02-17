"""Tests for local email provider."""

import json
import tempfile
from pathlib import Path

from src.providers.local import LocalEmailProvider


def _write_sample(path: Path) -> None:
    data = [
        {
            "id": "e1", "thread_id": "t1", "from_addr": "a@b.com",
            "to_addr": "c@d.com", "subject": "Hello", "body": "Hi",
            "date": "2026-01-01T00:00:00Z", "is_read": False, "labels": [],
        },
        {
            "id": "e2", "thread_id": "t1", "from_addr": "c@d.com",
            "to_addr": "a@b.com", "subject": "Re: Hello", "body": "Hey",
            "date": "2026-01-01T01:00:00Z", "is_read": False, "labels": [],
        },
    ]
    path.write_text(json.dumps(data))


class TestLocalProvider:
    def test_list_emails(self, tmp_path):
        p = tmp_path / "emails.json"
        _write_sample(p)
        provider = LocalEmailProvider(p)
        emails = provider.list_emails()
        assert len(emails) == 2

    def test_get_email(self, tmp_path):
        p = tmp_path / "emails.json"
        _write_sample(p)
        provider = LocalEmailProvider(p)
        assert provider.get_email("e1") is not None
        assert provider.get_email("nope") is None

    def test_get_thread(self, tmp_path):
        p = tmp_path / "emails.json"
        _write_sample(p)
        provider = LocalEmailProvider(p)
        thread = provider.get_thread("t1")
        assert len(thread) == 2

    def test_mark_read(self, tmp_path):
        p = tmp_path / "emails.json"
        _write_sample(p)
        provider = LocalEmailProvider(p)
        provider.mark_read("e1")
        assert provider.get_email("e1").is_read is True

    def test_send_email(self, tmp_path):
        p = tmp_path / "emails.json"
        _write_sample(p)
        provider = LocalEmailProvider(p)
        email = provider.send_email("x@y.com", "Test", "Body")
        assert email.to_addr == "x@y.com"
        assert len(provider.list_emails()) == 3
