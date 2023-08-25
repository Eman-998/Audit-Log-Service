#  AUDIT LOG SERVICE
 
# Table of contents 

###### [Project Description]

###### [Technologies Used]

###### [Design of Microservice API]

###### [Testing of Microservice API]

###### [Rationale and Trade-offs]

###### [Future Plans]

## Project Description

The **Audit Log Microservice API System** is a versatile and robust solution for recording and managing various types of events sent by other systems. The service will accept event data sent by other systems and provide an HTTP endpoint for querying recorded event data by field values. This service is write-intensive.

Examples of events recorded:

- a new customer account was created for a given identity
- a customer performed an action on a resource
- a customer was billed a certain amount
- a customer account was deactivated
  
The list of event types is open-ended, all events should contain a common set of fields and a set of fields specific to the event type. The code should not need to be modified for it to accept a new event type. Also note that this service is write-intensive.

## Technologies Used

**Python:** Chose Python for its readability, extensive ecosystem, and ease of use, aligning with the project's goal of clean and maintainable code.

**Flask:** Utilized Flask as it's a lightweight Python web framework, perfect for building microservices like this one.

**MongoDB:** Opted for MongoDBATLAS for its flexibility and scalability, fitting the open-ended event types and accommodating different data storage needs.

**JWT (JSON Web Tokens):** Employed JWT for authentication to ensure secure access to event submission and querying endpoints, in line with the project's security focus.

**Docker**: Utilized Docker to containerize the application, simplifying deployment and ensuring consistency across different environments.

**Gunicorn**: Gunicorn serves as the WSGI HTTP server, making the application production-ready with multi-worker support. This server currently runs 4 workers.

## Design of Microservice API

### Base URL

The base URL for this microservice is: `http://localhost:8080/`

### Authentication

The microservice uses JSON Web Token (JWT) authentication to secure its endpoints. To access protected endpoints, clients must include a valid JWT token in the `Authorization` header.  

### Error Responses

The API returns JSON error responses in the following format:

    {
      "error": "Error message here"
    }
    
### Endpoints

#### Welcome Message

-   **Endpoint**: `/`
-   **HTTP Method**: GET
-   **Description**: Provides a basic welcome message for users visiting the service.
-   **Authentication**: Not required
-   **Example**:
 `curl http://localhost:8080/`
 #### User Login

-   **Endpoint**: `/login`
-   **HTTP Method**: POST
-   **Description**: Allows users to log in by providing a valid username and password. If authentication is successful, a JWT token is generated and returned.
-   **Authentication**: Not required
-   **Request Body**:
````
{ 
		 "username":  "your_username",  
		 "password":  "your_password"  
 }
````
**Response**:

````
{  "token":  "generated_jwt_token"  }
````
#### Submitting an Event

-   **Endpoint**: `/event`
-   **HTTP Method**: POST
-   **Description**: Posts a new event to the audit log. The request body must conform to the JSON schema defined.
-   **Authentication**: Required (JWT token in `Authorization` header)
-   **Request Body**:
````
{  
"event_type":  "string",
"username":  "string",
"entitytype":  "string",  
"ip":  "string",  
"location":  "string",  
"description":  "string",  
"event_specificdetails":  {  
// Additional event-specific fields here 
(optional)  
	}  
}
````
- **Example**: 
````
will be shown through curl commands in the testing section
````
-   **Response**: Returns a confirmation message.
#### Retrieving Events

-   **Endpoint**: `/event`
-   **HTTP Method**: GET
-   **Description**: Retrieves events from the audit log based on query parameters.
-   **Authentication**: Required (JWT token in `Authorization` header)
-   **Query Parameters**:
    -   `event_type`
    -   `username` 
    -   `entitytype` 
    -   `ip`
    -   `location`
    -   `description`
    -   `timeStart` .
    -   `timeEnd` 
    
   - **Example**:
 ````
It will be shown through curl commands in the testing section
````
-   **Response**: Returns a JSON array containing retrieved events.
- 
### Schema
The Schema for the events is found in the mainfiles folder named Schema.json:

Here is an sample of how it would look like:

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

*event_specificdetails:* An optional object that allows for additional event-specific data. 

This schema ensures that all events must include the invariant data fields, guaranteeing a consistent structure. 

## Testing of Microservice API

### Prerequisites
To run this project , the following is required:
 
**1. Docker Desktop**

 Docker Desktop is required to build and run the Docker container that encapsulates your application and its dependencies.

 **2. Python ( version 3.x or later)**
 
 Python is needed to execute the project code, particularly when running and testing the application locally.

 **3. Cloning the git project**

     git clone https://github.com/Eman-998/Audit-Log-Service.git

 
 **4.  Generating an .env file**

After cloning the project, start the terminal. Make sure that you are in root of  Audit-Log-Service project. Then run the following commands:

     chmod +x setup-env.sh
     ./setup-env.sh

This runs a bash script that will generate a .env file with the required environment variables required for the project. 

You will now be prompted to enter a username and password. Enter as per your wish. The username and passowrd will then be stored in the environment variables.
 
### Deployment
To deploy the project, ensure that you are at the root of the project directory. The entire project will be deployed with the following single command on ubuntu :

    docker-compose up -d

After the containers have been built, The service will be tested in the terminal. 

Load the environment variables in the host terminal

    source .env

### Running

Now the service is up and running! To check if its live, run the following command:

    curl --request GET --url "http://localhost:8080/" 

Since ther service uses JWT Authetication, a bearer token is required to test the upcoming Curl commands.      
#### Obtain a BEARER_TOKEN for user
```
BEARER_TOKEN=$(curl --request POST --url "http://localhost:8080/login" --header "Content-Type: application/json" --data '{
  "username": "'$USERNAME'",
  "password": "'$PASSWORD'"
}' | jq -r '.token')
```


The token is generated and loaded into the BEARER_TOKEN variable. It is using a secret key which is generated randomly using SSL. 

##### *Note: To test with an invalid token, you can replace the values of BEARER_TOKEN with any other token value . Doing so will give an invalid token error*
##### *Note: The BEARER_TOKEN is valid for 30 minutes. 
#### Posting Events

In the terminal, please copy and post the following examples in the terminal.

*Example 1: A new customer account was created for user*

```
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

```
*Example 2: A customer was billed a certain amount* 

```
curl --request POST --url "http://localhost:8080/event" \
--header "Authorization: Bearer: $BEARER_TOKEN" \
--header "Content-Type: application/json" \
--data '{
  "event_type": "billing",
  "username": "john_mayor",
  "entitytype": "customer",
  "ip": "192.168.0.1",
  "location": "Chicago",
  "description": "A customer was billed a certain amount",
  "event_specificdetails": {
    "amount": 100.0,
    "currency": "USD",
    "billing_date": "2023-08-22"
  }
}'

```

*Example 3: A customer account was deactivated*

```
curl --request POST --url "http://localhost:8080/event" \
--header "Authorization: Bearer: $BEARER_TOKEN" \
--header "Content-Type: application/json" \
--data '{
  "event_type": "account_deactivation",
  "username": "alice_johnson",
  "entitytype": "customer_account",
  "ip": "192.168.0.3",
  "location": "Chicago",
  "description": "A customer account was deactivated",
  "event_specificdetails": {
    "reason": "Account closed by request",
    "deactivation_date": "2023-08-19"
  }
}'

```

*Example 4: A customer was billed a certain amount* 
```
curl --request POST --url "http://localhost:8080/event" \
--header "Authorization: Bearer: $BEARER_TOKEN" \
--header "Content-Type: application/json" \
--data '{
  "event_type": "billing",
  "username": "david_smith",
  "entitytype": "customer",
  "ip": "192.168.0.6",
  "location": "Dubai",
  "description": "A customer was billed a certain amount",
  "event_specificdetails": {
    "amount": 75.5,
    "currency": "AED",
    "billing_date": "2023-08-21"
  }
}'

```
#### Querying Events

##### **This retrieves all events avaible in the database**
```
curl -s --request GET --url "http://localhost:8080/event" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .

```
##### **This retrieves the number of events available in the database [4 in this case]**

```
curl -s --request GET --url "http://localhost:8080/event" --header "Authorization: Bearer: $BEARER_TOKEN" | jq 'length'

```

##### **Query on Variant Fields Only**

*This command queries events where the event_specificdetails include an "action" of "update"*

```
curl -s --request GET --url "http://localhost:8080/event?event_specificdetails.action=update" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .

```

 - This will return [] because there is no such event logged in that has
   updated their account

*This command queries events where the event_specificdetails include a "billing_date" of "2023-08-21"*

```
 curl -s --request GET --url "http://localhost:8080/event?event_specificdetails.billing_date=2023-08-21" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .
```
 - This will return the following:
   
        [
         {
           "_id": "emma_1692986668.409667",
           "description": "A customer was billed a certain amount",
           "entitytype": "customer",
           "event_specificdetails": {
             "amount": 75.5,
             "billing_date": "2023-08-21",
             "currency": "AED"
           },
           "event_type": "billing",
           "ip": "192.168.0.6",
           "location": "Dubai",
           "timestamp": 1692986668.409667,
           "user_id": "emma",
           "username": "david_smith"
         }
       ]

 
##### **Query on Invariant Fields Only** 
  
*This command queries  events with a "location" of "Chicago"*

```
curl -s --request GET --url "http://localhost:8080/event?location=Chicago" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .
```

*This command queries  events with an "ip" of "192.168.0.1"*

```
curl -s --request GET --url "http://localhost:8080/event?ip=192.168.0.1" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .
```

##### **Query on Both Variant and Invariant Fields:** 

*This command queries   events with an "event_type" of "account_created" and a "location" of "Dubai"*

```
curl -s --request GET --url "http://localhost:8080/event?event_type=AccountCreated&location=Dubai" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .
```

 - This will return [] because there is an event_type of account_created
   but it was not created in Dubai

*This command queries  events with an "event_type" of "billing" and an "currency" of 'AED'*

```
curl -s --request GET --url "http://localhost:8080/event?event_type=billing&event_specificdetails.currency=AED" --header "Authorization: Bearer: $BEARER_TOKEN" | jq .
```

## Dependencies

This is done through the requirements.txt which is deployed using Dockerfile which runs with docker-compose

-   Flask==2.3.2
-   PyJWT==2.7.0
-   Gunicorn==21.2.0
-   python-dotenv==0.19.0
-   jsonschema==4.17.3
-   pymongo==4.3.3

## Rationale and Trade-offs


**Flask**:

-   Rationale: Chosen for its simplicity and ease of use.
-   Trade-offs: Limited built-in features compared to larger frameworks, but this aligns with the project's goal to avoid extensive frameworks.

**MongoDB**:

-   Rationale: Suitable for an open-ended list of events due to its schema-less nature, offering flexibility.
-   Trade-offs: Complex querying can be challenging, but this aligns with the project's requirement for basic querying.

**JWT (JSON Web Tokens)**:

-   Rationale: Provides stateless authentication, enhancing security without the need for server-side sessions. Chosen over Oauth2 since we dont need to maintain state.
-   Trade-offs: Token management and revocation may be more complex for some use cases.

**Docker**:

-   Rationale: Ensures consistency across environments and simplifies deployment. Allows containerization.
-   Trade-offs: Slight overhead due to containerization, but this is outweighed by its benefits.

**Gunicorn**:
-   Rationale: Easy to set up and suitable for production environments.
-   Trade-offs: Less suitable for development environments compared to lightweight servers like Waitress, but optimal for production use.

## Future Plans


- Implement more specific error handling by catching and handling different JWT-related exceptions separately in JWT Token Decoding.

- Implement a robust logging strategy that logs important events and errors. Code lacks comprehensive logging and monitoring mechanisms that is cause challenges in diagnosing and trobuleshooting issues in a production environment.

- Set up monitoring tools and alerting systems to proactively detect and respond to issues.
- Lack of support for complex querying therefore a more robost validation mechanism for schemas should be implemented due to the flexibility of mongoDB schemas.
- Implementing MongoDB data sharding strategies to distribute data across multiple databases or shards to manage large datasets efficiently.
- Implement thorough input validation, including data sanitization, to prevent security vulnerabilities such as SQL injection or cross-site scripting (XSS).
- Implement automated testing that covers unit testing, integration testing, and end to end testing.
- Using Ngnix to manage load balancing across multiple instances to distribute incoming requests evenly.
- Set up structured logging, monitoring, and alerting systems to track errors, debug information.
- Implement specific exception handling for different components.
- Implement using message queuing systems for scalability, fault tolerance and asynchronous processing. 
- `docker-compose.yml` is designed for a single instance of the microservice. For high availability and scalability, there's a need for container orchestration solutions like Kubernetes to manage multiple instances of your microservice.
- 







