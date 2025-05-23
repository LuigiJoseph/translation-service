from flask import request
from flask_restx import Resource, fields , Namespace


from python_services.sync.translation_methods import MODEL_HANDLERS , translate_with_cache

api = Namespace("translation-endpoints", description="Translation controller")
translation_model = api.model('TranslationRequest', {
'text': fields.String(required=True, description='Text to be translated'),
'model': fields.String(required=True, description='Translation model to use (helsinki, qwen)'),
'source_locale': fields.String(required=True, description='Source Locale'),
'target_locale': fields.String(required=True, description='Target Locale'),

})

# METHOD = POST -> Translation
@api.route("/api/v1/translate")
class TranslateResource(Resource):

    @api.expect(translation_model)
    @api.doc(responses={
        200: 'Success',
        201: 'Created',
        400: 'Bad Request',
        500: 'Internal Server Error' 
    })
    def post(self):
        """Translate text from one language to another"""
        data = request.json
        text = data.get("text")
        model_name = data.get("model")
        source_locale = data.get("source_locale")
        target_locale = data.get("target_locale")

        if any(value in ["string", ""] for value in data.values()):
            return {"error": "Invalid input values"}, 400
        

        model_name = model_name.lower()
        if model_name not in MODEL_HANDLERS:
            return {"error": f"Model '{model_name}' is not supported."}, 400
        

        translated_text = translate_with_cache(text, source_locale, target_locale, model_name)
            
        return {
                    "source_text":text,
                    "source_language": source_locale,
                    'target_language': target_locale,
                    "model_used": model_name,
                    "translated_text": translated_text
                }, 200


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

    
