from config import app, socketio

# noinspection PyUnresolvedReferences
import chat
# noinspection PyUnresolvedReferences
import manage_users
# noinspection PyUnresolvedReferences
import manage_projects


if __name__ == "__main__":
    socketio.run(app)
