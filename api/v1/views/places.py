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

    body = request.get_json()
    if not body:
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
    body = request.get_json()
    if not body:
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
    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    states_ids = body.get("states")
    cities_ids = body.get("cities")
    amenities_ids = body.get("amenities")
    output = []
    if not states_ids and not cities_ids:
        places = storage.all(Place).values()
        output = list(places)

    if states_ids:
        for state_id in states_ids:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    for place in city.places:
                        output.append(place)
    if cities_ids:
        for city_id in cities_ids:
            city = storage.get(City, city_id)
            if city:
                for place in city.places:
                    if place not in output:
                        output.append(place)

    '''
    if amenities_ids:
        for place in output:
            if place.amenities:
                place_amenities_ids = [
                    amenity.id for amenity in place.amenities]
                for amenity_id in amenities_ids:
                    if amenity_id not in place_amenities_ids:
                        output.remove(place)
                        break
    '''
    if amenities_ids:
        filtered_output = []
        for place in output:
            place_amenities_ids = [amenity.id for amenity in place.amenities]
            if all(
                    amenity_id in place_amenities_ids for amenity_id in amenities_ids):
                filtered_output.append(place)
        output = filtered_output

    output = [storage.get(Place, place.id).to_dict() for place in output]
    keys_to_remove = ["amenities", "reviews", "amenity_ids"]
    result = [
        {k: v for k, v in place_dict.items() if k not in keys_to_remove}
        for place_dict in output
    ]
    return jsonify(output)
