from flask import jsonify, request

from . import api
from models import User, user_role, Role
from app import sqlalchemy as db
from Exceptions import (NotFound,
                        UnAuthorized, BadRequest,
                        ExistingResource,
                        InternalServerError)


@api.route("/roles", methods=["GET"])
def roles_collection():
    roles = Role.query.all()

    return jsonify([role.serialize for role in roles])


@api.route("/roles/<role_id>", methods=["GET"])
def get_role(role_id):
    user = Role.query.filter_by(id=role_id).first()

    if not role:
        raise NotFound("Role not found")

    return jsonify(user.serialize)


@api.route("/roles", methods=["POST"])
def add_role():
    role_name = request.json.get("name")

    role_exist = Role.query.filter_by(name=role_name).first()

    if role_exist:
        raise ExistingResource(f"Role with name {role_name} exists!")
    role = Role(name=role_name)

    try:
        Role.insert(role)
    except Exception as e:
        print(e)
        db.session.rollback()
        raise InternalServerError("""Unexpected error occured!
                                    Could not create role.""")

    return jsonify(role.serialize)
