#!/usr/bin/python3
"""Python script for a RESTful API that manages Amenity objects.
It uses the Flask framework and defines several routes to handle
different HTTP methods
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def amenities():
    """
    this route supports GET and POST methods
    """
    if request.method == 'GET':
        amenity_list = []
        for amenity in storage.all(Amenity).values():
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)
    if request.method == 'POST':
        infos = request.get_json(silent=True)
        if not infos:
            abort(400, 'Not a JSON')
        if 'name' not in infos:
            abort(400, 'Missing name')
        amenity_new = Amenity(**infos)
        amenity_new.save()
        return jsonify(amenity_new.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amanity_Method(amenity_id):
    """
    This route supports GET, DELETE, and PUT methods, all operating
    on a specific amenity identified by amenity_id.
    """

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'PUT':
        infos = request.get_json(silent=True)
        if not infos:
            abort(400, 'Not a JSON')
        for key, value in infos.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
