
"""
Created on Tue Aug 15 04:05:38 2023
This script defines the API endpoints for submitting and retrieving events. 
"""
#Submitting an event

"""
Description: 
    This endpoint posts a new event  using the POSTSERVICE function. The /event POST route uses the
    JWTtoken decorator to enforce authenticationpassed in the Authorization header. The route validates incoming event data against a 
    JSON schema defined in Schema.json. It logs the event in MongoDB and returns a response.

Args:
    user_id (str): The user ID extracted from the JWT token.

Returns:
    flask.Response: A JSON response confirming the successful submission of the event.
    
Raises:
    400 Bad Request: If the submitted event data does not conform to the expected schema.
    500 Internal Server Error: If there's an unexpected error during the process.

API Endpoint:
    POST /event

"""

#Posting an event

"""
    Description: 
        This endpoint retrieves events from the audit log service using the GETSERVICE function. The /event GET route 
        enforces authentication using JWT token passed in the Authorization header.It allows querying 
        events based on various parameters like event_type, username, entitytype, etc. It fetches events
        from MongoDB and returns them as JSON.

    Args:
        user_id (str): The user ID extracted from the JWT token.

    Returns:
        flask.Response: A JSON response containing the retrieved events.
        
    Raises:
        500 Internal Server Error: If there's an unexpected error during the process.

    API Endpoint:
        GET /event

    Query Parameters:
        - event_type (str, optional): Filter events by event type.
        - username (str, optional): Filter events by username.
        - entitytype (str, optional): Filter events by entity type.
        - ip (str, optional): Filter events by IP address.
        - location (str, optional): Filter events by location.
        - description (str, optional): Filter events by description.
        - timeStart (float, optional): Filter events with a timestamp greater than or equal to this value.
        - timeEnd (float, optional): Filter events with a timestamp less than or equal to this value.
"""

# Libraries
import os, json, jsonschema, time
from flask import jsonify, request, make_response
from mainfiles.JWTauthentication import JWTtoken
from flask import Blueprint, current_app

# The main blueprint that organizes and groups audit log service-related routes.
main_bp = Blueprint('endpoints', __name__)

#This endpoint provides a basic welcome message for users visiting the service.
@main_bp.route('/')
def auditlogentrypage():
    return 'Welcome to the Audit logging System.'


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
       
       # Create a response message with the beautified event data
        message = {
            'message': f'The event is submitted by user {data["username"]} and the event logged is of type {data["event_type"]}:',
            'status': 201,
        }
        
        resp = jsonify(message)
        resp.status_code = 201
        return resp

    except jsonschema.exceptions.ValidationError as e:
        error_message = e.message
        return make_response(error_message, 400)
    
    except Exception as e: 
        return jsonify({
            "error": f"{e}"
        })
        
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

        # Set event_type to the event_type argument.
        if 'event_type' in args:
            query['event_type'] = args['event_type']

        # Set username to query. username
        if 'username' in args:
            query['username'] = args['username']

        # Set the entity type of the query.
        if 'entitytype' in args:
            query['entitytype'] = args['entitytype']

        # Set the ip of the query
        if 'ip' in args:
            query['ip'] = args['ip']

        # Set the location of the query.
        if 'location' in args:
            query['location'] = args['location']

        # Set the description of the query.
        if 'description' in args:
            query['description'] = args['description']

        query['user_id'] = user_id

        # Set the timestamp and start time
        if 'timeStart' in args or 'timeEnd' in args:
            timestamp_query = {}
            # Set the time start time of the query
            if 'timeStart' in args:
                timestamp_query['$gte'] = float(args['timeStart'])
            # Set the time end of the query
            if 'timeEnd' in args:
                timestamp_query['$lte'] = float(args['timeEnd'])
            query['timestamp'] = timestamp_query

        events = list(collection.find(query))

        # Add the event id to the event s _id
        for event in events:
            event['_id'] = str(event['_id'])

        response = jsonify(events)
        response.indent = 2  
        return response

    # Return 500 if there was an error while trying to create a resource. \
    except Exception as e:
        return make_response(json.dumps({"error": str(e)}), 500)

