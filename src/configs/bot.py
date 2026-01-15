from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)
from pydantic import (
    Field,
    SecretStr
)


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BOT_",
        case_sensitive=False
    )

    token: SecretStr = Field(alias="BOT_TOKEN")
