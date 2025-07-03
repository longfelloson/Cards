from pydantic import EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SMTP_HOST = "smtp.gmail.com"


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


class Settings(BaseConfig):
    smtp: SMTPConfig = Field(default_factory=SMTPConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)

    DOMAIN: str
    VERIFICATION_PATH: str

    @property
    def verification_url(self) -> str:
        # 127.0.0.1 + /verification
        return self.DOMAIN + self.VERIFICATION_PATH


settings = Settings()
