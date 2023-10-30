#!/usr/bin/python3
"""Script that sets up routes for the Flask application
"""
# Imports the app_views object from the api.v1.views module.It’s likely that
#   app_views is a blueprint that contains routes for your application.
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import Cit
from models.place import Placey
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """
    This function mapped to the route /status and will return a JSON response
    with the status ‘OK’ when accessed with a GET request.
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    This function is mapped to the route /stats and will return a JSON response
    with the count of each object type when accessed with a GET request.
    The counts are obtained by calling the count() method on the storage object
    for each class.
    """
    from models import storage
    return jsonify({'amenities': storage.count(Amenity),
                    'cities': storage.count(City),
                    'places': storage.count(Place),
                    'reviews': storage.count(Review),
                    'states': storage.count(State),
                    'users': storage.count(User)})
