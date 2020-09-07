from flask import jsonify
from . import api
from models import User, user_role, Role
from Exceptions import NotFound



@api.route("/users/", methods=["GET"])
def users_collection():
    users = User.query.all()

    return jsonify([user.serialize for user in users])


@api.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.filter_by(public_id=user_id).first()

    if not user:
        raise NotFound("User not found")
    
    return jsonify(user.serialize)