"""
Created on Wed Aug 23 02:39:23 2023

Description: 
    The function SignIn defines a route for user login, where it authenticates a user
    and generate a JSON Web Token (JWT) for authorization.

Args:
    app (Flask): The Flask application instance. It is used to define routes
    and handle HTTP requests.

Returns:
    flask.Response: A JSON response containing a JWT token upon successful authentication.
    
Raises:
    401 Unauthorized: If the client's credentials are missing or invalid.
    500 Internal Server Error: If there's an unexpected error during the process.

API Endpoint:
    POST /login

Notes:
    - This endpoint allows users to log in by providing a valid username and password.
    - If authentication is successful, a JWT token is generated and returned.
    - The JWT token is used for subsequent authenticated API requests.

"""
# Libraries
import jwt 
from datetime import datetime, timedelta
from flask import jsonify, request, make_response 

# TODO: To enhance security, omplement password hashing
def SignIn(app):
    @app.route('/login', methods=['POST'])
    def login():
        # The code block you provided is a function called `login()` that handles user login and JWT
        # token generation. Here's a breakdown of what it does:
        try:
            data = request.get_json()

            # Check if both "username" and "password" are present in the request
            if 'username' not in data or 'password' not in data:
                # This returns a response indicating a status code of 401, which means that 
                # the request requires authentication and the client's credentials are missing.
                return make_response('Bad Request: Missing username or password', 401)

            # Validates username and password
            if data['username'] == app.config['USERNAME'] and data['password'] == app.config['PASSWORD']:
                # Generate a JWT token.
                token = jwt.encode(
                    {

                        #TODO: Implement token refresh mechanisms to ensure continued access without requiring frequent logins
                        'user':data['username'],
                        'expiration':(datetime.now() + timedelta(seconds=1800)).isoformat()
                    },
                    app.config['SECRET_KEY'],
                    algorithm="HS256"
                )
                return jsonify({'token': token})
            else:
                # This returns a response indicating a status code of 401, which means that 
                # the request requires authentication and the client's credentials are invalid.
                return make_response('Username or Password is incorrect', 401)
        # Handle exceptions
        except Exception as e:
        # The line `return make_response(e.message, 500)` is returning a response with an error message and a
        # status code of 500 (Internal Server Error).
           return make_response(e.message, 500)