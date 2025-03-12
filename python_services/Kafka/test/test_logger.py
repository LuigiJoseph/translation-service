from unittest.mock import patch, MagicMock
import pytest
from io import StringIO
import json
import logging

from python_services.Kafka.logger import get_logger , JsonFormatter

@pytest.fixture
def mock_path_mkdir():
    with patch("pathlib.Path.mkdir") as mock_mkdir:
        yield mock_mkdir

@pytest.fixture
def mock_file_handler():
    with patch("logging.FileHandler") as mock_file_handler:
        yield mock_file_handler

def test_json_formatter():
    log_record = logging.LogRecord(
        name="test_logger",
        level=logging.DEBUG,
        pathname="test.py",
        lineno=10,
        msg="Test message",
        args=None,
        exc_info=None
    )
    
    formatter = JsonFormatter()
    log_json = formatter.format(log_record)
    
    # Convert JSON string back to dictionary to verify the structure
    log_dict = json.loads(log_json)
    
    # Assertions to ensure the structure is as expected
    assert "name" in log_dict
    assert "asctime" in log_dict
    assert "levelname" in log_dict
    assert "message" in log_dict
    assert log_dict["message"] == "Test message"
