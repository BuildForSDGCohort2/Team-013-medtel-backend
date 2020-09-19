from flask import jsonify, request
from . import api
from models import db, User, user_role, Role, Address, user_address
from Exceptions import NotFound
from flask_jwt_extended import (
    jwt_required,
)
from app.auth_helpers import role_required
from Exceptions import (NotFound,
                        UnAuthorized, BadRequest,
                        ExistingResource,
                        InternalServerError)


@api.route("/users", methods=["GET"])
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


@api.route("/users/<user_id>", methods=["PATCH"])
def update_user_profile(user_id):
    name = request.json.get("name")
    email = request.json.get("email")
    phone = request.json.get("phone")
    password = request.json.get("password")

    city = request.json.get("city")
    state = request.json.get("state")
    country = request.json.get("country")

    user = User.query.filter_by(public_id=user_id).first()
    address = Address.query.filter(
        Address.users.any(public_id=user_id)).first()

    if not user:
        raise NotFound("User not found")
    # Update user basic information
    user.name = name
    user.email = email
    user.phone = phone

    # Create new address for user if address does not exists
    # Else update user existing address information
    if not address:
        address = Address(city=city, state=state, country=country)
        Address.insert(address)
        user_addr = user_address.insert().values(address_id=address.id,
                                                 user_id=user.public_id)
        db.session.execute(user_addr)
        db.session.commit()

    else:
        address.state = state
        address.city = city
        address.country = country

        Address.update(address)

    User.update(user)
    user_data = [user.serialize]
    return jsonify({
        "success": True,
        "data": user_data

    })
