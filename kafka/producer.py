from confluent_kafka import Producer
import json
import logging
from pathlib import Path
import yaml
from pythonjsonlogger import jsonlogger


configfile_path = Path("/configs/config.yaml")
# configfile_path = Path(__file__).resolve().parents[2] / "configs"/"config.yaml"

try:
    with open(configfile_path, "r") as file:
        config = yaml.safe_load(file)
except Exception as e:
    print(f"Error opening file: {e}")


KAFKA_BROKER= config["kafka"]["kafka_broker"]
TOPIC_IN=  config["kafka"]["topic_in"]
TOPIC_OUT=  config["kafka"]["topic_out"]
GROUP_ID= config["kafka"]["group_id"]


#  Configure JSON Logging (Avoids "message" Key Conflicts)
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

#  Initialize Kafka Producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})
logger.info("Kafka Producer initialized", extra={"kafka_broker": KAFKA_BROKER, "topic": TOPIC_IN})



# makes produce function wait for the messages and then sends log
def delivery_report(err, msg):
    """ Kafka delivery callback: Runs when Kafka confirms message delivery. """
    if err is not None:
        logger.error("Kafka message delivery failed", extra={"error_details": str(err)})
    else:
        logger.info(" Message delivered", extra={"topic": msg.topic(), "partition": msg.partition(), "offset": msg.offset()})



# Function to send messages
def send_translation_request(text, source_locale, target_locale, model_name):
    try:
        data = json.dumps({
        'target_locale': target_locale,
        "source_locale": source_locale,
        "text":text,
        "model_name": model_name
            }, ensure_ascii=False)  #  Added ensure_ascii=False

        # Callback function that gets called when processing message
        producer.produce(TOPIC_IN, value=data, callback=delivery_report)
        producer.flush()

        logger.info("Successfully sent translation request", extra={"kafka_payload": data})
    except Exception as e:
        logger.error("Failed to send Kafka message", extra={"error_details": str(e)}, exc_info=True)

if __name__ == "__main__":
    text = str(input("Please enter text to be translated: "))
    source_locale = str(input("Please enter the source language (e.g: en for English, tr for Turkish)"))
    target_locale = str(input("Please enter the target language (e.g: en for English, tr for Turkish)"))
    model_name = str(input("Please enter the model name (transformers, qwen)"))
    
    logger.info("User input received", extra={
        "input_text_payload": text,
        "source_locale": source_locale,
        "target locale": target_locale})
    
    send_translation_request(text, source_locale, target_locale, model_name)