from flask import jsonify
from app import create_app
from app.config import Config
from Exceptions import NotFound, MethodNotAllowed, \
    Forbiden, InternalServerError, ExistingResource,\
    BadRequest, AuthError


config = Config()

app = create_app(config)


@app.errorhandler(NotFound)
@app.errorhandler(Forbiden)
@app.errorhandler(MethodNotAllowed)
@app.errorhandler(InternalServerError)
def api_error(error):
    payload = dict(error.payload or ())
    payload['code'] = error.status_code
    payload['message'] = error.message
    payload['success'] = error.success
    return jsonify(payload), error.status_code


if __name__ == "__main__":
    app.run()
