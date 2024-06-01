#!/usr/bin/python3
""" places view """

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """ Retrieves the list of all Place objects linked to a city """
    output = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for place in city.places:
        output.append(place.to_dict())
    return jsonify(output)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object by its id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place object by its id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def add_place(city_id):
    """ Adds a new place to a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        body = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    if "user_id" not in body:
        abort(400, 'Missing user_id')
    user = storage.get(User, body.get('user_id'))
    if not user:
        abort(404)
    if "name" not in body:
        abort(400, 'Missing name')
    body['city_id'] = city_id
    place = Place(**body)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ Updates a place object by its id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    try:
        body = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    ignored_attrs = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in body.items():
        if key not in ignored_attrs:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_places():
    """ search_places """
    try:
        body = request.get_json()
    except Exception as a:
        abort(400, 'Not a JSON')

    output = []
    empty_lists = False
    if len(body.keys()) == 0:
        for value in body.values():
            if len(value) == 0:
                empty_lists = True
            else:
                empty_lists = False
                break

    if empty_lists:
        output = get_places()
    else:
        if 'states' in body and len(body['states']) > 0:
            for state_id in body['states']:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        output.extend(get_places(city.id))
        if 'cities' in body and len(body['cities']) > 0:
            for city_id in body['cities']:
                output.extend(get_places(city_id))
    return jsonify(output)


def get_places(city_id=None):
    """ get_places """
    output = []
    if (city_id):
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        for place in city.places:
            if place.to_dict() not in output:
                output.append(place.to_dict())
    else:
        places = storage.all(Place)
        for place in places:
            output.append(place.to_dict())
    return output
