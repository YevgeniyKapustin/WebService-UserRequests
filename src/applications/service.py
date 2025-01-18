from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.applications.models import Application as ApplicationModel
from src.utils.database_paginations import paginate_query


class Application(object):
    __slots__ = ('username', 'description')

    def __init__(
            self, 
            username: str | None = None, 
            description: str | None = None
        ):
        self.username = username
        self.description = description

    async def get(
            self, 
            session: AsyncSession, 
            page: int | None = None, 
            size: int | None = None
        ) -> list[ApplicationModel]:
        """Get applications."""
        query = select(ApplicationModel)

        if self.username:
            query = query.filter(ApplicationModel.username == self.username)

        query = paginate_query(query, page, size)

        result = await session.execute(query)
    
        if applications := list(result.scalars().all()):
            logger.debug(f'Finded applications: {len(applications)}')
            return applications
        logger.debug(f'Applications not found')
        return None


    async def create(self, session) -> bool:
        """Create application."""
        if self.username and self.description:
            logger.debug(f'Create application by user {self.username}...')
            session.add(
                ApplicationModel(
                    username=self.username,
                    description=self.description,
                )
            )
            await session.commit()
            logger.debug(f'The session was committed.')
            logger.debug(f'Application by user {self.username} created.')
            return True
        logger.debug(
            f'''Some data is missing to create the application:
            user_name: {self.username}
            description: {self.description}
            '''
        )
        return False
    