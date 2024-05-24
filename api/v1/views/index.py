#!/usr/bin/python3
""" index.py """


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

@app_views.route('/status')
def status():
    """ Returns a JSON: "status": "OK" """
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def objs_number():
    """ Retrieves the number of each objects by type """
    dct = {}
    dct['amenities'] = storage.count(Amenity)
    dct['cities'] = storage.count(City)
    dct['places'] = storage.count(Place)
    dct['reviews'] = storage.count(Review)
    dct['states'] = storage.count(State)
    dct['users'] = storage.count(User)
    return jsonify(dct)
