#!/usr/bin/python3
""" amenities view """

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_amenities():
    """ Retrieves the list of all Amenity objects """
    output = []
    for amenity in storage.all(Amenity).values():
        output.append(amenity.to_dict())
    return jsonify(output)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an amenity object by its id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an amenity object by its id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def add_amenity():
    """ Adds a new amenity """
    try:
        body = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    if "name" not in body:
        abort(400, 'Missing name')
    amenity = Amenity(**body)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an amenity object by its id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        body = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    setattr(amenity, "name", body.get("name"))
    amenity.save()
    return jsonify(amenity.to_dict()), 200
