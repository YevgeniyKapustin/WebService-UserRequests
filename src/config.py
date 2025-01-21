from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class Settings(BaseSettings):
    """App settings."""
    model_config = SettingsConfigDict(extra='ignore')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.POSTGRES_URL = self.__get_postgres_dsn()

    # APP
    APP_TITLE: str
    DEV_MODE: bool
    ORIGINS: list[str]

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URL: str = ''

    # Kafka
    KAFKA_PRODUCER_HOST: str

    def __get_postgres_dsn(self, query: str | None = None) -> str:
        return str(PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
            query=query
        ))



settings = Settings()
