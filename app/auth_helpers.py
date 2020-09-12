from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, decode_token
)
from flask import request, jsonify, url_for, abort
from models import User
from app.api import api
from functools import wraps
from models import User, user_role, Role
from Exceptions import (NotFound,
                        UnAuthorized, BadRequest,
                        ExistingResource, Forbiden,
                        InternalServerError)

def admin_required(role_name):
    def is_auth(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            role = Role.query.filter(Role.users.any(public_id=user_id)).first()
            if role.name != role_name:
                raise Forbiden(f"User have insufficient permission")
            else:
                return func(*args, **kwargs)
        return wrapper
    return is_auth