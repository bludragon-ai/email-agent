"""LLM factory — returns a LangChain chat model based on configuration."""

from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel

from src.utils.config import LLMProvider, get_settings


def get_llm() -> BaseChatModel:
    """Instantiate the configured LLM provider.

    Returns:
        A LangChain-compatible chat model ready for chain composition.

    Raises:
        ValueError: If the API key for the selected provider is missing.
    """
    settings = get_settings()

    if settings.llm_provider == LLMProvider.ANTHROPIC:
        if not settings.anthropic_api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic"
            )
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=settings.resolved_model,
            anthropic_api_key=settings.anthropic_api_key,
            temperature=settings.temperature,
            max_tokens=2048,
        )

    if settings.llm_provider == LLMProvider.OPENAI:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=settings.resolved_model,
            api_key=settings.openai_api_key,
            temperature=settings.temperature,
            max_tokens=2048,
        )

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
