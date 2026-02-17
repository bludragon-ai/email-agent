"""Smart reply drafting chain."""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from src.chains.llm import get_llm
from src.models.email import Email, DraftReply

_SYSTEM = """\
You are an expert email writer. Draft a reply to the email below.
Tone: {tone}

Return JSON with:
- subject: reply subject line
- body: the full reply body (plain text, no greeting/signature placeholders)
- confidence: float 0-1 indicating how confident you are this reply is appropriate

Return ONLY valid JSON, no markdown fences."""

_HUMAN = """\
Original email:
From: {from_addr}
Subject: {subject}
Date: {date}

{body}

{instructions}"""

_prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _HUMAN)])
_parser = JsonOutputParser()


def reply_chain(
    email: Email,
    tone: str = "professional",
    instructions: str = "",
) -> DraftReply:
    """Generate a draft reply."""
    chain = _prompt | get_llm() | _parser
    result = chain.invoke(
        {
            "tone": tone,
            "from_addr": email.from_addr,
            "subject": email.subject,
            "date": email.date.isoformat(),
            "body": email.body,
            "instructions": instructions or "Reply appropriately.",
        }
    )
    return DraftReply(email_id=email.id, tone=tone, **result)
