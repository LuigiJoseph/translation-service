from confluent_kafka import Consumer, Producer
from config import KAFKA_BROKER, TOPIC_OUT, TOPIC_IN
import json
import os
import requests


# Initilize Kafka Consumer
consumer = Consumer({
    'bootstrap.servers' : KAFKA_BROKER,
    'group.id' : 'translation group',
    'auto.offset.reset' : 'earliest'
})
consumer.subscribe([TOPIC_IN])

# Initilize Kafka Producer for responses
producer = Producer({'bootstrap.servers': KAFKA_BROKER})


REST_API_URL = "http://sync:5000/api/v1/translate"


def call_api(text):
    payload = {
        "source_target_locale": "en-tr",  # Set default or modify dynamically
        "target_locale": "tr",
        "text": text
    }
    response = requests.post(REST_API_URL, json=payload)
    print(f"📡 Sent request to API: {payload}")
    print(f"🔍 API Response: {response.status_code} - {response.text}")  # DEBUGGING
    if response.status_code == 200:
        return response.json().get("translated_text", "")
    return f"ERROR: {response.text}"


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
    translated_text = call_api(text_to_translate)

    #send translation result to topic_out
    response_message = json.dumps({"translated_text" : translated_text})
    producer.produce(TOPIC_OUT, value=response_message)
    producer.flush()
    print(f"Published translation: {response_message}")