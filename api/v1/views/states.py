#!/usr/bin/python3
"""
script that uses the Flask framework to create an API for handling State
objects
"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models.state import State
from models import storage


# This route handles two types of HTTP requests: POST and GET
@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """ function handles two types of requests:
        Returns entire states
    """
    if request.method == 'GET':
        states_list = []
        for state in storage.all(State).values():
            states_list.append(state.to_dict())
        return jsonify(states_list)

    if request.method == 'POST':
        infos = request.get_json(silent=True)
        if not infos:
            abort(400, description='Not a JSON')
        if 'name' not in infos:
            abort(400, description='Missing name')
        state = State(**infos)
        state.save()
        return jsonify(state.to_dict()), 201


# This route handles three types of HTTP requests: DELETE, GET and POST
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_methods(state_id):
    """function handles three types of requests:
        Returns a state specified by id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        for city in state.cities:
            for place in city.places:
                for review in place.reviews:
                    storage.delete(review)
                storage.delete(place)
            storage.delete(city)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        infos = request.get_json(silent=True)
        if not infos:
            abort(400, 'Not a JSON')
        for key, value in infos.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
