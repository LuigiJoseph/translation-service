from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from transformers import MarianMTModel, MarianTokenizer
from model import translate_text
import uuid

app = Flask(__name__)
api = Api(app, version='1.0', title='Translation service', description='An API for text translation')

# MODEL_NAME = "ckartal/turkish-to-english-finetuned-model"
# tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
# model = MarianMTModel.from_pretrained(MODEL_NAME)

translation_model = api.model('TranslationRequest', {
    'source_locale': fields.String(required=True, description='Source language'),
    'target_locale': fields.String(required=True, description='Target language'),
    'text': fields.String(required=True, description='Text to translate')
})

@api.route("/translate")
class TranslateResource(Resource):
    
    @api.expect(translation_model)
    @api.doc(responses={
        200: 'Success',
        400: 'Bad Request'
    })
    def post(self):
        #Description
        """Translate text from one language to another"""
        request_id = str(uuid.uuid4())
        data = request.json
        source_lang = data.get("source_locale")
        target_lang = data.get("target_locale")
        text = data.get("text")
        
        if not source_lang or not target_lang or not text:
            return {"error": "Missing required parameters"}, 400
        
        # Perform translation using the model
        translated_text = translate_text(text)
        
        return {"request_id": request_id,
            "translated_text": translated_text}

# @api.route("/languages")
# class Languages(Resource):
#     def get(self):
#         """This returns sopported languages"""
#         return {"languages" : ["tr" , "en"]}
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)