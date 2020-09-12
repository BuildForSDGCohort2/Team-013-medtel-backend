from flask import Blueprint

admin = Blueprint('admin', __name__,  url_prefix='/api/v1')

from . import admin
