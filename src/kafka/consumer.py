import asyncio
import json
import os

from confluent_kafka import Consumer, KafkaError

from data import db_handler
from kafka.message_handler import data_update


async def consume_messages():
    consumer_config = {
        "bootstrap.servers": os.getenv("KAFKA_ADVERTISED_LISTENERS", "kafka:9093"),
        "group.id": "consumer_group",
        "auto.offset.reset": "earliest",
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe(["test_topic"])
    
    async with db_handler.get_session() as session:
        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        continue
                
                data = json.loads(msg.value().decode('utf-8'))
                
                await data_update([data], session)
        
        finally:
            consumer.close()


if __name__ == "__main__":
    asyncio.run(consume_messages())
