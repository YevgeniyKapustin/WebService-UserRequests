"""Collecting metadata and creating a session."""
from typing import AsyncGenerator
from venv import logger

from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
)
from sqlalchemy.orm import as_declarative, declared_attr, Mapped, mapped_column
from sqlalchemy.pool import NullPool

from src.config import settings
from src.utils.database_types import type_annotation_map 


@as_declarative()
class Base:
    __name__: str
    id: Mapped[int] = mapped_column(primary_key=True)

    type_annotation_map = type_annotation_map

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


engine: AsyncEngine = create_async_engine(
    settings.POSTGRES_URL, poolclass=NullPool
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        logger.debug('yield session...')
        yield session
    logger.debug('close session...')
