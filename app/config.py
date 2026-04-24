from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "sqlite:///./flowstate.db"
    secret_key: str = "change-me-to-a-long-random-string-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
