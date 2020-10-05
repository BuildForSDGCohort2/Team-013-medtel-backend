from flask import jsonify, request
from . import api
from models import db, User, user_role, Role, Address, user_address
from Exceptions import NotFound
from flask_jwt_extended import (
    jwt_required,
    create_access_token
)
from datetime import timedelta
from app.auth_helpers import role_required
from Exceptions import (NotFound,
                        UnAuthorized, BadRequest,
                        ExistingResource,
                        InternalServerError)



@api.route("/users", methods=["POST"])
def new_user():
    name = request.json.get("name", None)
    email = request.json.get("email", None)
    phone = request.json.get("phone", None)
    password = request.json.get("password", None)
    role_id = request.json.get("role_id", None)

    if not email or not password:
        raise BadRequest("Provide email and password")

    user_exist = User.query.filter_by(email=email).first()

    if user_exist:
        raise ExistingResource(f"""User with email {email}
                                          and number {phone} exist!""")
    else:
        user = User(name=name,
                    email=email, phone_number=phone)
        user.set_password(password)
        print(user.id)

    try:
        User.insert(user)
        user_r = user_role.insert().values(role_id=role_id,
                                           user_id=user.id)
        db.session.execute(user_r)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        raise InternalServerError("Database commit error. Could not process your request!")
    
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(hours=24))

    return jsonify({"success": True,
                    "data": {
                        "user": user.serialize,
                        "access_token": access_token
                    }
                    }), 201

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
    user = User.query.filter_by(id=user_id).first()

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

    user = User.query.filter_by(id=user_id).first()
    address = Address.query.filter(
        Address.users.any(id=user_id)).first()

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
                                                 user_id=user.id)
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
