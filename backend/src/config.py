from enum import StrEnum
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, EmailStr, Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

SMTP_DEFAULT_HOST = "smtp.gmail.com"
LOGGING_DEFAULT_FILENAME = "logs.log"
REDIS_DEFAULT_PREFIX = "cache"


class LoggingLevel(StrEnum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"
    CRITICAL = "CRITICAL"


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_ignore_empty=True,
        extra="ignore",
    )


class LoggingConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="LOGGING_")

    FILENAME: str = LOGGING_DEFAULT_FILENAME
    LEVEL: LoggingLevel = LoggingLevel.WARNING


class SMTPConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="SMTP_")

    PORT: int
    HOST: str = SMTP_DEFAULT_HOST
    PASSWORD: SecretStr
    EMAIL: EmailStr
    
    @property
    def send_email_kwargs(self) -> dict:
        return {
            "hostname": self.HOST,
            "port": self.PORT,
            "start_tls": True,
            "username": self.EMAIL,
            "password": self.PASSWORD.get_secret_value()
        }


class DatabaseConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="DB_")

    PORT: int
    HOST: str
    NAME: str
    PASSWORD: SecretStr
    USER: str

    @property
    def url(self) -> str:
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.USER,
            self.PASSWORD.get_secret_value(),
            self.HOST,
            self.PORT,
            self.NAME,
        )


class AuthConfig(BaseConfig):
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str


class RedisConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    HOST: str
    PORT: int = 6379
    DB: int = 0
    PASSWORD: SecretStr
    DB_PREFIX: str = REDIS_DEFAULT_PREFIX

    @property
    def url(self):
        return "redis://:{}@{}:{}/{}".format(
            self.PASSWORD.get_secret_value(),
            self.HOST,
            self.PORT,
            self.DB,
        )


class Settings(BaseConfig):
    smtp: SMTPConfig = Field(default_factory=SMTPConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    API_VERSION: int | float

    DOMAIN: str
    VERIFICATION_PATH: str
    FRONTEND_HOST: str = "http://localhost:5173"
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    @property
    def verification_url(self) -> str:
        # 127.0.0.1 + /verification
        return self.DOMAIN + self.VERIFICATION_PATH

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        cors = [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS]
        return cors + [self.FRONTEND_HOST]

    @property
    def api_prefix(self) -> str:
        return f"/api/v{self.API_VERSION}"


settings = Settings()
