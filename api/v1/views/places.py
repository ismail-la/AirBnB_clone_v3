#!/usr/bin/python3
""" script that defines two Flask routes for an API that controls places"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User

# This route handles two types of HTTP requests: POST and GET
@app_views.route('/cities/<city_id>/places', methods=['POST', 'GET'],
                 strict_slashes=False)
def city_places_methods(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'POST':
        information = request.get_json(silent=True)
        if not information:
            abort(400, 'Not a JSON')
        if 'user_id' not in information:
            abort(400, 'Missing user_id')
        user = storage.get(User, information['user_id'])
        if user is None:
            abort(404)
        if 'name' not in information:
            abort(400, 'Missing name')
        information['city_id'] = city_id
        new_place = Place(**information)
        new_place.save()
        return jsonify(new_place.to_dict()), 201
    if request.method == 'GET':
        place_list = []
        for place in city.places:
            place_list.append(place.to_dict())
        return jsonify(place_list)


# This route handles three types of HTTP requests: DELETE, GET and POST
@app_views.route('/places/<place_id>', methods=['DELETE', 'GET', 'PUT'],
                 strict_slashes=False)
def place_object(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'DELETE':
        for review in place.reviews:
            storage.delete(review)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'PUT':
        information = request.get_json(silent=True)
        if not information:
            abort(400, 'Not a JSON')
        for key, value in information.items():
            if key in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200

# This root accepts only one type of HTTP request: POST
@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def place_search():
    """
    Allows the client to search for places using filters: state, city, amenity
    """
    information = request.get_json(silent=True)
    if information is None:
        abort(400, 'Not a JSON')

    places = storage.all(Place)
    place_list = []
    count = 0
    for key in information.keys():
        if len(information[key]) > 0 and key in ['states', 'cities', 'amenities']:
            count = 1
            break
    if len(information) == 0 or count == 0 or not information:
        for place in places.values():
            place_list.append(place.to_dict())
        return jsonify(place_list)

    if 'amenities' in information and len(information['amenities']) > 0:
        for place in places.values():
            for id_a in information['amenities']:
                amenity = storage.get(Amenity, id_a)
                if amenity in place.amenities and place not in place_list:
                    place_list.append(place)
                elif amenity not in place.amenities:
                    if place in place_list:
                        place_list.remove(place)
                    break
    else:
        for place in places.values():
            place_list.append(place)

    if 'cities' in information and len(information['cities']) > 0:
        place_tmp = []
        for id_c in information['cities']:
            for place in place_list:
                if place.city_id == id_c:
                    place_tmp.append(place)
        if 'states' in information and len(information['states']) > 0:
            for id_s in information['states']:
                state = storage.get(State, id_s)
                for city in state.cities:
                    if city.id in information['cities']:
                        count = 2
                        break
                if count == 2:
                    continue
                for place in place_list:
                    city_id = place.city_id
                    city = storage.get(City, city_id)
                    if city.state_id == id_s and place not in place_tmp:
                        place_tmp.append(place)
        place_list = place_tmp
    elif 'states' in information and len(information['states']) > 0:
        place_tmp = []
        for id_s in information['states']:
            for place in place_list:
                city_id = place.city_id
                city = storage.get(City, city_id)
                if city.state_id == id_s:
                    place_tmp.append(place)
        place_list = place_tmp

    place_tmp = []
    for place in place_list:
        result = place.to_dict()
        if 'amenities' in result:
            del result['amenities']
        place_tmp.append(result)
    return jsonify(place_tmp)