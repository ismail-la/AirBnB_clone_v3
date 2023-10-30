#!/usr/bin/python3
"""Script that controls API functions for city objects"""

# imports necessary modules and objects
from api.v1.views import app_views
from flask import abort, request, jsonify
from models.state import State
from models.city import City
from models import storage

# This route handles two types of HTTP requests: GET and POST
@app_views.route('/states/<state_id>/cities', methods=['POST', 'GET'],
                 strict_slashes=False)
def get_state_city(state_id):

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'POST':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        if 'name' not in info.keys():
            abort(400, 'Missing name')
        info['state_id'] = state_id
        new_city = City(**info)
        new_city.save()
        return jsonify(new_city.to_dict()), 201
    if request.method == 'GET':
        city_list = []
        for city in state.cities:
            city_list.append(city.to_dict())
        return jsonify(city_list)



@app_views.route('/cities/<city_id>', methods=['DELETE', 'GET', 'PUT'],
                 strict_slashes=False)
def handle_city(city_id):

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'DELETE':
        for place in city.places:
            for review in place.reviews:
                storage.delete(review)
            storage.delete(place)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'PUT':
        info = request.get_json()
        if not info:
            abort(400, 'Not a JSON')
        for key, value in info.items():
            if key in ['id', 'state_id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(city, key, value)
        city.save()
        return (city.to_dict()), 200
