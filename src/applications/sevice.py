from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from paginate_sqlalchemy import SqlalchemyOrmPage

from src.applications.models import Application as ApplicationModel


class Application(object):
    __slots__ = ('user_name', 'description')

    def __init__(
            self, 
            user_name: str | None = None, 
            description: str | None = None
        ):
        self.user_name = user_name
        self.description = description

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
        logger.debug(f'Applications not found')
        return None


    async def create(self, session) -> bool:
        """Create application."""
        if self.user_name and self.description:
            logger.debug(f'Create application by user {self.user_name}...')
            session.add(
                ApplicationModel(
                    user_name=self.user_name,
                    description=self.description,
                )
            )
            await session.commit()
            logger.debug(f'The session was committed.')
            logger.debug(f'Application by user {self.user_name} created.')
            return True
        logger.debug(
            f'''Some data is missing to create the application:
            user_name: {self.user_name}
            description: {self.description}
            '''
        )
        return False
    