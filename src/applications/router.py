from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from database import get_async_session
from schemas import NotFoundScheme
from src.applications.models import Application

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
            'model': list[Application],
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
        user_name: Annotated[
            str | None,
            Query(
                title='Имя пользователя',
                description='Искать по имени пользователя'
            )
        ] = None,

        session: AsyncSession = Depends(get_async_session),

) -> JSONResponse:
    crud: CommandCRUD = CommandCRUD(
        type_=command_type,
        request=request_,
        is_inline=is_inline
    )

    return await get_objects(crud, CommandScheme, session)


# @router.post(
#     '/commands',
#     name='Создает команду',
#     responses=get_create_response()
# )
# async def create_command(
#         command: CommandCreateScheme,

#         session: AsyncSession = Depends(get_async_session),

# ) -> JSONResponse:
#     obj = CommandCRUD(
#         type_=command.type,
#         request=command.request,
#         response=command.response,
#     )
#     return await create_object(obj, session)
