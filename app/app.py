# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 03:58:39 2023

@author: Eman's PC
"""
# Libraries
import os
from flask import Flask
from pymongo import MongoClient
from waitress import serve
from mainfiles import config
from mainfiles import JWTauthentication
from mainfiles import login
from mainfiles import routes
from mainfiles.routes import main_bp


# Create a context manager for MongoDB client
class MongoDBManager:
    def __init__(self, app):
        self.app = app

    def __enter__(self):
        self.app.mongo_client = MongoClient(self.app.config['MONGODBATLAS_HOST'])
        return self.app.mongo_client

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self.app, 'mongo_client'):
            self.app.mongo_client.close()
            del self.app.mongo_client


# instantiate the app
app = Flask(__name__)

#CONFIGURATION TO PLACE ELSEWHERE
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['USER'] = os.environ.get('USER')
app.config['PASS'] = os.environ.get('PASS')
app.config['MONGODBATLAS_HOST'] = os.environ.get('MONGODBATLAS_HOST')

#User logging in
login.SignIn(app)

#JWTAuthentication is done in routes.py

# Use MongoDB client to get message from MongoDB database
app.mongo_manager = MongoDBManager(app)

# POST event and GET event is done
app.register_blueprint(main_bp)

# Use MongoDB manager as a context manager
with app.mongo_manager:
    # Start the Flask app
    if __name__ == '__main__':
        serve(app, host="0.0.0.0", port=5000)