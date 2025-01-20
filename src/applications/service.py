from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from aiokafka.structs import RecordMetadata

from src.applications.schemas import ApplicationSchema
from src.kafka.producer import KafkaProducer
from src.applications.models import Application as ApplicationModel
from src.utils.database_paginations import paginate_query


class Application(object):
    __slots__ = ('username', 'description', 'id', 'created_at')

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
            logger.debug(f'Finded applications count: {len(applications)}')
            return applications
        logger.debug(f'Applications not found')
        return None


    async def create(self, session) -> bool:
        """Create application."""
        if self.username and self.description:
            logger.debug(f'Create application by user {self.username}...')
            application = ApplicationModel(
                username=self.username,
                description=self.description,
            )
            session.add(application)

            await session.commit()
            logger.debug('The session was committed.')

            self.id = application.id
            self.created_at = application.created_at
            await self.publish()

            logger.debug(f'Application by user {self.username} created.')
            return True
        logger.debug(
            f'''Some data is missing to create the application:
            user_name: {self.username}
            description: {self.description}
            '''
        )
        return False
    
    async def publish(self) -> RecordMetadata:
        topik = 'applications'
        message: dict[str] = ApplicationSchema(
            id=self.id,
            username=self.username,
            description=self.description,
            created_at=self.created_at.isoformat(timespec="minutes")
        ).model_dump_json()
        logger.info(f'Publish message: {topik}: "{message}"')
        return await KafkaProducer.send_message(topik, message)
