from loguru import logger
from aiokafka import AIOKafkaProducer

class KafkaProducer:
    _instance = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = AIOKafkaProducer(
                bootstrap_servers='localhost:9092'
            )
            await cls._instance.start()
        return cls._instance

    @classmethod
    async def stop(cls):
        if cls._instance is not None:
            await cls._instance.stop()
            cls._instance = None
    
    @classmethod
    async def send_message(cls, topic, message):
      producer = await cls.get_instance()
      try:
          await producer.send_and_wait(topic, message.encode('utf-8'))
          logger.debug(f'Message sent to "{topic}"')
      except Exception as e:
          logger.error(f'Error sending message to {topic}: {e}')
