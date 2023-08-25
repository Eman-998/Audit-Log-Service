#!/bin/bash

# Create an empty .env file in the host directory
touch .env

# User inputs 
read -p "Enter a username for AUDITLOG: " USERNAME
read -sp "Enter a password for AUDITLOG: " PASSWORD

# Set the environment variables for the Docker containers
export USERNAME
export PASSWORD

# Save the environment variables to a .env file
echo "MONGODBATLAS_HOST='mongodb+srv://auditlog_user:FIluWQ9rJL86VOO8@cluster0.pzaaftb.mongodb.net/?retryWrites=true&w=majority'" >> .env

echo "USERNAME=$USERNAME" >> .env

echo "PASSWORD=$PASSWORD" >> .env

echo "SECRET_KEY=$(openssl rand -base64 32)" >> .env

# Source (load) the .env file
source .env

. .env
