# gunicorn_config.py

# This script configures Gunicorn, the web server, to serve your Flask app.

# Set the bind parameter to specify the host and port for Gunicorn.
bind = "0.0.0.0:8080"

# Configure the number of workers and threads as needed.
workers = 4
threads = 2