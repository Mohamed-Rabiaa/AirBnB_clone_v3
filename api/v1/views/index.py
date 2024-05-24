#!/usr/bin/python3
""" index.py """


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """ Returns a JSON: "status": "OK" """
    return jsonify({"status": "OK"})
