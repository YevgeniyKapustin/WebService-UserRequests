from loguru import logger
from aiokafka import AIOKafkaProducer
from aiokafka.structs import RecordMetadata

from src.config import settings


class KafkaProducer:
    _instance = None

    @classmethod
    async def get_instance(cls) -> AIOKafkaProducer:
        if cls._instance is None:
            url = f'{settings.KAFKA_PRODUCER_HOST}:{settings.KAFKA_PRODUCER_PORT}'
            cls._instance = AIOKafkaProducer(
                bootstrap_servers=url
            )
            await cls._instance.start()
            logger.info(f'Kafka Producer running on {url}')
        return cls._instance

    @classmethod
    async def stop(cls) -> None:
        if cls._instance is not None:
            await cls._instance.stop()
            cls._instance = None
            logger.info(f'Kafka Producer stopped')

    @classmethod
    async def send_message(cls, topic: str, message: str) -> RecordMetadata | None:
      producer = await cls.get_instance()
      try:
          result: RecordMetadata = await producer.send_and_wait(topic, message.encode('utf-8'))
          logger.debug(f'Kafka sent message to topic: "{topic}"')
          return result
      except Exception as e:
          logger.error(f'Kafka error sending message to topic: "{topic}": {e}')
          return None
