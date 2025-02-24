import yaml
from pathlib import Path
import requests

from log.loggers import logger

configfile_path = Path("/configs/config.yaml")
# configfile_path = Path(__file__).resolve().parents[2] / "configs"/"config.yaml"
try:
    with open(configfile_path, "r") as file:
        config = yaml.safe_load(file)
except Exception as e:
    logger.info(f"Error opening file: {e}")

OLLAMA_URL = config["ollama"]["url"]

def translate_qwen(text, source_lang, target_lang):
    """Handles Qwen translation using Ollama"""

    if not text.strip():
        return {"error": "Input text cannot be empty"}, 400
    
    payload = {
        "model": 'qwen2.5:1.5b-instruct', 
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
        raise Exception(f"Ollama API error: {response.text}")