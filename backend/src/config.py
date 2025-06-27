from typing import Literal
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseSettings):
    DB_PORT: int
    DB_HOST: str
    DB_NAME: str
    DB_PASSWORD: SecretStr
    DB_USER: str

    @property
    def db_url(self):
        DB_PASSWORD = self.DB_PASSWORD.get_secret_value()
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class AuthConfig(BaseSettings):
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str


class Settings(
    AuthConfig,
    DatabaseConfig,
):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    MODE: Literal["DEV", "TEST"]


settings = Settings()
