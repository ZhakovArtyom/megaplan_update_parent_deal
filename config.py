from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс Settings подгружает данные из файла .env."""

    MP30224613_TOKEN: str
    MP30224613_API_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
