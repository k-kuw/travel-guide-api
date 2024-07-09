from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# 環境変数呼び出し
class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    browser_url: str
    sqlalchemy_database_url: str

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()

# 環境変数情報
settings = get_settings()
