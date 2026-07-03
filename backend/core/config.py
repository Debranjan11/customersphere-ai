from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# ----------------------------------------
# Application Settings
# ----------------------------------------

class AppSettings(BaseSettings):
    app_name: str = Field(..., alias="APP_NAME")
    app_version: str = Field(..., alias="APP_VERSION")
    debug: bool = Field(..., alias="DEBUG")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


# ----------------------------------------
# Database Settings
# ----------------------------------------

class DatabaseSettings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


# ----------------------------------------
# Security Settings
# ----------------------------------------

class SecuritySettings(BaseSettings):
    secret_key: str = Field(..., alias="SECRET_KEY")

    algorithm: str = Field(..., alias="ALGORITHM")

    access_token_expire_minutes: int = Field(
        ...,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


# ----------------------------------------
# Master Settings
# ----------------------------------------

class Settings:

    def __init__(self):

        self.app = AppSettings()

        self.database = DatabaseSettings()

        self.security = SecuritySettings()


@lru_cache
def get_settings():

    return Settings()


settings = get_settings()