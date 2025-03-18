from confluent_kafka import Consumer
import json



from python_services.Kafka.logger import get_logger
from python_services.config import load_config

config = load_config()
KAFKA_BROKER = config["kafka"]["kafka_broker"]
TOPIC_OUT = config["kafka"]["topic_out"]
GROUP_ID = config["kafka"]["response_group"]

# ✅ Initialize Logger
logger = get_logger("response_consumer")

# ✅ Initialize Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': GROUP_ID,
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([TOPIC_OUT])

logger.info("Kafka Response Consumer started", extra={"topic": TOPIC_OUT})

# ✅ Function to Process Incoming Response Messages
def process_response_messages():
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            logger.debug(" No new response messages, waiting...")
            continue

        if msg.error():
            logger.error(" Kafka Consumer Error", extra={"kafka_error": str(msg.error())})
            continue

        try:
            #  Log the raw Kafka message
            msg_raw = msg.value().decode('utf-8') if msg.value() else None
            logger.debug("Raw response message received", extra={"message_raw": msg_raw})

            if msg_raw is None:
                logger.error(" Received empty message from Kafka. Skipping...")
                continue

            #  Parse message
            message_data = json.loads(msg_raw)
            text = message_data.get("text")
            source_locale = message_data.get("source_language")
            target_locale = message_data.get("target_language")
            translated_text = message_data.get("translated_text")
            model_name = message_data.get("model_name")

            #  Validate message content
            if not text or not source_locale or not target_locale or not translated_text or not model_name:
                logger.error(" Missing required fields in response message. Skipping...", extra={
                    "text": text,
                    "source_locale": source_locale,
                    "target_locale": target_locale,
                    "translated_text": translated_text,
                    "model_name": model_name
                })
                continue

            # ✅ Log the successful translation event
            logger.info(" Processed Translated Message", extra={
                "original_text": text,
                "source_locale": source_locale,
                "target_locale": target_locale,
                "translated_text": translated_text,
                "model_name": model_name
            })

        except json.JSONDecodeError as e:
            logger.error(" JSON Decoding Error", extra={"error_details": str(e), "raw_message": msg_raw}, exc_info=True)
        except Exception as e:
            logger.error(" Unexpected error processing message", extra={"error_details": str(e)}, exc_info=True)

# ✅ Run the response consumer
if __name__ == "__main__":
    process_response_messages()
