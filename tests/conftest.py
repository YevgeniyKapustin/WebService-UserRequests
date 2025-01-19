import asyncio
from functools import wraps
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
)
from sqlalchemy.pool import NullPool

from src.config import Settings
from src.database import get_async_session, Base
from src.main import app

# устанавливаем .env для тестов
test_settings = Settings(_env_file='./test/.env')
# создаем тестовые движок и создатель сессий на нем
test_engin: AsyncEngine = create_async_engine(
    test_settings.POSTGRES_URL, poolclass=NullPool
)
async_session_maker = async_sessionmaker(test_engin, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# переписываем зависимость сессии, чтобы использовался наш создатель сессии
app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    """Создает таблицы при прогоне тестов и удаляет при завершении."""
    async with test_engin.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engin.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(scope='session',)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
