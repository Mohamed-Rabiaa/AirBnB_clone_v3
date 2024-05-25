#!/usr/bin/python3
""" State view """

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request

@app_views.route('/states', methods=['GET'])
def get_all_states():
    """ Retrieves the list of all State objects """
    output = []
    for state in storage.all(State).values():
        output.append(state.to_dict())
    return jsonify(output)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """ Retrieves a State object by its id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object by its id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'])
def add_state():
    """ Adds a new state """
    body = request.get_json()
    if not body:
        abort(404, description='Not a JSON')
    if not body.get('name'):
        abort(404, description='Missing name')

    state = State(name=body.get('name'))
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates a state by its id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    body = request.get_json()
    if not body:
        abort(404, description='Not a JSON')
    setattr(state, 'name', body.get('name'))
    state.save()
    return jsonify(state.to_dict()), 200
