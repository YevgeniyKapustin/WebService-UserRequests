from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from paginate_sqlalchemy import SqlalchemyOrmPage

from src.applications.models import Application as ApplicationModel

class Application(object):
    __slots__ = ('user_name',)

    def __init__(self, user_name: str | None = None):
        self.user_name = user_name

    async def get(
            self, 
            session: AsyncSession, 
            page: int | None = None, 
            size: int | None = None
        ) -> list[ApplicationModel]:
        """Get applications."""
        query = (
            select(ApplicationModel)
            .filter(ApplicationModel.user_name == self.user_name)

            if self.user_name else

            select(ApplicationModel)
        )

        if page and size:
            query = SqlalchemyOrmPage(query, page=page, items_per_page=size)

        result = await session.execute(query)
    
        if applications := await list(result.scalars().all()):
            logger.debug(f'Finded applications: {[i.request for i in applications]}')
            return applications
        logger.info(f'Applications not found')
        return None
