from config import socketio
from flask import jsonify, session, request
from flask_socketio import send, emit, join_room, leave_room, close_room, rooms, disconnect

active_users = []

@socketio.on('sendInRoom')
def send_room_message(message):
    # session['receive_count'] = session.get('receive_count', 0) + 1
    print("request.sid!: ")
    print(request.sid)
    emit('room_response',
         {'data': message['data'], 'room': message['room']},
         room=message['room'])


@socketio.on('join')
def join(message):
    join_room(message['room'])
    # session['receive_count'] = session.get('receive_count', 0) + 1
    print("Joined ROOM!")
    print(message['who'])
    active_users.append(message['who'])
    emit('join_room_response',
         {'data': ",".join(rooms())})

@socketio.on('leave')
def leave(message):
    leave_room(message['room'])
    # session['receive_count'] = session.get('receive_count', 0) + 1
    print("LEEEFT ROOM!")
    print(message['who'])
    print(message['room'])
    active_users.remove(message['who'])
    disconnect()
    emit('leave_room_response',
         {'data': ",".join(rooms())})

@socketio.on('my_ping')
def my_ping(message):
    emit('my_pong', {'data': message['start'], 'active_users': active_users})


