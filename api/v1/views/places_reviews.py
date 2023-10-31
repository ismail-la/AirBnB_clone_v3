#!/usr/bin/python3
"""
script that defines two Flask routes for API that controls reviews of a place
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


#  The first route it supports two HTTP methods: POST and GET
@app_views.route('/places/<place_id>/reviews', methods=['POST', 'GET'],
                 strict_slashes=False)
def review_place_methods(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'POST':
        infos = request.get_json(silent=True)
        if not infos:
            abort(400, 'Not a JSON')
        if 'user_id' not in infos:
            abort(400, 'Missing user_id')
        user = storage.get(User, infos['user_id'])
        if user is None:
            abort(404)
        if 'text' not in infos:
            abort(400, 'Missing text')
        infos['place_id'] = place_id
        new_review = Review(**infos)
        new_review.save()
        return jsonify(new_review.to_dict()), 201
    if request.method == 'GET':
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)


#  The first route it supports three HTTP methods: DELETE, GET and PUT
@app_views.route('reviews/<review_id>', methods=['DELETE', 'GET', 'PUT'],
                 strict_slashes=False)
def review_methods(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'PUT':
        infos = request.get_json(silent=True)
        if not infos:
            abort(400, 'Not a JSON')
        for key, value in infos.items():
            if key in ['id', 'created_at', 'updated_at', 'user_id',
                       'place_id']:
                pass
            else:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
