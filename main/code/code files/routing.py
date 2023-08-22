
"""
Created on Tue Aug 15 04:05:38 2023

@author: Eman's PC
"""

# Libraries
import os, json, jsonschema, time
from flask import jsonify, json, request, make_response
from pymongo import MongoClient
from bson import ObjectId

# Post a new event to the service
def post_event(app, mongo_client):
    @app.route('/event', methods=['POST'])
    def push_message(user_id):
        timestamp = time.time()
        try:
            data = request.get_json()

            json_dir = os.path.join(os.getcwd(), 'schemas')
            json_file_path = os.path.join(json_dir, 'event_schema.json')
            with open(json_file_path) as file:
                json_schema = json.load(file)
            jsonschema.validate(data, json_schema)
            print("Data is valid according to the schema.")   
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
            db = mongo_client['audit_log_db']
            collection = db['events']
            # Store the message in MongoDB
            collection.insert_one(event)

            message = {
                'status': 200,
                'message': 'Event submitted',
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
def get_event(app, mongo_client):
    @app.route('/event', methods=['GET'])
    def get_events(user_id):
        try:
            # Extract parameters and prepare for query
            args = request.args
            # Find our events table in MongoDB
            db = mongo_client['audit_log_db']
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

            app.logger.info(f"GET events from user: {user_id}. Query: {query}")
            return jsonify(events)

        except Exception as e:
            return make_response(json.dumps({"error": str(e)}), 500)
