#  AUDIT LOG SERVICE

## Project Description

The **Audit Log Microservice API System** is a versatile and robust solution for recording and managing various types of events sent by other systems. The service will accept event data sent by other systems and provide an HTTP endpoint for querying recorded event data by field values. This service is write-intensive.

## Key Features

**Event Recording**: The service is designed to record a wide range of events.

**Open-Ended Event Types**: The service accommodates an open-ended list of event types. It enforces a structure where all events contain a common set of fields along with event-specific data. This flexibility allows the service to adapt to new event types without requiring code modifications.

**Authentication**: To ensure data security, the service incorporates authentication mechanisms for both event submission and querying endpoints. This guarantees that only authorized users can interact with the service.

**Microservice Architecture**: The Audit Log Microservice is designed to be a lightweight and efficient microservice. It runs as an HTTP server, making it easy to integrate into your existing system architecture.


## Technologies Used

**Python:** Chose Python for its readability, extensive ecosystem, and ease of use, aligning with the project's goal of clean and maintainable code.

**Flask:** Utilized Flask as it's a lightweight Python web framework, perfect for building microservices like this one.

**MongoDB:** Opted for MongoDB for its flexibility and scalability, fitting the open-ended event types and accommodating different data storage needs.

**JWT (JSON Web Tokens):** Employed JWT for authentication to ensure secure access to event submission and querying endpoints, in line with the project's security focus.

**Docker**: Utilized Docker to containerize the application, simplifying deployment and ensuring consistency across different environments.

**Gunicorn**: Gunicorn serves as the WSGI HTTP server, making the application production-ready with multi-worker support.

## Usage

### Authentication

Authentication in this project is implemented using the following functions and components from the *login.py* and *JWTAuthentication.py* file:

***SignIn(app):*** 
This function defines the /login endpoint, allowing users to log in by sending a POST request with their username and password.

***@JWTtoken():*** 
This decorator is applied to endpoints that require authentication, ensuring that only users with valid JWTs can access them.

### Submitting Events

Event submission in this project involves the following functions and components from the *routes.py* file:

***@main_bp.route('/event', methods=['POST']):***
 This route handles event submission through HTTP POST requests and used with the next function.

***POSTSERVICE(user_id):***
This function is the handler for event submission. It validates incoming event data against the defined JSON schema and inserts the event into the MongoDB database.

### Querying Events

Querying events in this project involves the following functions and components from the *routes.py* file:

***@main_bp.route('/event', methods=['GET']):*** 
This route handles event querying through HTTP GET requests and used with the next function.

***GETSERVICE(user_id):*** 
This function is the handler for event querying. It constructs a query based on the provided query parameters (e.g., event type, username) and retrieves matching events from the MongoDB database.

### Schema
The Schema for the events is found in the mainfiles folder named Schema.json:

Here is an sample of how it'd look like

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


**What's Required (Invariant Data):**

*event_type:* A string specifying the type of the event.
*username:* A string representing the username associated with the event.
*entitytype:* A string indicating the type of entity involved in the event (e.g., customer, resource).
*ip:* A string representing the IP address associated with the event.
*location:* A string describing the location or context of the event.
*description:* A string providing a description or summary of the event.

**What Isn't Required (Variant Data):**

*event_specificdetails:* An optional object that allows for additional event-specific data. This field is open-ended and can vary based on the type of event being recorded. It's not required but allows for flexibility to capture event-specific information.

This schema ensures that all events must include the invariant data fields, guaranteeing a consistent structure. 

## Getting Started

### A. Prerequisites

To run this project , the following is required:
 

 **1. Docker Desktop**

 Docker Desktop is required to build and run the Docker container that encapsulates your application and its dependencies.

 **2. Python ( version 3.x or later)**
 Python is needed to execute the project code, particularly when running and testing the application locally.

 **4. Cloning the git project**

     git clone https://github.com/Eman-998/Audit-Log-Service.git

 
 **5.  Generating an .env file**

After cloning the project, start the terminal. Make sure that you are in root of  Audit-Log-Service project. Then run the following commands:

    $ chmod +x setup-env.sh
    $ ./setup-env.sh

This runs a bash script that will generate a .env file with the required environment variables required for the project. 

You will now be prompted to enter a username and password. Enter as per your wish. The username and passowrd will then be stored in the environment variables.
 
### B. Deployment
To deploy the project, ensure that you are at the root of the project directory. The entire project will be deployed with the following command:

    docker-compose up -d

After the containers have been built, The service will be tested in the terminal. Sometimes, environment variables aren't loaded properly so next run the following command:

    source .env

### C. Testing

#### System Check

    curl --request GET --url "http://localhost:8080/" 
    
#### Obtaining a BEARER_TOKEN for user

    BEARER_TOKEN=$(curl --request POST --url "http://localhost:8080/login" --header "Content-Type: application/json" --data 
    '{
      "username": "'$USERNAME'",
      "password": "'$PASSWORD'"
    }' | jq -r '.token')

This is crucial as every post and get request requies a bearer token
#### Posting Events


Example: A new customer account was created for John Mayor

    curl --request POST --url "http://localhost:8080/event" \
    --header "Authorization: Bearer: $BEARER_TOKEN" \
    --header "Content-Type: application/json" \
    --data '{
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
    }'

Example: A customer performed an action on a resource

    curl --request POST --url "http://localhost:8080/event" \
    --header "Authorization: Bearer: $BEARER_TOKEN" \
    --header "Content-Type: application/json" \
    --data '{
      "event_type": "ResourceAction",
      "username": "alice_smith",
      "entitytype": "resource",
      "ip": "192.168.0.2",
      "location": "Los Angeles",
      "description": "A customer performed an action on a resource",
      "event_specificdetails": {
        "resource_id": "456789",
        "action": "update",
        "timestamp": "2023-08-21T12:00:00"
      }
    }'

Example: A customer was billed a certain amount 

    curl --request POST --url "http://localhost:8080/event" \
    --header "Authorization: Bearer: $BEARER_TOKEN" \
    --header "Content-Type: application/json" \
    --data '{
      "event_type": "billing",
      "username": "bob_johnson",
      "entitytype": "customer",
      "ip": "192.168.0.3",
      "location": "Chicago",
      "description": "A customer was billed a certain amount",
      "event_specificdetails": {
        "amount": 100.0,
        "currency": "USD",
        "billing_date": "2023-08-22"
      }
    }'

Example: A customer account was deactivated

    curl --request POST --url "http://localhost:8080/event" \
    --header "Authorization: Bearer: $BEARER_TOKEN" \
    --header "Content-Type: application/json" \
    --data '{
      "event_type": "account_deactivation",
      "username": "bob_johnson",
      "entitytype": "customer_account",
      "ip": "192.168.0.3",
      "location": "Chicago",
      "description": "A customer account was deactivated",
      "event_specificdetails": {
        "reason": "Account closed by request",
        "deactivation_date": "2023-08-25"
      }
    }'

Example: A customer was billed a certain amount 

    curl --request POST --url "http://localhost:8080/event" \
    --header "Authorization: Bearer: $BEARER_TOKEN" \
    --header "Content-Type: application/json" \
    --data '{
      "event_type": "billing",
      "username": "david_smith",
      "entitytype": "customer",
      "ip": "192.168.0.6",
      "location": "Los Angeles",
      "description": "A customer was billed a certain amount",
      "event_specificdetails": {
        "amount": 75.5,
        "currency": "USD",
        "billing_date": "2023-08-21"
      }
    }'

#### Querying Events

**Retrieving all events**

    curl --request GET --url "http://localhost:8080/event" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .

**Query on Variant Fields Only:**

*Example 1: Query events where the event_specificdetails include a "resource_id" of "456789"*

    curl --request GET --url "http://localhost:8080/event?event_specificdetails.resource_id=456789" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .

*Example 2: Query events where the event_specificdetails include an "action" of "update"*

    curl --request GET --url "http://localhost:8080/event?event_specificdetails.action=update" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .

*Example 3: Query events where the event_specificdetails include a "billing_date" of "2023-08-25"*

    curl --request GET --url "http://localhost:8080/event?event_specificdetails.billing_date=2023-08-25" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .

**Query on Invariant Fields Only :**

*Example 4: Query events with an "event_type" of "account_created"*

    curl --request GET --url "http://localhost:8080/event?event_type=account_created" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .

*Example 5: Query events with a "username" of "john_mayor"*

    curl --request GET --url "http://localhost:8080/event?username=john_mayor" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .

*Example 6: Query events with an "ip" of "192.168.0.1"*

    curl --request GET --url "http://localhost:8080/event?ip=192.168.0.1" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .

**Query on Both Variant and Invariant Fields:**

*Example 7: Query events with an "event_type" of "account_created" and a "location" of "New York"*

    curl --request GET --url "http://localhost:8080/event?event_type=account_created&location=New%20York" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .

*Example 8: Query events with an "event_type" of "billing" and an "amount" of 100.0*

    curl --request GET --url "http://localhost:8080/event?event_type=billing&event_specificdetails.amount=100.0" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .

*Example 9: Query events with a "username" of "alice_johnson" and a "description" containing "created*"

    curl --request GET --url "http://localhost:8080/event?username=alice_johnson&description=created" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .


## Rationale and Trade-offs

## Future Plans





