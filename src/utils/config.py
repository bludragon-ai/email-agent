"""App configuration loaded from environment."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "anthropic")
APP_TITLE: str = os.getenv("APP_TITLE", "📧 Email Agent")
