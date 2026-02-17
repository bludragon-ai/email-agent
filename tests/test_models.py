"""Tests for domain models."""

from datetime import datetime

from src.models.email import Email, EmailAnalysis, EmailCategory, EmailPriority, DraftReply


def _make_email(**kw) -> Email:
    defaults = dict(
        id="e1", thread_id="t1", from_addr="a@b.com", to_addr="c@d.com",
        subject="Test", body="Hello", date=datetime(2026, 1, 1),
    )
    defaults.update(kw)
    return Email(**defaults)


class TestEmail:
    def test_create(self):
        e = _make_email()
        assert e.id == "e1"
        assert e.is_read is False

    def test_labels_default(self):
        e = _make_email()
        assert e.labels == []


class TestEmailAnalysis:
    def test_create(self):
        a = EmailAnalysis(
            email_id="e1",
            category=EmailCategory.URGENT,
            priority=EmailPriority.CRITICAL,
            summary="Server down",
            key_points=["DB offline"],
            suggested_action="Fix it",
            requires_reply=True,
        )
        assert a.category == EmailCategory.URGENT
        assert a.priority == 1


class TestDraftReply:
    def test_create(self):
        d = DraftReply(email_id="e1", subject="Re: Test", body="Hi", tone="friendly", confidence=0.9)
        assert d.confidence == 0.9
