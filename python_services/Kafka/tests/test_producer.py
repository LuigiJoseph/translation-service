import pytest
from unittest.mock import patch,MagicMock, Mock
import json
import requests

from python_services.Kafka.producer import send_translation_request , delivery_report , producer

@pytest.fixture
def mock_producer():
    return MagicMock()

@pytest.fixture
def mock_logger():
    return MagicMock()



@patch('python_services.Kafka.producer.logger', new_callable=MagicMock)
def test_delivery_report_success(mock_logger):
    # Mock Kafka message
    mock_msg = MagicMock()
    mock_msg.topic.return_value = "test_topic"
    mock_msg.partition.return_value = 0
    mock_msg.offset.return_value = 123

    # Call delivery_report with no error
    delivery_report(None, mock_msg)

    # Verify that the logger was called with the success message
    mock_logger.info.assert_called_with(" Message delivered", extra={
        "topic": "test_topic",
        "partition": 0,
        "offset": 123
    })

@patch('python_services.Kafka.producer.logger', new_callable=MagicMock)
def test_delivery_report_failure(mock_logger):
    # Simulate a Kafka delivery error
    error = Exception("Kafka delivery failed")

    # Call delivery_report with an error
    delivery_report(error, None)

    # Verify that the logger was called with the error message
    mock_logger.error.assert_called_with("Kafka message delivery failed", extra={"error_details": "Kafka delivery failed"})    

@patch('python_services.Kafka.producer.logger', new_callable=MagicMock)
@patch('python_services.Kafka.producer.producer', new_callable=MagicMock)
def test_send_translation_request_success(mock_producer, mock_logger):
    TOPIC_IN = "topic_in"
    mock_producer.produce.return_value = None
    mock_producer.flush.return_value = None

    send_translation_request("Hello", "en", "tr", "qwen")

    # Verify that the producer.produce method was called with the correct payload
    expected_payload = json.dumps({
        'target_locale': 'tr',
        'source_locale': 'en',
        'text': 'Hello',
        'model_name': 'qwen'
    }, ensure_ascii=False)
    mock_producer.produce.assert_called_once_with(
        TOPIC_IN, 
        value=expected_payload,
        callback=delivery_report
    )

    
    mock_logger.info.assert_called_with("Successfully sent translation request", extra={"kafka_payload": expected_payload})

@patch('python_services.Kafka.producer.logger', new_callable=MagicMock)
@patch('python_services.Kafka.producer.producer', new_callable=MagicMock)
def test_send_translation_request_failure(mock_producer, mock_logger):
    # Simulate an exception in the producer
    mock_producer.produce.side_effect = Exception("Kafka produce error")

    # Call send_translation_request
    send_translation_request("Hello", "en", "tr", "qwen")

    # Verify that the logger was called with the error message
    mock_logger.error.assert_called_with("Failed to send Kafka message", extra={"error_details": "Kafka produce error"}, exc_info=True)