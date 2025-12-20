from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ADMIN_TOKEN: str

    # Kafka
    #kafka_bootstrap_servers: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow"
    }


settings = Settings()
