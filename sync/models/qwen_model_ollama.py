from ollama import chat
from ollama import ChatResponse
import ollama
from log.loggers import logger


logger.info("pulling qwen2.5 ")
ollama.pull('qwen2.5:1.5b-instruct')
logger.info("pulled qwen2.5 ")

def translate_text(text,source_lang,target_lang):

    response: ChatResponse = chat(model='qwen2.5:1.5b-instruct', messages=[
    {
        "role": "system", "content": "You are a translator with the source and target locales of both languages. You only return the translated text.",
        "role": "user", "content": f"Translate from {source_lang} to {target_lang} the following text: {text}",
    },
    ])
    
    logger.info(response['message']['content'])
    # or access fields directly from the response object
    # print(response.message.content)

    return response