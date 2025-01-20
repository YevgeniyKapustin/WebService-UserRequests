from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
)

from applications.service import Application
from src.applications.models import Application as ApplicationModel

async def test_get_application(test_db_session):  
    for i in range(10):
        application = ApplicationModel(
            username=f'test_get_application_name',
            description=f'test_get_application_desc{i}',
        )
        test_db_session.add(application)
    await test_db_session.commit()

    searched_application = Application('test_get_application_name')

    applications = await searched_application.get(test_db_session)
    
    assert len(applications) == 10
