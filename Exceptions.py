from flask import jsonify

# Error handler


class AppErrorRequest(Exception):
    """
    Extends python base exception and convert to clean json error message
    Attributes:
    message (str): Error message of exception
    success (bool): True/False to indicate if request was successful
    status_code (int): http status code for error
    payload (dict): dictionary that contains exception data
    """
    status_code = 400

    def __init__(self, message, success=False, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.success = success

        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['success'] = self.success
        rv['message'] = self.message
        return rv


class AuthError(AppErrorRequest):
    status_code = 401


class ExistingResource(AppErrorRequest):
    status_code = 409


class UnAuthorized(AppErrorRequest):
    status_code = 401


class NotFound(AppErrorRequest):
    status_code = 404


class InternalServerError(AppErrorRequest):
    status_code = 500


class MethodNotAllowed(AppErrorRequest):
    status_code = 405


class Forbiden(AppErrorRequest):
    status_code = 403


class BadRequest(AppErrorRequest):
    status_code = 400
