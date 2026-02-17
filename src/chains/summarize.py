"""Thread summarization chain."""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.chains.llm import get_llm
from src.models.email import Email

_SYSTEM = """\
You are an expert at summarizing email threads. Provide a concise summary that captures:
- The main topic and context
- Key decisions or action items
- Current status / what's pending

Keep it under 200 words."""

_HUMAN = """\
Email thread ({count} messages):

{thread_text}"""

_prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _HUMAN)])


def summarize_chain(thread: list[Email]) -> str:
    """Summarize an email thread."""
    thread_text = "\n---\n".join(
        f"From: {e.from_addr}\nDate: {e.date.isoformat()}\nSubject: {e.subject}\n\n{e.body}"
        for e in sorted(thread, key=lambda e: e.date)
    )
    chain = _prompt | get_llm() | StrOutputParser()
    return chain.invoke({"count": len(thread), "thread_text": thread_text})
