from flask import jsonify, request
import logging
from . import api
from models import (db, User, user_role, Role,
                    Address, user_address, Doctor,
                    Qualification, HospitalAffiliate,
                    Specialization)
from Exceptions import NotFound
from flask_jwt_extended import (
    jwt_required,
)
from app.auth_helpers import role_required
from Exceptions import (NotFound,
                        UnAuthorized, BadRequest,
                        ExistingResource,
                        InternalServerError)

# Set up  logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


@api.route("/doctors/<doctor_id>", methods=["GET"])
@jwt_required
def get_doctor(doctor_id):
    # Retrieve doctor role
    doctor_role = Role.query.filter_by(name="doctor").first()

    # Get user with role doctor and Id {doctor_id}
    doctor = Doctor.query.filter_by(id=doctor_id).first()

    if not doctor:
        raise NotFound("User not found")

    doctor_data = doctor.serialize
    return jsonify({
        "success": True,
        "data": doctor_data
    })


@api.route('/doctors', methods=["POST"])
def register_doctor():
    name = request.json.get("name")
    overview = request.json.get("overview")
    practicing_from = request.json.get("practicing_from")
    password = request.json.get("password")
    email = request.json.get("email")
    profile_image = request.json.get("profile_image")

    if not email or not password:
        raise BadRequest("Provide email and password")

    doctor_exist = User.query.filter_by(email=email).first()

    if doctor_exist:
        raise ExistingResource(f"""User with email {email} exist!""")
    else:
        doctor = Doctor(
            name=name,
            email=email,
            overview=overview,
            practicing_from=practicing_from,
            profile_image=profile_image
        )
    doctor.set_password(password)

    try:
        Doctor.insert(doctor)
    except Exception as e:
        print(e)
        db.session.rollback()
        raise InternalServerError(
            "Database commit error. Could not process your request!")

    access_token = create_access_token(
        identity=doctor.id,
        expires_delta=timedelta(hours=24))

    return jsonify({"success": True,
                    "data": {
                        "user": doctor.serialize,
                        "access_token": access_token
                    }
                    }), 201


@api.route("/doctors/qualifications", methods=["POST"])
def add_qualification():
    doctor_id = request.json.get("doctor_id")
    qualification_name = request.json.get("name")
    institute = request, json.get('institute')
    procurement_year = request.json.get("year")

    qualification = Qualification(doctor_id=doctor_id, name=qualification_name,
                                  institute=institute, procurement_year=procurement_year)
    try:
        Qualification.insert(qualification)
    except Exception as ex:
        logger.error(str(ex))
        raise InternalServerError(str(ex))

    return jsonify({
        "success": True,
        "data": qualification.serialize
    })


@api.route("/doctors/hospitals", methods=["POST"])
def add_affiliate_hospital():
    doctor_id = request.json.get("doctor_id")
    hospital_name = request.json.get("hosp_name")
    city = request.json.get("city")
    country = request.json.get("country")
    start_date = request.json.get('start_date')
    end_date = request.json.get('end_date')

    hospital = HospitalAffiliate(doctor_id=doctor_id, hospital_name=hospital_name,
                                 city=city, country=country, start_date=start_date,
                                 end_date=end_date)
    try:
        HospitalAffiliate.insert(hospital)
    except Exception as ex:
        logger.error(str(ex))
        raise InternalServerError(str(ex))

    return jsonify({
        "success": True,
        "data": hospital.serialize
    })

@api.route("/doctors/specialization", methods=["POST"])
def add_specialization():
    name = request.json.get("name")
    special = Specialization(name=name)

    try:
        Specialization.insert(special)
    except Exception as ex:
        logger.error(str(ex))
        raise InternalServerError(str(ex))

    return jsonify({
        "success": True,
        "data": special.serialize
    })
