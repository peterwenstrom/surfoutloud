from config import socketio
from flask_socketio import send, emit, join_room, leave_room, close_room, rooms, disconnect


active_users = {}


@socketio.on('sendInRoom')
def send_room_message(message):
    emit('room_response',
         {'data': message['data'], 'room': message['room']},
         room=message['room'])


@socketio.on('join')
def join(message):
    user = message['who']
    room = message['room']
    direct_chat_room = message['direct_chat']

    join_room(room)

    if not direct_chat_room:
        users_in_room = active_users.get(room)
        if users_in_room:
            # room is not empty
            if user not in users_in_room:
                # user added to active users in existing room
                active_users.get(room).append(user)
        else:
            # room created in dict and user set to active
            active_users[room] = [user]

        emit('join_room_response',
             {'active_users': active_users[room]},
             room=room)
    else:
        return


@socketio.on('leave')
def leave(message):
    user = message['who']
    room = message['room']
    direct_chat_room = message['direct_chat']

    leave_room(room)

    if not direct_chat_room:
        if active_users.get(room):
            # check if room exists, should definitely exist
            active_users.get(room).remove(user)

        users_in_room = active_users.get(room)
        if not users_in_room:
            # remove room from dict if empty after user has left
            del active_users[room]

        disconnect()
        emit('leave_room_response',
             {'active_users': active_users.get(room)},
             room=room)
    else:
        return


@socketio.on('my_ping')
def my_ping(message):
    emit('my_pong', {'data': message['start']})


@socketio.on('newMember')
def send_room(message):
    emit('member_join_response',
         {'data': message['data'], 'room': message['room']},
         room=message['room'])


