from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from transformers import MarianMTModel, MarianTokenizer
from models.model import translate_text , MODELS , mark_model_used
# from restapi_server import route


app = Flask(__name__)
api = Api(app, version='1.0', title='Translation service', description='An API for text translation')


from restapi_server import route
# MODEL_NAME = "ckartal/turkish-to-english-finetuned-model"
# tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
# model = MarianMTModel.from_pretrained(MODEL_NAME)

