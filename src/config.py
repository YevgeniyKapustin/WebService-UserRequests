from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    """App config."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.POSTGRES_URL: str = self.__get_postgres_dsn('async_fallback=True')

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_URL: str = None

    # CORS
    ORIGINS: list[str]

    def __get_postgres_dsn(self, query: str | None = None) -> str:
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=f'/{self.POSTGRES_DB}',
            query=query
        )

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
