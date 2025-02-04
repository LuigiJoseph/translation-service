from confluent_kafka import Producer
from config import KAFKA_BROKER, TOPIC_IN
import json
import os



# Initilize the kafka producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Function to send message
def send_translation_request(text):
    data = json.dumps({"text": text})
    producer.produce(TOPIC_IN, value=data)
    producer.flush()
    print(f"Successfuly Sent translation request: {data}")



if __name__ == "__main__":
    input_text = str(input("please enter text to be translated: "))
    send_translation_request(input_text)
