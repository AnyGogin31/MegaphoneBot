from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)
from pydantic import (
    Field,
    SecretStr
)

class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="API_",
        case_sensitive=False
    )

    id: SecretStr = Field(alias="API_ID")
    hash: SecretStr = Field(alias="API_HASH")
