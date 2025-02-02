from confluent_kafka import Consumer, Producer
import json
import os
import requests

# Load Kafka configuation
# KAFKA_BROKER  = os.getenv("KAFKA_BROKER", "kafka:9093")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC_IN = "topic_in"
TOPIC_OUT = "topic_out"


# Initilize Kafka Consumer
consumer = Consumer({
    'bootstrap.servers' : KAFKA_BROKER,
    'group.id' : 'translation group',
    'auto.offset.reset' : 'earliest'
})
consumer.subscribe([TOPIC_IN])

# Initilize Kafka Producer for responses
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Will replace this with API method for translating
def process_text(text):
    print(f"Processing text: {text}")
    return text[::-1] #return the string reversed for testing


# Start consuming messages
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        print("🕒 No new messages, waiting...")
        continue
    if msg.error():
        print(f"Consume error: {msg.error()}")
        continue

    #Decode and process message:
    text_data = json.loads(msg.value().decode('utf-8'))
    text_to_translate = text_data["text"]
    print(f"Received text to trasnlate: {text_to_translate}")

    # REPLACE LATER WITH PROPER FUNCTION
    translated_text = process_text(text_to_translate)

    #send translation result to topic_out
    response_message = json.dumps({"translated_text" : translated_text})
    producer.produce(TOPIC_OUT, value=response_message)
    producer.flush()
    print(f"Published translation: {response_message}")