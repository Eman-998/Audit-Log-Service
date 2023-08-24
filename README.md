# AUDIT LOG SERVICE

## Project Description

The Audit Log Microservice API is a versatile and robust solution for recording and managing various types of events sent by other systems. The service will accept event data sent by other systems and provide an HTTP endpoint for querying recorded event data by field values. This service is write-intensive.

## Key Features 

*Event Recording: The service is designed to record a wide range of events, including but not limited to:

Creation of new customer accounts for a given identity.
Customer actions on specific resources.
Billing events, including the amount billed.
Customer account deactivation.

*Open-Ended Event Types: The service accommodates an open-ended list of event types. It enforces a structure where all events contain a common set of fields along with event-specific data. This flexibility allows the service to adapt to new event types without requiring code modifications.

*Authentication: To ensure data security, the service incorporates authentication mechanisms for both event submission and querying endpoints. This guarantees that only authorized users can interact with the service.

*Microservice Architecture: The Audit Log Microservice is designed to be a lightweight and efficient microservice. It runs as an HTTP server, making it easy to integrate into your existing system architecture.

## Technologies Used

Python: Chose Python for its readability, extensive ecosystem, and ease of use, aligning with the project's goal of clean and maintainable code.

Flask: Utilized Flask as it's a lightweight Python web framework, perfect for building microservices like this one.

MongoDB: Opted for MongoDB for its flexibility and scalability, fitting the open-ended event types and accommodating different data storage needs.

JWT (JSON Web Tokens): Employed JWT for authentication to ensure secure access to event submission and querying endpoints, in line with the project's security focus.

Docker: Utilized Docker to containerize the application, simplifying deployment and ensuring consistency across different environments.

Gunicorn: Gunicorn serves as the WSGI HTTP server, making the application production-ready with multi-worker support.

## Usage

### Authentication

Authentication in this project is implemented using the following functions and components from the provided code:

User Registration and Login (login.py):

SignIn(app): This function defines the /login endpoint, allowing users to log in by sending a POST request with their username and password.
JWT Authentication (JWTauthentication.py):

JWTtoken(): This function is a decorator used to protect endpoints that require authentication. It verifies JWTs sent in the Authorization header of incoming requests.
Authentication Integration (routes.py):

@JWTtoken(): This decorator is applied to endpoints that require authentication, ensuring that only users with valid JWTs can access them.
These functions and components work together to provide secure authentication and authorization for the service, allowing registered users to obtain and use JWTs for accessing protected endpoints.

### Submitting Events

Event submission in this project involves the following functions and components from the provided code:

1.Event Submission (routes.py):

@main_bp.route('/event', methods=['POST']): This route handles event submission through HTTP POST requests.

POSTSERVICE(user_id): This function is the handler for event submission. It validates incoming event data against the defined JSON schema and inserts the event into the MongoDB database.

2.JSON Schema Validation (routes.py):

jsonschema.validate(data, json_schema): This function validates incoming event data against the JSON schema defined in Schema.json. It ensures that submitted events adhere to the required structure.

3.MongoDB Integration (routes.py):

MongoDB is used to store event data in the events collection. The code uses the pymongo library to interact with the MongoDB database.
These functions and components collectively enable the secure submission of events to the service, ensuring that only authenticated users can add events that comply with the defined JSON schema.

### Querying Events

Querying events in this project involves the following functions and components from the provided code:

Event Querying (routes.py):

@main_bp.route('/event', methods=['GET']): This route handles event querying through HTTP GET requests.
GETSERVICE(user_id): This function is the handler for event querying. It constructs a query based on the provided query parameters (e.g., event type, username) and retrieves matching events from the MongoDB database.
MongoDB Integration (routes.py):

MongoDB is used to store event data in the events collection. The code uses the pymongo library to interact with the MongoDB database.
Query Parameter Parsing (routes.py):

The function parses query parameters from the HTTP request to construct a query for event retrieval. Parameters such as event_type, username, entitytype, ip, location, description, timeStart, and timeEnd can be used to filter events.
These functions and components collectively enable users to query events based on specific criteria, providing a flexible and powerful way to retrieve event data from the service.

### Schema
The Schema for the events is found in the mainfiles folder named Schema.json:

Here is an sample of how itd look like


{
  "event_type": "AccountCreated",
  "username": "john_mayor",
  "entitytype": "customer_account",
  "ip": "192.168.0.1",
  "location": "New York",
  "description": "A new customer account was created for John Mayor",
  "event_specificdetails": {
    "account_number": "94859",
    "email": "john@gmail.com"
  }
}


What's Required (Invariant Data):

event_type: A string specifying the type of the event.
username: A string representing the username associated with the event.
entitytype: A string indicating the type of entity involved in the event (e.g., customer, resource).
ip: A string representing the IP address associated with the event.
location: A string describing the location or context of the event.
description: A string providing a description or summary of the event.

What Isn't Required (Variant Data):

event_specificdetails: An optional object that allows for additional event-specific data. This field is open-ended and can vary based on the type of event being recorded. It's not required but allows for flexibility to capture event-specific information.
This schema ensures that all events must include the invariant data fields, guaranteeing a consistent structure. The event_specificdetails field provides the flexibility needed to accommodate variant data specific to each event type.
## Getting Started

### Installation

#### Prerequisites

To run this project , the following is required:
 
1.Docker Desktop: Docker Desktop is required to build and run the Docker container that encapsulates your application and its dependencies.

2.Python ( version 3.x or later): Python is needed to execute the project code, particularly when running and testing the application locally.
#### Deployment
- Deployment instructions

#### Testing
- Instructions for running tests

##### Registering a user
##### Logging a user
##### Obtaining a BEARER_TOKEN for user
-expires when
##### Posting Events
##### Querying Events


## Rationale and Trade-offs

## Future Plans
