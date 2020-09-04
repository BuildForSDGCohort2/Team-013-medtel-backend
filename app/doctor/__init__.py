from flask import Blueprint
from flask_restplus import Api

doctor = Blueprint('doctor', __name__, url_prefix='/doc')

api = Api(doctor)
