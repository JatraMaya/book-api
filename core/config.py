from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    debug: bool = False
    api_title: str
    allowed_hosts: str = ""
    admin_email: str
    admin_password: str
    api_version: str

    @field_validator("allowed_hosts")
    def parse_hosts(cls, v: str) -> list[str]:
        return v.split(",") if v else []

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
