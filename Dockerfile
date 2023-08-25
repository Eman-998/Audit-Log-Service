#This Dockerfile specifies how to build a Docker image for your application. 

# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
WORKDIR /app

# Install virtualenv
RUN pip install virtualenv

# Create a virtual environment and activate it
RUN virtualenv venv
ENV PATH="/app/venv/bin:$PATH"

# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/

# Install the required packages
RUN pip install -r requirements.txt

# Copy the application code into the container at /app
COPY ./app /app/

# Define the command to run your application
CMD ["gunicorn", "run:app", "-c", "gunicorn_config.py"]



