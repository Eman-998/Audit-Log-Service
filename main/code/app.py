# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 03:58:39 2023

@author: Eman's PC
"""
# Libraries
import os, sys
from flask import Flask 
import secrets 
from api.src.helpers.authentication import * 
from api.src.helpers.routing import * 
from api.src.helpers.errors import * 
from pymongo import MongoClient
# instantiate the app
app = Flask(__name__)
#place these configs in docker when created
app.config.from_object(__name__) 
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['USER'] = os.environ.get('USER')
app.config['PASS'] = os.environ.get('PASS')
app.config['MONGODBATLAS_HOST'] = os.environ.get('MONGODBATLAS_HOST')
#setup authentication authenticate(app) 
#setup clients and endpoints
# Use MongoDB client to get message from MongoDB database 
mongo_client = MongoClient(app.config['MONGODB_HOST'])
# POST event
post_event(app, mongo_client) 
# GET event
get_event(app, mongo_client) 
# Closing MongoDB connection
#setup errors
handle_not_found(app)
@app.route('/health')
def health_check(): 
    return 'OK' 
if __name__ == '__main__': 
    from gunicorn.app.wsgiapp import run
    run()
