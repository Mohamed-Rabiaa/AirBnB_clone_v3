#!/usr/bin/python3
""" users view """

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """ Retrieves the list of all User objects """
    output = []
    for user in storage.all(User).values():
        output.append(user.to_dict())
    return jsonify(output)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves a user object by its id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user object by its id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def add_user():
    """ Adds a new user """
    try:
        body = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    if "email" not in body:
        abort(400, 'Missing email')
    if "password" not in body:
        abort(400, 'Missing password')
    user = User(**body)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a user object by its id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    try:
        body = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    setattr(user, "password", body.get("password"))
    user.save()
    return jsonify(user.to_dict()), 200
