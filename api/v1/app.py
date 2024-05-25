#!/usr/bin/python3
""" app.py """


from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.errorhandler(404)
def handle_api_error(error):
    """ Returns a JSON-formatted 404 status code response """
    return jsonify({"error": "Not found"}), 404

@app.teardown_appcontext
def close(exception):
    """ close method """
    storage.close()


if __name__ == "__main__":
    if 'HBNB_API_HOST' in os.environ:
        host = os.getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'
    if 'HBNB_API_PORT' in os.environ:
        port = os.getenv('HBNB_API_PORT')
    else:
        port = 5000
    app.run(host, port, threaded=True)
