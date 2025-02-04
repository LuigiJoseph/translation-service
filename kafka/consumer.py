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

#Place holder for the API laters
REST_API_URL = "http://rest-api:5000/translate"

# Function to call REST API
def call_translation_api(text):
    response = requests.post(REST_API_URL, json={"text": text})
    print(f"📡 Sent request to API: {text}")
    print(f"🔍 API Response: {response.status_code} - {response.text}")  # DEBUGGING
    if response.status_code == 200:
        return response.json().get("translated_text", "")
    return "ERROR"


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
    translated_text = call_translation_api(text_to_translate)

    #send translation result to topic_out
    response_message = json.dumps({"translated_text" : translated_text})
    producer.produce(TOPIC_OUT, value=response_message)
    producer.flush()
    print(f"Published translation: {response_message}")