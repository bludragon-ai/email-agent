"""Email triage chain — categorize, score priority, summarize."""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from src.chains.llm import get_llm
from src.models.email import Email, EmailAnalysis

_SYSTEM = """\
You are an expert email triage assistant. Analyze the email and return JSON with these fields:
- category: one of "urgent", "client", "routine", "newsletter", "spam"
- priority: integer 1-5 (1=critical, 5=minimal)
- summary: one-sentence summary
- key_points: list of 2-4 key points
- suggested_action: brief recommended action
- requires_reply: boolean

Return ONLY valid JSON, no markdown fences."""

_HUMAN = """\
From: {from_addr}
To: {to_addr}
Subject: {subject}
Date: {date}

{body}"""

_prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _HUMAN)])
_parser = JsonOutputParser()


def triage_chain(email: Email) -> EmailAnalysis:
    """Run the triage chain on a single email."""
    chain = _prompt | get_llm() | _parser
    result = chain.invoke(
        {
            "from_addr": email.from_addr,
            "to_addr": email.to_addr,
            "subject": email.subject,
            "date": email.date.isoformat(),
            "body": email.body,
        }
    )
    return EmailAnalysis(email_id=email.id, **result)
