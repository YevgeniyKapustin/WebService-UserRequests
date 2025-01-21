import asyncio

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import Settings
from src.database import get_async_session
from src.main import app

CLEAN_TABLES = [
    'application',
]

test_settings = Settings(_env_file='./test/.env')

test_engine = create_async_engine(test_settings.POSTGRES_URL, future=True, echo=False)
async_session_maker = async_sessionmaker(test_engine, expire_on_commit=False)

@pytest.fixture(scope='function')
async def test_db_session():
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = test_db_session

@pytest.fixture(scope='function', autouse=True)
async def clean_tables(test_db_session):
    """Clean data in all tables before running test function."""
    async with test_db_session as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f'TRUNCATE TABLE {table_for_cleaning};'))


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
