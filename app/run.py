"""
Created on Tue Aug 14 03:58:39 2023

This is the entry point of the application. 
It initializes the Flask app, configures it, and runs it using Gunicorn.
"""
# Import necessary libraries and modules.
from flask import Flask
from pymongo import MongoClient
from mainfiles import login
from mainfiles.routes import main_bp
from mainfiles.config import settings

# Create a Flask app instance.
app = Flask(__name__)

# Configure the app by calling the settings function from config.py.
settings(app)

# Set up user login and authentication by calling SignIn function from login.py.
login.SignIn(app)

# Initialize the MongoDB client and store it in the app context.
app.mongo_client = MongoClient(app.config['MONGODBATLAS_HOST'])

# Register the API routes defined in main_bp from routes.py.
app.register_blueprint(main_bp)

# Start the Flask app.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
