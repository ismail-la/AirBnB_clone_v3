#!/usr/bin/python3
"""
script that uses the Flask framework to create an API for handling User objects
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


# This route handles two types of HTTP requests: POST and GET
@app_views.route('/users', methods=['GET', 'POST'],
                 strict_slashes=False)
def users():
    """function handles two types of requests:
        Retrieves all users
    """
    if request.method == 'GET':
        user_list = []
        for user in storage.all(User).values():
            user_list.append(user.to_dict())
        return jsonify(user_list)
    if request.method == 'POST':
        infos = request.get_json(silent=True)
        if not infos:
            abort(400, 'Not a JSON')
        if 'email' not in infos:
            abort(400, 'Missing email')
        if 'password' not in infos:
            abort(400, 'Missing password')
        new_user = User(**infos)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


# This route handles three types of HTTP requests: DELETE, GET and POST
@app_views.route('/users/<user_id>', methods=['DELETE', 'GET', 'PUT'],
                 strict_slashes=False)
def user_object(user_id):
    """function handles three types of requests:
    Handles a specified User
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == 'DELETE':
        for review in user.reviews:
            storage.delete(review)
        for place in user.places:
            storage.delete(place)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'PUT':
        infos = request.get_json(silent=True)
        if not infos:
            abort(400, 'Not a JSON')
        for key, value in infos.items():
            if key in ['id', 'created_at', 'updated_at', 'email']:
                pass
            else:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
