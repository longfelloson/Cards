from typing import Annotated, Any, Literal, Union
from pydantic import AnyUrl, BeforeValidator, EmailStr, Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SMTP_HOST = "smtp.gmail.com"


def parse_cors(v: Any) -> Union[list[str], str]:
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


class SMTPConfig(BaseConfig):
    SMTP_PORT: int
    SMTP_HOST: str = DEFAULT_SMTP_HOST
    SMTP_PASSWORD: SecretStr
    SMTP_EMAIL: EmailStr


class DatabaseConfig(BaseConfig):
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


class AuthConfig(BaseConfig):
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str


class RedisConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="REDIS_")

    HOST: str
    PORT: int = 6379
    DB: int = 0
    PASSWORD: SecretStr

    @property
    def url(self):
        password = self.PASSWORD
        return f"redis://:{password}@{self.HOST}:{self.PORT}/{self.DB}"


class Settings(BaseConfig):
    smtp: SMTPConfig = Field(default_factory=SMTPConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)

    API_V1_PATH: str = "/api/v1"
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


settings = Settings()
