#!/usr/bin/python3
"""Script to starts a web application using flask framework
"""

# storage object is used to interact with some form of data storage
from models import storage
# read environment variables
from os import getenv
# app_views is a blueprint contains routes for your application
from api.v1.views import app_views
# Handle Cross Origin Resource Sharing (CORS),
#   allowing or restricting requests from different domains.
from flask_cors import CORS
# Flask class to create a new Flask web server application
# and the jsonify function to convert Python data structures to JSON responses.
from flask import Flask, jsonify


# The host and port for running the application are fetched from environment
#  variables, with defaults of ‘0.0.0.0’ and ‘5000’ respectively.
host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else '5000'

# creating a Flask app
app = Flask(__name__)

# Create new Flask application and the blueprint (app_views)
#  is registered with it.
app.register_blueprint(app_views)

# CORS is enabled for all origins on all routes
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown_db(exception):
    """This function Called at the end of each request to close the storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handles 404 page_not_found errors"""
    return jsonify({'error': 'Not found'}), 404
    """
    Returns a JSON response with an error message when a 404 error occurs.
    """


# If this script is run directly (not imported as a module),
#  it will start the Flask development server with the specified host and port.
if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
