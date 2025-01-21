from contextlib import asynccontextmanager
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from src.kafka.producer import KafkaProducer
from src.config import settings
from src.applications.router import router as router_application
from src.utils.logger import unified_logging

unified_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await KafkaProducer.get_instance()
    yield 
    await KafkaProducer.stop()


app = FastAPI(
    title=settings.APP_TITLE,
    version='1.0',
    lifespan=lifespan,
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
