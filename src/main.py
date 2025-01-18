from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from src.config import settings
from src.applications.router import router as router_application

app = FastAPI(
    title='Заявки пользователей API',
    version='1.0',
    swagger_ui_parameters={
        'operationsSorter': 'method',
        'defaultModelsExpandDepth': -1
    },
)
app.include_router(router_application)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ORIGINS],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
    allow_headers=[
        'Access-Control-Allow-Headers', 'Access-Control-Allow-Origin',
        'Content-Type', 'Set-Cookie', 'Authorization'
    ]
)


logger.add('../log.txt')
