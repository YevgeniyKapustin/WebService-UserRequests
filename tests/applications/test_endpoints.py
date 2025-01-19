"""Интеграционные тесты для applications."""
from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
)

from src.database import get_async_session
from src.applications.models import Application as ApplicationModel

async def test_get_application(
        async_client: AsyncClient,
        session: AsyncSession = Depends(get_async_session)
):  
    for i in range(20):
        application = ApplicationModel(
            username=f'test_get_application_name{i}',
            description=f'test_get_application_desc{i}',
        )
        session.add(application)
    await session.commit()

    response = await async_client.get('/api/v1/applications/')
    content = response.content
    print(content)
    assert response.status_code == HTTP_200_OK
    assert response.content == content


async def test_create_application(
        async_client: AsyncClient,
):
    response = await async_client.post(
        '/api/v1/applications/',
        json={
            "type": "string",
            "request": "string",
            "response": "string"
        }
    )

    assert response.status_code == HTTP_201_CREATED
