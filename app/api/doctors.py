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

@api.route("/users/doctors/<doctor_id>", methods=["GET"])
#@jwt_required
#@role_required("doctor")
def get_doctor(doctor_id):
    # Retrieve doctor role
    doctor_role = Role.query.filter_by(name="doctor").first()

    # Get user with role doctor and Id {doctor_id}
    doctor = User.query.filter(User.roles.any(id=doctor_role.id)).filter_by(public_id=doctor_id).first()

    if not doctor:
        raise NotFound("User not found")

    doctor_data = doctor.serialize
    return jsonify({
        "success": True,
        "data": doctor_data
    })
