
"""

Description: 
    The function acts as a middleware and defines a decorator generator for JWT-based authentication in Python.
    The decorator enforces JSON Web Token (JWT) authentication on Flask routes. When used on a route, it intercepts
    requests, validates the token, and provides user information to the route handler through the 'user_id' argument

Returns:
    function: A decorated route function that requires a valid JWT token for access.
    
Raises:
    401 Unauthorized: If the JWT token is missing or invalid.
    500 Internal Server Error: If there's an unexpected error during token decoding.

"""
# Libraries
import jwt 
from functools import wraps
from datetime import datetime
from jwt.exceptions import ExpiredSignatureError
from flask import request, make_response, current_app  


def JWTtoken():
  
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            app = current_app 

            token = None
            # Check if the Authorization header is present and extract it
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer:'):
                    token = auth_header[7:].strip()

            if not token:
                return make_response('Unauthorized: Token is missing', 401)
            try:
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

                # Verify expiration
                expiration_str = payload['expiration']
                expiration_dt = datetime.strptime(expiration_str, '%Y-%m-%dT%H:%M:%S.%f')
                expiration_timestamp = int(expiration_dt.timestamp())
                if expiration_timestamp < datetime.utcnow().timestamp():
                    raise ExpiredSignatureError
                
                kwargs['user_id'] = payload['user']

            except ExpiredSignatureError:
                return make_response('Unauthorized: Token expired', 401)
            except:
                return make_response('Unauthorized: Invalid Token', 401)
            
            return func(*args, **kwargs)
        return decorated
    return decorator

