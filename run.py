import uvicorn 

from src.kafka.producer import KafkaProducer
from src.main import app


if __name__ == '__main__':
        uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,
        log_level=None,
    )
