"""
config.py

Description:
    This configures the Flask application with settings required for the Audit Log Service. It
    sets values for the secret key, user credentials, and MongoDB host from environment variables.

Args:
    app (Flask): The Flask application instance to be configured.

"""
# Libraries
import os
from pymongo import MongoClient

# Define a function to configure the app.

def settings(app):  
    app.config.from_object(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['USER'] = os.environ.get('USER')
    app.config['PASS'] = os.environ.get('PASS')
    app.config['MONGODBATLAS_HOST'] = os.environ.get('MONGODBATLAS_HOST')

    

