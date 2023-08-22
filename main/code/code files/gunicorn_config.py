# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 10:11:39 2023

@author: Eman's PC
"""

import multiprocessing

# Gunicorn configuration
bind = "0.0.0.0:5000"  # Host and port to bind to
workers =  1 #multiprocessing.cpu_count() * 2 + 1  # Number of worker processes
worker_class = "sync"  # Worker class for handling requests
threads = 2  # Number of threads per worker process

# Application entry point
app_module = "src.app:app"

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log errors to stdout

# Security
preload_app = True  # Preload the application to avoid unnecessary forking
