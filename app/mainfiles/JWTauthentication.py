"""
Created on Tue Aug 21 16:08:56 2023

@author: Eman's PC
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
            app = current_app  # Get the current Flask application instance

            token = None
            # Check if the Authorization header is present and extract it
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer:'):
                    token = auth_header[7:].strip()

            if not token:
                return make_response('Unauthorized: Token is missing', 403)
            try:
                payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

                # Verify expiration
                expiration_str = payload['expiration']
                expiration_dt = datetime.strptime(expiration_str, '%Y-%m-%dT%H:%M:%S.%f')
                expiration_timestamp = int(expiration_dt.timestamp())
                if expiration_timestamp < datetime.utcnow().timestamp():
                    raise ExpiredSignatureError
                
                # Pass the user ID as an argument to the endpoint function
                kwargs['user_id'] = payload['user']

            except ExpiredSignatureError:
                return make_response('Unauthorized: Token expired', 403)
            except:
                return make_response('Unauthorized: Invalid Token', 403)
            
            return func(*args, **kwargs)
        return decorated
    return decorator
