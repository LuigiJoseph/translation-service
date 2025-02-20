from flask import request, jsonify
from flask_restx import Resource, fields , Namespace
# import ollama


from log.loggers import logger
from models.helsinki_models import translate_text 
from models.qwen_model_ollama import translate_text as translate_qwen 
from mongodb.mongo import translation_cache , generate_cache_key
from restapi_server import api

api = Namespace("translation-endpoints", description="Translation controller")

# OLLAMA_HOST = "http://ollama:11434/api/chat" 

translation_model = api.model('TranslationRequest', {
    'target_locale': fields.String(required=False, description='Target languages'),
    'source_locale': fields.String(required=True, description='Source languages'),
    'text': fields.String(required=True, description='Text to translate')
})

MODEL_HANDLERS = {
            "helsinki": translate_text,
            "qwen": translate_qwen
                                }
logger.info(f"Available models: {MODEL_HANDLERS.keys()}")

def translate_with_cache(text, source_locale, target_locale, model_name):
            """Checks the cache before translating text."""
            
            # Generate a unique hash key
            cache_key = generate_cache_key(text, source_locale, target_locale,model_name)
            
            # Check if translation exists in cache
            cached_translation = translation_cache.find_one({"_id": cache_key})
            
            if cached_translation:
                logger.info("Cache hit! Returning cached translation.")
                return cached_translation["translated_text"]
            
            logger.info("Cache miss! Performing translation...")
            
            model_key = model_name.lower()  
            if model_key not in MODEL_HANDLERS:
                return {"error": f"Model '{model_name}' is not supported."}, 400

            translation_function = MODEL_HANDLERS[model_key]
            translated_text = translation_function(text, source_locale, target_locale)
            
            # Store in cache
            translation_cache.insert_one({
                "_id": cache_key,
                "source_text": text,
                "source_language": source_locale,
                "target_language": target_locale,
                "model_used": model_name,
                "translated_text": translated_text
            })
            
            return translated_text


# METHOD = POST -> Translation
@api.route("/api/v1/translate/<string:model_name>")
class TranslateResource(Resource):

    @api.expect(translation_model)
    @api.doc(responses={
        200: 'Success',
        201: 'Created',
        400: 'Bad Request',
        500: 'Internal Server Error' 
    })
    def post(self,model_name):
        """Translate text from one language to another"""
        data = request.json
        target_locale=data.get("target_locale")
        source_locale = data.get("source_locale")
        text = data.get("text")

        if not text:
            api.abort(400, "Missing required fields: text, source_locale, target_locale")
        

        model_name = model_name.lower()
        if model_name not in MODEL_HANDLERS:
            return {"error": f"Model '{model_name}' is not supported."}, 400

        # Use caching function
        translated_text = translate_with_cache(text, source_locale, target_locale, model_name)
            
        return {
                    "source_text":text,
                    "source_language": source_locale,
                    'target_language': target_locale,
                    "model_used": model_name,
                    "translated_text": translated_text
                }, 201


# METHOD = GET -> List models 
@api.route("/api/v1/list-models")
class Languages(Resource):
    @api.doc(responses={  
        200: 'Success',  
        400: 'Bad Request',
        500: 'Internal Server Error' 
    })
    def get(self):
        """Returns a list of available translation models."""
        return {
            "available_models": list(MODEL_HANDLERS.keys())
        }, 200

# @api.route('/')
# class Translation(Resource):
#     @api.expect(translation_model)
#     def post(self):
#         """Translate text using the specified Ollama model"""
#         data = request.json
#         text = data.get('text')
#         model = data.get('model')

#         if not text or not model:
#             return {'error': 'Text and model are required'}, 400

#         try:
#             # Use Ollama to generate the translation
#             response = ollama.generate(model=model, prompt=f"Translate the following text: {text}")
#             translation = response['response']

#             return {'translation': translation}, 200
#         except Exception as e:
#             return {'error': str(e)}, 500
    
