from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from src.applications.service import Application
from src.applications.schemas import ApplicationCreateSchema, ApplicationSchema
from src.database import get_async_session
from src.utils.schemas import CreateScheme, NotFoundScheme

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
            'model': list[ApplicationSchema],
            'description': 'Список заявок получен',
        },
        HTTP_404_NOT_FOUND: {
            'model': NotFoundScheme,
            'description': 'Заявок не существует',
        }
    }
)
async def get_application(
        username: Annotated[str | None, Query(title='Имя пользователя',)] = None,
        page: Annotated[int | None, Query(title='Страница', ge=1)] = None,
        size: Annotated[int | None, Query(title='Размер страницы', ge=1)] = None,

        session: AsyncSession = Depends(get_async_session)

) -> JSONResponse:
    searched_application = Application(username)

    if applications := await searched_application.get(session, page, size):

        response: list[dict[str, str]] = [
            ApplicationSchema(
                id=application.id,
                username=application.username,
                description=application.description,
                created_at=application.created_at.isoformat(timespec="minutes"),
            )
            .model_dump()
            for application in applications
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
    application_obj = Application(application.username, application.description)
    await application_obj.create(session)
    return JSONResponse(
        content=CreateScheme().model_dump(),
        status_code=HTTP_201_CREATED
    )
