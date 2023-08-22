"""
Created on Tue Aug 16 13:05:56 2023

@author: Emaan Shahzad
"""

# Libraries
from flask import jsonify, request

# Handle 404 errors thrown
def handle_not_found(app):
    @app.errorhandler(404)
    def not_found(error=None):
        message = {
                'status': 404,
                'message': 'Not Found: ' + request.url,
        }
        resp = jsonify(message)
        resp.status_code = 404

        return resp

# TODO: Handle 5XX errors thrown