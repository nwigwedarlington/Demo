from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "local"
    api_base_url: str = "http://localhost:8000"
    database_url: str = "postgresql+asyncpg://factcheck:factcheck@localhost:5432/factcheck"
    sync_database_url: str = "postgresql://factcheck:factcheck@localhost:5432/factcheck"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = Field(default="change-me-in-production")
    rate_limit_per_minute: int = 60

    ai_free_demo_mode: bool = True
    scraper_free_demo_mode: bool = True
    transcript_free_demo_mode: bool = True

    grok_api_key: str | None = None
    grok_base_url: str = "https://api.x.ai/v1"
    grok_model: str = "grok-3-mini"
    gemini_api_key: str | None = None
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    gemini_model: str = "gemini-2.5-flash"
    apify_api_token: str | None = None
    apify_facebook_comments_actor: str = "apify/facebook-comments-scraper"

    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
