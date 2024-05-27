#!/usr/bin/python3
""" places_reviews view """

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_review(place_id):
    """ Retrieves the list of all Review objects linked to a place """
    output = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for review in place.reviews:
        output.append(review.to_dict())
    return jsonify(output)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Retrieves a review object by its id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review object by its id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def add_review(place_id):
    """ Adds a new review to a place """
    place = storage.get(Place, place_id)
    if not place:
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
    if "text" not in body:
        abort(400, 'Missing text')
    body['place_id'] = place_id
    review = Review(**body)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a review object by its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    try:
        body = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    setattr(review, "text", body.get("text"))
    review.save()
    return jsonify(review.to_dict()), 200
