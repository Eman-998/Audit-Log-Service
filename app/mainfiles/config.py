# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:58:30 2023

@author: Eman's PC
"""

# Libraries
import os

def settings(app):  
    app.config.from_object(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['USER'] = os.environ.get('USER')
    app.config['PASS'] = os.environ.get('PASS')
    app.config['MONGODBATLAS_HOST'] = os.environ.get('MONGODBATLAS_HOST')
