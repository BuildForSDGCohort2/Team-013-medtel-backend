from flask import Blueprint
from flask_restplus import Api

admin = Blueprint('admin', __name__, url_prefix='/admin')

api = Api(admin)
