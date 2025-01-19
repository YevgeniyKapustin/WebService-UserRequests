from loguru import logger
from aiokafka import AIOKafkaProducer

from src.config import settings
class KafkaProducer:
    _instance = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            url = f'{settings.KAFKA_HOST}:9092'
            cls._instance = AIOKafkaProducer(
                bootstrap_servers=url
            )
            await cls._instance.start()
            logger.info(f'Kafka Producer running on {url}')
        return cls._instance

    @classmethod
    async def stop(cls):
        if cls._instance is not None:
            await cls._instance.stop()
            cls._instance = None
            logger.info(f'Kafka Producer stopped')
    
    @classmethod
    async def send_message(cls, topic, message):
      producer = await cls.get_instance()
      try:
          await producer.send_and_wait(topic, message.encode('utf-8'))
          logger.debug(f'Kafka sent message to topic: "{topic}"')
      except Exception as e:
          logger.error(f'Kafka error sending message to topic: "{topic}": {e}')
