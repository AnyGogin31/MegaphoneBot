from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)
from pydantic import Field


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DB_",
        case_sensitive=False
    )

    url: str = Field(alias="DATABASE_URL")
