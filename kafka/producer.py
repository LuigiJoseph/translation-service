from confluent_kafka import Producer
from config import KAFKA_BROKER, TOPIC_IN
import json
import logging
from pythonjsonlogger import jsonlogger

# ✅ Configure JSON Logging (Avoids "message" Key Conflicts)
logger = logging.getLogger("translation_producer")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("producer_service.log")
console_handler = logging.StreamHandler()


json_formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s  %(levelname)s  %(name)s",  
    json_ensure_ascii=False
)

file_handler.setFormatter(json_formatter)
console_handler.setFormatter(json_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ✅ Initialize Kafka Producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})
logger.info("Kafka Producer initialized", extra={"kafka_broker": KAFKA_BROKER, "topic": TOPIC_IN})

# Function 
def delivery_report(err, msg):
    """ Kafka delivery callback: Runs when Kafka confirms message delivery. """
    if err is not None:
        logger.error("Kafka message delivery failed", extra={"error_details": str(err)})
    else:
        logger.info("✅ Message delivered", extra={"topic": msg.topic(), "partition": msg.partition(), "offset": msg.offset()})



# ✅ Function to send messages
def send_translation_request(text):
    try:
        data = json.dumps({"text": text}, ensure_ascii=False)  # ✅ Added ensure_ascii=False

        # Callback function that gets called when processing message
        producer.produce(TOPIC_IN, value=data, callback=delivery_report)
        producer.flush()

        logger.info("Successfully sent translation request", extra={"kafka_payload": data})
    except Exception as e:
        logger.error("Failed to send Kafka message", extra={"error_details": str(e)}, exc_info=True)

if __name__ == "__main__":
    input_text = str(input("Please enter text to be translated: "))
    logger.info("User input received", extra={"input_text_payload": input_text})
    send_translation_request(input_text)
