from confluent_kafka import Consumer, Producer
import json
import requests


from config import load_config
from python_services.Kafka.logger import get_logger

config = load_config()
KAFKA_BROKER= config["kafka"]["kafka_broker"]
TOPIC_IN=  config["kafka"]["topic_in"]
TOPIC_OUT=  config["kafka"]["topic_out"]
GROUP_ID= config["kafka"]["group_id"]
REST_API_URL= config["kafka"]["rest_api_url"]

# ✅ Initialize Two Separate Loggers
logger = get_logger("translation_consumer")  # Logs consumer-related messages


# ✅ Initialize Kafka Consumer for Incoming Messages
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


# ✅ Function to Call the Translation API
def call_translation_api(text, source_locale, target_locale, model_name):
    # Dynamically changes the api depending on the model names
    if model_name not in ["qwen", "helsinki"]:
        logger.error("Unsupported model received", extra={"model_name": model_name})
        return {"success:": False, "error:" : "Unsupported Model"}


    rest_api_url = f"{REST_API_URL}/{model_name}"    


    payload = {
        'target_locale': target_locale,
        "source_locale": source_locale,
        "text":text
    }
    logger.info("Sending request to API", extra={"api_payload": payload, "api_url": rest_api_url})

    try:
        response = requests.post(rest_api_url, json=payload, headers={"Content-Type": "application/json"}, timeout=5)
        
        logger.info(" API Response Successful", extra={
            "status_code": response.status_code,
            "response_headers": dict(response.headers),
            "api_response": response.text
        })

        if response.status_code == 200:
            response_json = response.json()
            translated_text = response_json.get("translated_text")
        
            if translated_text:
                return {"success:" :True, "translated_text:": translated_text}
            else:
                return {"success:" :False, "error:": "Missing 'translated_text' in API response"}

        return {"success": False, "error": f"API returned {response.status_code} - {response.text}"}

    except requests.RequestException as e:
        logger.error("Translation API request failed", 
                    extra={
                        "error_details": str(e),
                        "payload": payload,  #  Adding the payload details
                        "api_url": rest_api_url  
                    }, exc_info=True)
        return {"success": False, "error": "Translation API request failed"}

#  Function for Processing Incoming Messages
def process_messages():
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            logger.debug(" No new messages, waiting...")
            continue

        if msg.error():
            logger.error("Consume error", extra={"kafka_error": str(msg.error())})
            continue

        try:
            #  Log the raw Kafka message
            msg_raw = msg.value().decode('utf-8') if msg.value() else None
            logger.debug("Kafka message received", extra={"message_raw": msg_raw})

            if msg_raw is None:
                logger.error(" Received empty message from Kafka. Skipping...")
                continue

            #  Parse message
            message_data = json.loads(msg_raw)
            text_to_translate = message_data.get("text")
            source_locale = message_data.get("source_locale")
            target_locale = message_data.get("target_locale")
            model_name = message_data.get("model_name")

            # Stop processing if a field is
            if not text_to_translate or not source_locale or not target_locale or not model_name:
                logger.error(" Missing required fields in Kafka message. Skipping...", extra={"message_data": message_data})


            logger.info(" Received text to translate", extra={"text_to_translate": text_to_translate})

            #  Call translation API
            response = call_translation_api(text_to_translate,source_locale, target_locale, model_name)

            if response.get("success"):
                translated_text = response["translated_text"]
                response_message = json.dumps({
                    "text":text_to_translate,
                    "source_language": source_locale,
                    'target_language': target_locale,
                    "translated_text": translated_text,
                    "model_name": model_name})    
            
            else:
                error_message = response.get("error", "Unknown error")  #  Extract error message
                logger.error("Translation failed", extra={
                    "text": text_to_translate,
                    "source_locale": source_locale,
                    "target_locale": target_locale,
                    "error_message": error_message
                })

                response_message = json.dumps({
                    "text": text_to_translate,
                    "source_language": source_locale,
                    "target_language": target_locale,
                    "error": error_message,  #  Store error instead of translation
                    "model_name": model_name
                })


            producer.produce(TOPIC_OUT, value=response_message)
            producer.flush()

            logger.info(" Published translation", extra={"translated_text_payload": translated_text})

        except json.JSONDecodeError as e:
            logger.error(" JSON Decoding Error", extra={"error_details": str(e), "raw_message": msg_raw}, exc_info=True)
        except Exception as e:
            logger.error(" Unexpected error processing message", extra={"error_details": str(e)}, exc_info=True)


if __name__ == "__main__":
    process_messages()