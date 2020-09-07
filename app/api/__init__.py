from flask import Blueprint
from flask_restplus import Api

api = Blueprint('api', __name__, url_prefix='/api/v1')

from . import users, doctors, roles, auth