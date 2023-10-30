#!/usr/bin/python3
"""
script that uses the Flask web framework to create an API for managing
the relationship between Place and Amenity objects
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from models import storage, storage_t


# This endpoint returns a list of amenities linked to a specific place
@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenity(place_id):
    """
        Returns an Amenity linked to a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if storage_t == 'db':
        amenity_list = []
        for amenity in place.amenities:
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)
    else:
        return jsonify(place.amenity_ids)


#  This endpoint performs actions on a specific amenity linked to a place
@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def find_amenity(place_id, amenity_id):
    """
        Acts on a specific Amenity linked to a Place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

# If the request method is POST, it checks if the amenity is already linked to
#   the place (either directly in case of a database or via ID in other cases)
    if request.method == 'POST':
        if storage_t == 'db':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            place.amenities.append(amenity)
        else:
            if amenity.id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.append(amenity.id)
        place.save()
        return jsonify(amenity.to_dict()), 201

#  If the request method is DELETE, it checks if the amenity is linked to
#   the place (either directly in case of a database or via ID in other cases)
    if request.method == 'DELETE':
        if storage_t == 'db':
            if amenity not in place.amenities:
                abort(404)
            place.amenities.remove(amenity)
        else:
            if amenity.id not in place.amenity_ids:
                abort(404)
            place.amenity_ids.remove(amenity.id)
        place.save()
        return jsonify({}), 200
