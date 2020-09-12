from datetime import timedelta

from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity
)
from random import randint

from app import sqlalchemy as db
from Exceptions import (NotFound,
                        UnAuthorized, BadRequest,
                        ExistingResource,
                        InternalServerError)
from . import api
from models import User, user_role, Role


@api.route("/users/auth", methods=['POST'])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not login or not password:
        raise BadRequest("Missing login or password")

    try:
        user = User.query.filter_by(email=email).first()
    except Exception as ex:
        print(e)
        raise InternalServerError(str(ex))

    if not user:
        raise NotFound(f"User with email {email} not found")

    if not user.check_password(password):
        raise UnAuthorized("invalid password", 401)
    else:
        user_id = user.serialize.get("id")
        access_token = create_access_token(identity=user_id,
                                           expires_delta=timedelta(hours=24))

        return jsonify({
            "success": True,
            "data": {
                "access_token": access_token,
                "user_id": user_id
            }

        })


@api.route("/auth/users", methods=["POST"])
def new_user():
    name = request.json.get("name", None)
    email = request.json.get("email", None)
    phone = request.json.get("phone", None)
    password = request.json.get("password", None)
    role_id = request.json.get("role_id", None)
    public_id = randint(100, 100000)

    if not email or not password:
        raise BadRequest("Provide email and password")

    user_exist = User.query.filter_by(email=email).first()

    if user_exist:
        raise ExistingResource(f"""User with email {email} 
                                          and number {phone} exist!""")
    else:
        user = User(name=name,
                    email=email, phone_number=phone,
                    public_id=public_id)
        user.set_password(password)
        print(user.public_id)

    try:
        User.insert(user)
        user_r = user_role.insert().values(role_id=role_id,
                                            user_id=user.public_id)
        db.session.execute(user_r)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        raise InternalServerError({
                                   "error": """Database commit error.
                                                Could not process your request!"""})
    access_token = create_access_token(
                            identity=user.id,
                            expires_delta=timedelta(hours=24))

    return jsonify({"success": True,
                    "data": {
                        "user": user.serialize,
                        "access_token": access_token
                        }
                    }), 201