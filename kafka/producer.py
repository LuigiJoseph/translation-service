from confluent_kafka import Producer
import json
import os


# Load kafka configration
# KAFKA_BROKER  = os.getenv("KAFKA_BROKER", "kafka:9093")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC_IN = "topic_in"

# Initilize the kafka producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Function to send message
def send_translation_request(text):
    data = json.dumps({"text": text})
    producer.produce(TOPIC_IN, value=data)
    producer.flush()
    print(f"Successfuly Sent translation request: {data}")



if __name__ == "__main__":
    send_translation_request("Hello, Kafka!")
