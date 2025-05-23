import requests
from flask import abort


from python_services.sync.log.loggers import logger
from python_services.config import load_config

config = load_config()

OLLAMA_URL = config["ollama"]["url"]
MODEL_NAME= config["qwen"]["model_name"]


logger.info("ollama running")
def translate_qwen(text, source_lang, target_lang):
    """Handles Qwen translation using Ollama"""

    if not text.strip():
        return {"error": "Input text cannot be empty"}, 400
    
    payload = {
        "model": MODEL_NAME, 
        "prompt": f"""You are a highly skilled translator. 
        Translate the following text from {source_lang} to {target_lang}. 
        Only return the translated text without explanations, formatting, or additional details:\n\n{text}""",

        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        translated_text = response.json().get("response", "").strip()
        logger.info(f"Translated Text: {translated_text}")
        return translated_text
    else:
        logger.error(f"Ollama API Error: {response.status_code} - {response.text}")
        abort(response.status_code, description=f"Ollama API error: {response.text}")
    
