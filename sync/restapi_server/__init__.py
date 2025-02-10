from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Translation service', description='An API for text translation')


from restapi_server import route


