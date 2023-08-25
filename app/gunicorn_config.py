
# This script configures Gunicorn, the web server, to serve your Flask app.

#TODO:  In a more complex production environment, configure additional settings such as worker timeout,
#       worker class, and log settings. The provided configuration is suitable for basic use but may need expansion
#       for more advanced scenarios.


bind = "0.0.0.0:8080"

#TODO: Implement a more dynamic way to add values based on the hardware capabilities of the server
#      and the expected workload
workers = 4
threads = 2