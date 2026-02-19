"""LLM factory — returns Anthropic or OpenAI chat model based on config."""

from __future__ import annotations

import os
from functools import lru_cache

from langchain_core.language_models import BaseChatModel


@lru_cache(maxsize=1)
def get_llm() -> BaseChatModel:
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        kwargs = dict(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=temperature,
        )
        base_url = os.getenv("OPENAI_BASE_URL", "")
        if base_url:
            kwargs["base_url"] = base_url
        return ChatOpenAI(**kwargs)

    # default: anthropic
    from langchain_anthropic import ChatAnthropic

    return ChatAnthropic(
        model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
        temperature=temperature,
    )
