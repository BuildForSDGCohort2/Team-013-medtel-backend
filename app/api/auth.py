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
from models import User, user_role, Role, Doctor


@api.route("/users/auth", methods=['POST'])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not login or not password:
        raise BadRequest("Missing login or password")

    try:
        user = User.query.filter_by(email=email).first()
    except Exception as ex:
        print(ex)
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


@api.route("/doctors/auth", methods=['POST'])
def doctor_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if not login or not password:
        raise BadRequest("Missing login or password")

    try:
        doctor = Doctor.query.filter_by(email=email).first()
    except Exception as ex:
        print(ex)
        raise InternalServerError(str(ex))

    if not doctor:
        raise NotFound(f"User with email {email} not found")

    if not doctor.check_password(password):
        raise UnAuthorized("invalid password", 401)
    else:
        doctor_id = doctor.serialize.get("id")
        access_token = create_access_token(identity=doctor_id,
                                           expires_delta=timedelta(hours=24))

        return jsonify({
            "success": True,
            "data": {
                "access_token": access_token,
                "user_id": doctor_id
            }

        })
