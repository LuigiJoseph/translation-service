from python_services.sync.log.loggers import logger
from python_services.sync.models.transformers_models import translate_text 
from python_services.sync.models.qwen_model import translate_qwen
from python_services.sync.mongodb.mongo import cache_translations , get_cached_translation, generate_cache_key

MODEL_HANDLERS = {
            "helsinki": translate_text,
            "qwen": translate_qwen
                                }
logger.info(f"Available models: {MODEL_HANDLERS.keys()}")
   
def translate_with_cache(text, source_locale, target_locale, model_name):


    model_key = model_name.lower()
    if model_key not in MODEL_HANDLERS:
        return {"error": f"Model '{model_name}' is not supported."}, 400

    # Check if translation exists in cache
    cache_key = generate_cache_key(text, source_locale, target_locale, model_name)

    cached_translation = get_cached_translation(cache_key)

    if cached_translation:
        translated_text = cached_translation["translated_text"]
        logger.info(f"Returning cached translation: {translated_text}")
        return translated_text

    translation_function = MODEL_HANDLERS[model_key]

    if model_key == 'helsinki' and (source_locale, target_locale) in [("tr", "ar"), ("ar", "tr")]:

        intermediate_result = translation_function(text, source_locale, "en") # Translate to English (`en`) intermediate language
        logger.info(f"Intermediate result: {intermediate_result} (type: {type(intermediate_result)})")

        if not intermediate_result:
            return {"error": "Intermediate translation to English failed."}, 400

        final_result = translation_function(intermediate_result, "en", target_locale) # Translate from English (`en`) to the target language
        logger.info(f"Final result: {final_result} (type: {type(final_result)})")

        if not final_result:
            return {"error": "Final translation failed."}, 400

        return final_result

    else:
        # Normal Direct Translation
        translated_text = translation_function(text, source_locale, target_locale)

    cache_translations(cache_key,text, source_locale, target_locale, model_name, translated_text)

    return  translated_text