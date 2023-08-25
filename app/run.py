"""
Created on Tue Aug 14 03:58:39 2023

This is the entry point of the application. 
It initializes the Flask app, configures it, and runs it using Gunicorn.
"""
# Import necessary libraries and modules.
import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient
from mainfiles import login
from mainfiles.routes import main_bp

# Create a Flask app instance.
app = Flask(__name__)


#TODO: In a production environment, using a more robust configuration management system, 
#      such as Python's configparser or third-party libraries like python-decouple, can provide
#      better separation of configuration from code.

app.config.from_object(__name__)

# Load environment variables from .env file into Flask app
load_dotenv()

app.config['USERNAME'] = os.environ.get('USERNAME')
app.config['PASSWORD'] = os.environ.get('PASSWORD')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MONGODBATLAS_HOST'] = os.environ.get('MONGODBATLAS_HOST')

# Set up user login and authentication by calling SignIn function from login.py.
login.SignIn(app)

# Initialize the MongoDB client and store it in the app context.
app.mongo_client = MongoClient(app.config['MONGODBATLAS_HOST'])

# Register the API routes defined in main_bp from routes.py.
app.register_blueprint(main_bp)

# Start the Flask app.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
