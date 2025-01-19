from pydantic_settings import BaseSettings
from pydantic import ConfigDict, PostgresDsn

class Settings(BaseSettings):
    """App config."""
    model_config = ConfigDict(extra='ignore')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.POSTGRES_URL = str(self.__get_postgres_dsn('async_fallback=True'))

    # APP
    ORIGINS: list[str]

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URL: str | None = None

    # Kafka
    KAFKA_HOST: str

    def __get_postgres_dsn(self, query: str | None = None) -> str:
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
            query=query
        )



settings = Settings()
