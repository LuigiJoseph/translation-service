from confluent_kafka import Consumer, Producer
from config import KAFKA_BROKER, TOPIC_OUT, TOPIC_IN
import json
import os
import requests
from logger import get_logger

REST_API_URL = "http://sync:5000/api/v1/translate"

# Initilize Logger
logger = get_logger("translation_consumer")

# ✅ Initialize Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'translation_group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([TOPIC_IN])
logger.info("Kafka Consumer subscribed", extra={"topic": TOPIC_IN})

# ✅ Initialize Kafka Producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})
logger.info("Kafka Producer initialized", extra={"kafka_broker": KAFKA_BROKER})



def call_translation_api(text):
    """ Calls the translation API and returns the translated text. """
    payload = {
        "source_target_locale": "en-tr",
        "target_locale": "tr",
        "text": text
    }
    logger.info("📡 Sending request to API", extra={"api_payload": payload})  

    try:
        response = requests.post(REST_API_URL, json=payload, headers={"Content-Type": "application/json"})
        
        logger.info("🔍 API Response", extra={
            "status_code": response.status_code,
            "response_headers": dict(response.headers),
            "api_response": response.text
        })

        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            return response_json.get("translated_text", " ERROR: Missing 'translated_text' in API response")

        return f"❌ ERROR: API returned {response.status_code} - {response.text}"
    
    except requests.RequestException as e:
        logger.error("❌ API request failed", extra={"error_details": str(e)}, exc_info=True)
        return "ERROR: Translation API request failed"



# Start consuming messages
while True:
    msg = consumer.poll(1.0)

    if msg is None:
        logger.debug(" No new messages, waiting...")
        continue

    if msg.error():
        logger.error(" Consume error", extra={"kafka_error": str(msg.error())})
        continue


    #Decode and process message:
    msg_raw = msg.value().decode('utf-8') if msg.value() else None
    logger.debug("📝 Raw Kafka message received", extra={"message_raw": msg_raw})


    # ✅ Parse message
    message_data = json.loads(msg_raw)
    text_to_translate = message_data.get("text")
    
    if text_to_translate is None:
        logger.error("⚠️ Received message does NOT contain 'text' key. Skipping...", extra={"message_data": message_data})
        continue

    logger.info("📥 Received text to translate", extra={"text_to_translate": text_to_translate})

    translated_text = call_translation_api(text_to_translate)

    # ✅ Send translation result to TOPIC_OUT
    response_message = json.dumps({"translated_text": translated_text})
    producer.produce(TOPIC_OUT, value=response_message)
    producer.flush()

    logger.info("📤 Published translation", extra={"translated_text_payload": translated_text})
