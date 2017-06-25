from config import socketio
from flask_socketio import emit, join_room, leave_room, disconnect


active_users = {}


@socketio.on('join_room')
def join(message):
    user = message['user']
    room = message['room']
    private_room = message['private_room']

    join_room(room)

    if not private_room:
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


@socketio.on('leave_room')
def leave(message):
    user = message['user']
    room = message['room']

    leave_room(room)

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


@socketio.on('message_room')
def message_room(message):
    emit('message_room_response',
         {'data': message['data'], 'room': message['room']},
         room=message['room'])


#############################


@socketio.on('my_ping')
def my_ping(message):
    emit('my_pong', {'data': message['start']})