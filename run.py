from flask import jsonify
from app import create_app, socket_io
from app.config import Config
from Exceptions import NotFound, MethodNotAllowed, \
    Forbiden, InternalServerError, ExistingResource,\
    BadRequest, AuthError, UnAuthorized


config = Config()

app = create_app(config)

@app.errorhandler(NotFound)
@app.errorhandler(Forbiden)
@app.errorhandler(MethodNotAllowed)
@app.errorhandler(InternalServerError)
@app.errorhandler(ExistingResource)
@app.errorhandler(UnAuthorized)
@app.errorhandler(BadRequest)
def api_error(error):
    payload = dict(error.payload or ())
    payload['code'] = error.status_code
    payload['message'] = error.message
    payload['success'] = error.success
    return jsonify(payload), error.status_code


if __name__ == "__main__":
    socket_io.run(app)
