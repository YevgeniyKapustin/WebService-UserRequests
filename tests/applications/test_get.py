from applications.service import Application
from src.applications.models import Application as ApplicationModel

async def test_get_application(test_db_session):  
    for i in range(10):
        application = ApplicationModel(
            username=f'test_name',
            description=f'test_desc{i}',
        )
        test_db_session.add(application)
    await test_db_session.commit()

    searched_application = Application()
    applications = await searched_application.get(test_db_session)
    assert len(applications) == 10

async def test_get_with_pagination_application(test_db_session):  
    for i in range(10):
        application = ApplicationModel(
            username=f'test_name',
            description=f'test_desc{i}',
        )
        test_db_session.add(application)
    await test_db_session.commit()

    searched_application = Application('test_name')
    applications = await searched_application.get(test_db_session, page=3, size=4)
    assert len(applications) == 2


async def test_get_with_size_application(test_db_session):  
    for i in range(10):
        application = ApplicationModel(
            username=f'test_name',
            description=f'test_desc{i}',
        )
        test_db_session.add(application)
    await test_db_session.commit()

    searched_application = Application('test_name')
    applications = await searched_application.get(test_db_session, size=4)
    assert len(applications) == 4


async def test_get_with_page_application(test_db_session):  
    for i in range(10):
        application = ApplicationModel(
            username=f'test_name',
            description=f'test_desc{i}',
        )
        test_db_session.add(application)
    await test_db_session.commit()

    searched_application = Application('test_name')
    applications = await searched_application.get(test_db_session, page=2)
    assert len(applications) == 10
