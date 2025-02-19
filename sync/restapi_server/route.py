from flask import request, jsonify
from flask_restx import Resource, fields , Namespace
import uuid


from log.loggers import logger
from models.model import translate_text , MODELS , mark_model_used
from mongodb.mongo import translationTxt_collection
from restapi_server import api


api = Namespace("translate", description="Translation operations")
logger.info(f"Number of handlers attached: {len(logger.handlers)}")

translation_model = api.model('TranslationRequest', {
    'source_target_locale': fields.String(required=True, description='Source and Target languages'),
    'target_locale': fields.String(required=True, description='Target language'),
    'text': fields.String(required=True, description='Text to translate')
})

# METHOD = POST -> Translation
@api.route("/api/v1/translate")
class TranslateResource(Resource):
    
    @api.expect(translation_model)
    @api.doc(responses={
        200: 'Success'
    })
    def post(self):
        """Translate text from one language to another"""
        request_id = str(uuid.uuid4())
        data = request.json
        target_locale=data.get("target_locale")
        source_target_locale = data.get("source_target_locale")
        text = data.get("text")

        if not text:
            api.abort(400, "text cannot be empty, please enter text")

        if source_target_locale in MODELS:
            model_info = MODELS[source_target_locale]
            mark_model_used(source_target_locale)
            cached_translation = translationTxt_collection.find_one({
                "source_target_locale": source_target_locale,
                "text": text
                })
            if cached_translation:
                logger.debug(f"transaltion: {text}, source_target_locale {source_target_locale} is retrived from cache")
                print(text)

                return jsonify({  
                "source_target_locale": source_target_locale,
                "text": text,
                "translated_text": cached_translation["translated_text"]
                })  
                

            
            translated_text = translate_text(text, source_target_locale)
            # inserting a new doc to mongodb collection
            translationTxt_collection.insert_one({
                "source_target_locale": source_target_locale,
                "text": text,
                "translated_text": translated_text
                })  
            
            
            return {
                "request_id": request_id,
                "translated_text": translated_text,
                "model_used": model_info["name"]
            }
        else:
            return {"error": "Invalid translation direction"}, 400

# METHOD = GET -> List models 
@api.route("/api/v1/list-models")
class Languages(Resource):
    @api.doc(responses={  
        200: 'Success',  
        400: 'Bad Request'  
    })
    def get(self):
        """This returns all translation models available"""
        return {"models": [model["name"] for model in MODELS.values()]}
    
