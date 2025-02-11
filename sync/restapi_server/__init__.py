from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields


# def create_app():
app = Flask(__name__)
api = Api(app, version='1.0', title='Translation service', description='An API for text translation')
    
from restapi_server.route import api as translation_ns 
api.add_namespace(translation_ns)
 # return api





