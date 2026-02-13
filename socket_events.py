from flask_socketio import join_room, emit

def register_socket_events(socketio):

    @socketio.on("join")
    def handle_join(data):
        room = data["room"]
        username = data["username"]

        join_room(room)
        print(f"👤 {username} joined room {room}")

        emit("message", f"{username} joined room {room}", room=room)
