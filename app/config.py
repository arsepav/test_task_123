from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str = "tmp-api-key"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/organizations_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
