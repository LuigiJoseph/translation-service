from ollama import chat
from ollama import ChatResponse
import ollama
from log.loggers import logger


logger.info("pulling llama3.2:1b ")
ollama.pull('llama3.2:1b')
logger.info("pulled llama3.2:1b ")

# def translate_text(text,source_lang,target_lang):
#     """Handles Qwen translation using Ollama"""
#     payload = {
#         "model": "qwen2.5-1.5b",  # Users can specify models dynamically if needed
#         "prompt": f"Translate from {source_lang} to {target_lang}: {text}",
#         "stream": False
#     }
#     response = requests.post(OLLAMA_URL, json=payload)

#     if response.status_code == 200:
#         translated_text = response.json().get("response", "").strip()
#         logger.info(f"Translated Text: {translated_text}")
#         return translated_text
#     else:
#         raise Exception(f"Ollama API error: {response.text}")



# def translate_text(text,source_lang,target_lang):
#     url = "http://ollamal/api/generate" 
#     response: ChatResponse = chat(model='llama3.2:1b', messages=[
#     {
#         "role": "system", "content": "You are a translator with the source and target locales of both languages. You only return the translated text.",
#         "role": "user", "content": f"Translate from {source_lang} to {target_lang} the following text: {text}",
#     },
#     ])
    
#     logger.info(response['message']['content'])
#     # or access fields directly from the response object
#     # print(response.message.content)

#     return response