
"""
Created on Tue Aug 15 04:05:38 2023
@author: Eman's PC

DESCRIPTION: 
    This Python script defines and handles HTTP POST and GET requests for managing audit log events. 
    It uses JWTToken from JWTAuthentication to ensure that the token is present and valid 
    before posting and getting and event.
    It uses Blueprint......

"""

# Libraries
import os, json, jsonschema, time
from flask import jsonify, request, make_response
from mainfiles.JWTauthentication import JWTtoken
from flask import Blueprint, current_app

main_bp = Blueprint('endpoints', __name__)

@main_bp.route('/')
def auditlogentrypage():
    return 'Welcome to the Audit logging System.'

# Post a new event to the service
@main_bp.route('/event', methods=['POST'])
@JWTtoken()   
def POSTSERVICE(user_id):
    timestamp = time.time()
    try:
        data = request.get_json()
        
        current_dir = os.path.join(os.getcwd(), 'mainfiles')
        json_file_path = os.path.join(current_dir, 'Schema.json')

        with open(json_file_path) as file:
            json_schema = json.load(file)
        jsonschema.validate(data, json_schema)

        # Access user_id from the token payload
        custom_id = f"{user_id}_{timestamp}"
        event = {
              "_id": custom_id,
              "event_type": data["event_type"],
              "username": data["username"],
              "entitytype": data["entitytype"],
              "ip": data["ip"],
              "location": data["location"],
              "description": data["description"],
              "event_specificdetails": data.get("event_specificdetails", {}),
              "user_id": user_id,
              "timestamp": timestamp,
          }

        # Use the passed mongo_client for database operations
        db = current_app.mongo_client['audit_log_db']
        collection = db['events'] 
        
        # Store the message in MongoDB
        collection.insert_one(event)
       
        # Beautify the event data
        event_pretty_json = json.dumps(event, indent=2)
        

       # Create a response message with the beautified event data
        message = {
            'message': 'The following event has been posted:',
            'event': json.loads(event_pretty_json)  # Convert the beautified JSON back to a dictionary
        }
        
        resp = jsonify(message)
        resp.status_code = 200
        return resp

    except jsonschema.exceptions.ValidationError as e:
        error_message = e.message
        return make_response(error_message, 400)
    
    except Exception as e: 
        return jsonify({
            "error": f"{e}"
        })
        
# Retrieve events from the service
@main_bp.route('/event', methods=['GET'])
@JWTtoken()
def GETSERVICE(user_id):
    try:

        # Extract parameters and prepare for query
        args = request.args
        # Find our events table in MongoDB
        db = current_app.mongo_client['audit_log_db']
        collection = db['events']
        # Narrow down the results based on the parameters passed
        query = {}

        if 'event_type' in args:
            query['event_type'] = args['event_type']

        if 'username' in args:
            query['username'] = args['username']

        if 'entitytype' in args:
            query['entitytype'] = args['entitytype']

        if 'ip' in args:
            query['ip'] = args['ip']

        if 'location' in args:
            query['location'] = args['location']

        if 'description' in args:
            query['description'] = args['description']

        # Add user_id filter
        query['user_id'] = user_id

        # Query by timestamp range
        if 'timeStart' in args or 'timeEnd' in args:
            timestamp_query = {}
            if 'timeStart' in args:
                timestamp_query['$gte'] = float(args['timeStart'])
            if 'timeEnd' in args:
                timestamp_query['$lte'] = float(args['timeEnd'])
            query['timestamp'] = timestamp_query

        # Find events matching the query
        events = list(collection.find(query))

        # Convert ObjectId to string before JSON serialization
        for event in events:
            event['_id'] = str(event['_id'])
        # Create a response object with prettified JSON
        response = jsonify(events)
        response.indent = 2  # Set the desired indentation level (e.g., 2 spaces)
        return response

    except Exception as e:
        return make_response(json.dumps({"error": str(e)}), 500)
