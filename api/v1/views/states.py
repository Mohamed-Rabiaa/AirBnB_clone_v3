#!/usr/bin/python3
""" states view """

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves the list of all State objects """
    output = []
    for state in storage.all(State).values():
        output.append(state.to_dict())
    return jsonify(output)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object by its id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object by its id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """ Adds a new state """
    try:
        body = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    if "name" not in body:
        abort(400, 'Missing name')

    state = State(**body)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a state by its id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        body = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    setattr(state, "name", body.get("name"))
    state.save()
    return jsonify(state.to_dict()), 200
