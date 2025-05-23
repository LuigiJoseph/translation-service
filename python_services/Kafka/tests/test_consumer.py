
import pytest
from unittest.mock import patch, Mock

from python_services.Kafka.consumer import call_translation_api, process_messages, TOPIC_OUT
from python_services.config import load_config

config = load_config()
REST_API_URL= config["kafka"]["rest_api_url"]

@pytest.fixture
def mock_kafka_consumer():
    consumer = Mock()
    consumer.poll = Mock()  
    return consumer

@pytest.fixture
def mock_kafka_producer():
    producer = Mock()
    producer.produce = Mock() 
    return producer


@patch("requests.post")
def test_call_translation_api_valid_response(mock_post):
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"translated_text": "Merhaba"}
    mock_response.headers = {"Content-Type": "application/json"}  

    mock_post.return_value = mock_response

    # ✅ Call the function
    result = call_translation_api("Hello", "en", "tr", "qwen")

    # ✅ Assertions
    assert result  == {"success": True,"translated_text": "Merhaba"}
    mock_post.assert_called_once_with(
        f"{REST_API_URL}",
        json={"target_locale": "tr", "source_locale": "en", "text": "Hello","model": "qwen"},
        headers={"Content-Type": "application/json"},
        timeout=5
    )

@patch("requests.post")
def test_call_translation_api_unsupported_model(mock_post):
    result = call_translation_api("Hello", "en", "tr", "model")

    assert result == {'error:': 'Unsupported Model', 'success:': False}
    mock_post.assert_not_called()

