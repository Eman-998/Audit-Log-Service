"""
Created on Tue Aug 16 13:05:56 2023

@author: Emaan Shahzad
"""

# Libraries
import jwt 
from datetime import datetime, timedelta
from flask import jsonify, request, make_response 

# Login endpoint
def SignIn(app):
    @app.route('/login', methods=['POST'])
    def login():
        try:
            infos = request.get_json()

            # Check if both "username" and "password" are present in the request
            if 'username' not in infos or 'password' not in infos:
                return make_response('Bad Request: Missing username or password', 400)

            # Validates username and password
            if infos['username'] == app.config['USER'] and infos['password'] == app.config['PASS']:
                token = jwt.encode(
                    {
                        'user':infos['username'],
                        'expiration':(datetime.now() + timedelta(seconds=3600)).isoformat()
                    },
                    app.config['SECRET_KEY'],
                    algorithm="HS256"
                )
                return jsonify({'token': token})
            else:
                return make_response('Unauthorized: Invalid credentials', 403)
        # Handle exceptions
        except Exception as e:
           return make_response(e.message, 500)