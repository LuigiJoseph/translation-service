from confluent_kafka import Consumer
from config import KAFKA_BROKER, TOPIC_OUT
import json
import os


# Initialize Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'response_group',
    'auto.offset.reset': 'earliest'
})



consumer.subscribe([TOPIC_OUT])

# Start consuming
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Response Consumer Error : {msg.error()}")
        continue

    # Decode and process message 
    translated_text = json.loads(msg.value().decode('utf-8'))["translated_text"]
    print(f"Received Translated Text: {translated_text}")