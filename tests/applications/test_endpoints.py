# """Интеграционные тесты для applications."""
# from fastapi import Depends

# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette.status import (
#     HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
# )

# from src.applications.models import Application as ApplicationModel

# async def test_get_application(
#         client,
#         test_db_session
# ):  
#     for i in range(20):
#         application = ApplicationModel(
#             username=f'test_get_application_name{i}',
#             description=f'test_get_application_desc{i}',
#         )
#         test_db_session.add(application)
#     await test_db_session.commit()

#     response = await client.get('/api/v1/applications/')
#     content = response.content
#     print(content)
#     assert response.status_code == HTTP_200_OK
#     assert response.content == content

# async def test_create_application(
#         client,
# ):
#     response = await client.post(
#         '/api/v1/applications/',
#         json={
#             "username": "test_create_application_name",
#             "description": "test_create_application_desc"
#         }
#     )

#     assert response.status_code == HTTP_201_CREATED
