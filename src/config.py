from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

class Settings(BaseSettings):
    """App config."""
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

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
