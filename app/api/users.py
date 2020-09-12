from flask import jsonify
from . import api
from models import User, user_role, Role
from Exceptions import NotFound
from flask_jwt_extended import (
    jwt_required,
)
from app.auth_helpers import admin_required



@api.route("/users", methods=["GET"])
@jwt_required
def users_collection():
    users = User.query.all()
    users_data = [user.serialize for user in users]
    return jsonify({
        "success": True,
        "data": users_data
    })


@api.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.filter_by(public_id=user_id).first()

    if not user:
        raise NotFound("User not found")
    
    user_data = user.serialize
    return jsonify({
        "success": True,
        "data": user_data
    })