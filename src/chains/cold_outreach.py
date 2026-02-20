"""Cold outreach email generation chain."""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from src.chains.llm import get_llm
from src.models.email import ColdOutreachEmail


_SYSTEM = """\
You are an expert at writing cold outreach emails that get responses. Write a compelling, \
personalized cold email that:
- Opens with a genuine, specific hook (not generic flattery)
- Clearly states the value proposition in 1-2 sentences
- Has a low-friction call to action
- Reads naturally — NOT like a template
- Is appropriately brief (under 150 words for body)

Return JSON with:
- subject: a punchy, specific subject line (under 60 chars)
- body: the full email body (plain text, no placeholders like [Name])
- hook: one-sentence description of the opening hook used
- cta: the specific call-to-action used

Return ONLY valid JSON, no markdown fences."""

_HUMAN = """\
Target: {target}
Their company/context: {context}
My goal: {goal}
Sender name: {sender_name}
Tone: {tone}"""

_prompt = ChatPromptTemplate.from_messages([("system", _SYSTEM), ("human", _HUMAN)])
_parser = JsonOutputParser()


def cold_outreach_chain(
    target: str,
    context: str,
    goal: str,
    sender_name: str = "Alex",
    tone: str = "professional",
) -> ColdOutreachEmail:
    """Generate a cold outreach email."""
    chain = _prompt | get_llm() | _parser
    result = chain.invoke(
        {
            "target": target,
            "context": context,
            "goal": goal,
            "sender_name": sender_name,
            "tone": tone,
        }
    )
    return ColdOutreachEmail(
        target=target,
        goal=goal,
        tone=tone,
        **result,
    )
