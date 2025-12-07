from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ADMIN_TOKEN: str = "changeme"

    class Config:
        env_file = ".env"

settings = Settings()
#для коммита