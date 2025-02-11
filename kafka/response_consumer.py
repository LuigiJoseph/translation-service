from confluent_kafka import Consumer
from config import KAFKA_BROKER, TOPIC_OUT
import json
from logger import get_logger

# ✅ Initialize Logger
logger = get_logger("response_consumer")

# ✅ Initialize Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'response_group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([TOPIC_OUT])
logger.info("Kafka Response Consumer started", extra={"topic": TOPIC_OUT})

# ✅ Start consuming messages
while True:
    msg = consumer.poll(1.0)

    if msg is None:
        logger.debug("🕒 No new messages, waiting...")
        continue

    if msg.error():
        logger.error("❌ Response Consumer Error", extra={"kafka_error": str(msg.error())})
        continue

    try:
        # ✅ Log the raw Kafka message
        msg_raw = msg.value().decode('utf-8') if msg.value() else None
        logger.debug("📝 Raw response message received", extra={"message_raw": msg_raw})

        if msg_raw is None:
            logger.error("⚠️ Received empty message from Kafka. Skipping...")
            continue

        # ✅ Parse message
        message_data = json.loads(msg_raw)
        translated_text = message_data.get("translated_text")

        if translated_text is None:
            logger.error("⚠️ Received message does NOT contain 'translated_text' key. Skipping...", extra={"message_data": message_data})
            continue

        logger.info("📥 Received Translated Text", extra={"translated_text": translated_text})

    except json.JSONDecodeError as e:
        logger.error("❌ JSON Decoding Error", extra={"error_details": str(e), "raw_message": msg_raw}, exc_info=True)
    except Exception as e:
        logger.error("❌ Unexpected error processing message", extra={"error_details": str(e)}, exc_info=True)