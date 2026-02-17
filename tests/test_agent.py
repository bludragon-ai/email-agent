"""Tests for EmailAgent (no LLM calls)."""

import json
from pathlib import Path

from src.agents.email_agent import EmailAgent
from src.providers.local import LocalEmailProvider


def _setup(tmp_path: Path) -> EmailAgent:
    p = tmp_path / "emails.json"
    data = [
        {
            "id": "e1", "thread_id": "t1", "from_addr": "a@b.com",
            "to_addr": "c@d.com", "subject": "Test", "body": "Hi",
            "date": "2026-01-01T00:00:00Z", "is_read": False, "labels": [],
        },
    ]
    p.write_text(json.dumps(data))
    return EmailAgent(provider=LocalEmailProvider(p))


class TestEmailAgent:
    def test_inbox(self, tmp_path):
        agent = _setup(tmp_path)
        assert len(agent.inbox()) == 1

    def test_get_email(self, tmp_path):
        agent = _setup(tmp_path)
        assert agent.get_email("e1") is not None
        assert agent.get_email("nope") is None

    def test_mark_read(self, tmp_path):
        agent = _setup(tmp_path)
        agent.mark_read("e1")
        assert agent.get_email("e1").is_read is True
