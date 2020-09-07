from flask import Blueprint
from flask_restplus import Api

admin = Blueprint('admin', __name__,  url_prefix='/api/v1')

from . import admin
