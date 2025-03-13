
import sys
import os

# Add the parent directory of "tests" to sys.path so Python can find "restapi_server"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from unittest.mock import patch
from flask import json
from restapi_server import app  #  Import Flask app directly

# Create the client globally
app.config['TESTING'] = True
client = app.test_client()
app.testing = True  # testing mode


#  Test GET /api/v1/list-models
def test_list_models():
    response = client.get("translation-endpoints/api/v1/list-models")
    
    assert response.status_code == 200
    data = response.get_json()
    assert "available_models" in data
    assert isinstance(data["available_models"], list)
    assert "helsinki" in data["available_models"]
    assert "qwen" in data["available_models"]


#  Test POST /api/v1/translate/<model_name> - Successful Request
@patch("restapi_server.route.translate_with_cache")
def test_translation_success(mock_translate_with_cache):
    mock_translate_with_cache.return_value = "Merhaba"

    payload = {
        "text": "Hello",
        "source_locale": "en",
        "target_locale": "tr"
    }
    response = client.post("translation-endpoints/api/v1/translate/qwen", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["translated_text"] == "Merhaba"
    assert data["source_language"] == "en"
    assert data["target_language"] == "tr"


 
def test_translation_missing_fields():
    payload = {"source_locale": "en"}  # Missing "text" and "target_locale"
    response = client.post("translation-endpoints/api/v1/translate/qwen", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert "Input payload validation failed" in data["message"]



def test_translation_unsupported_model():
    payload = {
        "text": "Hello",
        "source_locale": "en",
        "target_locale": "tr"
    }
    response = client.post("translation-endpoints/api/v1/translate/unknown_model", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert "Model 'unknown_model' is not supported." in data["error"]



# TO-DO: change how API handles error to send a 400 when error message 
#        instead of return 200 with a body saying "error" 
@patch("restapi_server.route.translate_with_cache")  
@patch("mongodb.mongo.translation_cache.find_one")  
def test_translation_empty_text(mock_db_find, mock_translate_with_cache):
    mock_db_find.return_value = None  # ✅ Simulate cache miss
    mock_translate_with_cache.return_value = {"error": "Input text cannot be empty"}  # ✅ Simulate correct return

    payload = {
        "text": "   ",  # Empty text
        "source_locale": "en",
        "target_locale": "tr"
    }
    response = client.post("translation-endpoints/api/v1/translate/qwen", json=payload)  # ✅ Fixed path

    assert response.status_code == 400
    data = response.get_json()
    assert "Input text cannot be empty" in data["error"]




@patch("mongodb.mongo.translation_cache.find_one")
@patch("restapi_server.route.translate_with_cache")
def test_translation_with_cache(mock_translate_with_cache, mock_db_find):
    mock_db_find.return_value = {"translated_text": "Merhaba"}  # ✅Simulating cached response
    mock_translate_with_cache.return_value = "Merhaba"

    payload = {
        "text": "Hello",
        "source_locale": "en",
        "target_locale": "tr"
    }
    response = client.post("translation-endpoints/api/v1/translate/qwen", json=payload)

   
