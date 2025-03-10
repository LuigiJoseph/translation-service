from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields


app = Flask(__name__)
api = Api(app, version='1.0',validate=True, title='Translation service', description='An API for text translation')
    
from python_services.sync.restapi_server.route import api as translation_ns 
api.add_namespace(translation_ns)
 




