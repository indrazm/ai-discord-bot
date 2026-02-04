from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DISCORD_TOKEN: str
    MONITORED_CHANNEL_ID: str
    OPENAI_API_KEY: str

    TAVILY_API_KEY: str = ""

    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = ""

    DATABASE_PATH: str = "./data/discord_ai.db"
    DATABASE_ECHO: bool = False

    CREATOR_ID: str = ""
    CREATOR_USERNAME: str = ""

    LLM_MODEL: str = "openrouter/openai/gpt-5.1-codex-mini"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings() # type: ignore
