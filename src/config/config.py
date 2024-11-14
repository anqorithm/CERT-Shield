from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "CERT Shield API"
    environment: str = Field(..., env="ENVIRONMENT")
    mongo_db_uri: str = Field(..., env="MONGO_DB_URI")
    description: str = "An API for scraping and managing Saudi CERT security alerts."
    version: str = "1.0.0"
    mongo_db_name: str = Field(..., env="MONGO_DB_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
