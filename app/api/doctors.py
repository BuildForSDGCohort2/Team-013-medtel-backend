import logging
from datetime import timedelta
from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
)
from app.auth_helpers import role_required
from . import api
from models import (db, User, user_role, Role,
                    Address, user_address, Doctor,
                    Qualification, HospitalAffiliate,doctor_special,
                    Specialization)
from Exceptions import (NotFound,
                        UnAuthorized, BadRequest,
                        ExistingResource,
                        InternalServerError)

# Set up  logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

@api.route("/doctors/<doctor_id>", methods=["GET"])
def get_doctor(doctor_id):
    # Get user with role doctor and Id {doctor_id}
    doctor = Doctor.query.filter_by(id=doctor_id).first()

    if not doctor:
        raise NotFound("User not found")

    return jsonify({
        "success": True,
        "data": doctor.serialize
    })

@api.route("/doctors", methods=["GET"])
def get_all_doctor():
    doctors = Doctor.query.all()

    doctors_data = [doctor.serialize for doctor in doctors]

    return jsonify({
        "success": True,
        "data": doctors_data
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

    doctor_exist = Doctor.query.filter_by(email=email).first()

    if doctor_exist:
        raise ExistingResource(f"""User with email {email} exist!""")

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
        access_token = create_access_token(
        identity=doctor.id,
        expires_delta=timedelta(hours=24))
    except Exception as e:
        print(e)
        db.session.rollback()
        raise InternalServerError(
            "Database commit error. Could not process your request!")

    return jsonify({"success": True,
                    "data": {
                        "user": doctor.serialize,
                        "access_token": access_token
                    }
                    }), 201


@api.route("/doctors/<doctor_id>/specialities/<special_id>")
def assign_speciality(doctor_id, special_id):
    """
    Args:
        doctor_id (Int):
        special_id (Int):
    """
    try:
        doctor_spec = doctor_special.insert().values(doctor_id=doctor_id,
                                           special_id=special_id)
        db.session.execute(doctor_spec)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        raise InternalServerError("Database commit error. Could not process your request!")

    speciality = Specialization.query.filter_by(id=special_id).first()
    doctor = Doctor.query.filter_by(id=doctor_id).first()
    return jsonify({
        "success": True,
        "message": f"Speciality  Assigned to doctor"
    })


@api.route("/doctors/qualifications", methods=["POST"])
def add_qualification():
    doctor_id = request.json.get("doctor_id")
    qualification_name = request.json.get("name")
    institute = request.json.get('institute')
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

@api.route("/specialization", methods=["POST"])
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
