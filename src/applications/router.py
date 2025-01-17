from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from applications.schemas import ApplicationCreateSchema, ApplicationSchema
from database import get_async_session
from schemas import CreateScheme, NotFoundScheme, OkScheme
from src.applications.models import Application as ApplicationModel
from src.applications.sevice import Application

router = APIRouter(
    prefix='/api/v1',
    tags=['Заявки пользователей'],
)


@router.get(
    '/applications',
    name='Возвращает список заявок',
    description='''
    Предоставляет списка заявок по запросу.
    ''',
    responses = {
        HTTP_200_OK: {
            'model': list[ApplicationModel],
            'description': 'Список заявок получен',
        },
        HTTP_404_NOT_FOUND: {
            'model': JSONResponse(
                content=NotFoundScheme().dict(),
                status_code=HTTP_404_NOT_FOUND,
            ),
            'description': 'Заявок не существует',
        }
    }
)
async def get_application(
        user_name: Annotated[str | None, Query(title='Имя пользователя',)] = None,
        page: Annotated[str | None, Query(title='Страница', ge=1)] = None,
        size: Annotated[str | None, Query(title='Размер страницы', ge=1)] = None,

        session: AsyncSession = Depends(get_async_session)

) -> JSONResponse:
    searched_application = Application(user_name)

    if applications := await searched_application.get(session, page, size):

        response: list[dict] = [
            {
                attr: getattr(obj, attr)
                for attr in ApplicationSchema.model_json_schema().get('properties')
            }
            for obj in applications
        ]
        return JSONResponse(
            content=response,
            status_code=HTTP_200_OK,
        )

    else:
        return JSONResponse(
            content=NotFoundScheme().model_dump(),
            status_code=HTTP_404_NOT_FOUND,
        )


@router.post(
    '/applications',
    name='Создаёт заявку пользователя',
    responses={
        HTTP_201_CREATED: {
            'model': CreateScheme,
            'description': 'Заявка создана',
        }
    }
)
async def create_application(
        application: ApplicationCreateSchema,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    application = Application(application.user_name, application.description)
    await application.create(session)
    return JSONResponse(
        content=CreateScheme().model_dump(),
        status_code=HTTP_201_CREATED
    )
