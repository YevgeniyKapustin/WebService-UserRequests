from datetime import datetime, timezone
from aiokafka.structs import RecordMetadata

from src.applications.service import Application as ApplicationService


async def test_create_application(test_db_session):  
    application = ApplicationService('test_name', 'test_desc')
    result = await application.create(test_db_session)

    assert hasattr(result, 'id')
    assert hasattr(application, 'id')


async def test_publish_application():  
    application = ApplicationService(
        username='test_name',
        description='test_desc',
    )
    application.id = 1
    application.created_at = datetime.now(timezone.utc)

    result = await application.publish()

    assert isinstance(result, RecordMetadata)
    assert result.topic == 'applications'
