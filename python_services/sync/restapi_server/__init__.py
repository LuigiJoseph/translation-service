from flask import Flask
from flask_restx import Api
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://frontend:3000"]}})


api = Api(app, version='1.0',validate=True, title='Translation Service', description='An API for text translation')
    
from python_services.sync.restapi_server.route import api as translation_ns 
api.add_namespace(translation_ns)
 




