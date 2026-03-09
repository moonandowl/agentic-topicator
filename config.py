"""Configuration from environment variables."""

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@lru_cache
def get_settings():
    return Settings()


class Settings:
    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY", "")
        self.xai_api_key = os.getenv("XAI_API_KEY", "")
        self.auth_username = os.getenv("AUTH_USERNAME", "")
        self.auth_password = os.getenv("AUTH_PASSWORD", "")
        # Model IDs (override via env if needed)
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.google_model = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
        self.anthropic_model = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-6")
        self.perplexity_model = os.getenv("PERPLEXITY_MODEL", "sonar-pro")
        self.grok_model = os.getenv("GROK_MODEL", "grok-4-fast-reasoning")

    @property
    def auth_enabled(self) -> bool:
        return bool(self.auth_username and self.auth_password)
