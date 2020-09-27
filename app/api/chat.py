from flask import session
from flask_jwt_extended import jwt_required
from flask_socketio import emit
from app import socket_io
from . import api


@api.route("/chat")
@jwt_required
def message_user():
    return

@socket_io.on("text", namespace="/chat")
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)