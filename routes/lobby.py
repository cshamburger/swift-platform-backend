from flask_socketio import emit, join_room, leave_room
from flask import request
from extensions import socketio
import jwt
from config import Config

# track connected players
connected_users = {}

# matchmaking queue
matchmaking_queue = []

MATCH_SIZE = 2



@socketio.on("connect")
def handle_connect():
    print("Client attempting to connect")


@socketio.on("authenticate")
def authenticate(data):
    token = data.get("token")

    if not token:
        emit("auth_error", {"message": "No token provided"})
        return

    try:
        decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["user_id"]

        connected_users[request.sid] = user_id

        emit("auth_success", {"message": "Authenticated", "user_id": user_id})
        print(f"User {user_id} connected")

    except Exception as e:
        emit("auth_error", {"message": "Invalid token"})


@socketio.on("join_lobby")
def join_lobby(data):
    room = data.get("room", "main_lobby")

    join_room(room)

    emit("system_message",
         {"message": f"User joined {room}"},
         to=room)
    
@socketio.on("find_match")
def find_match():
    user_id = connected_users.get(request.sid)

    if not user_id:
        emit("system_message", {"message": "Not authenticated"})
        return

    # prevent duplicate queueing
    if request.sid in matchmaking_queue:
        emit("system_message", {"message": "Already in queue"})
        return

    matchmaking_queue.append(request.sid)

    emit("system_message", {"message": "Searching for match..."})

    # if enough players → create match
    if len(matchmaking_queue) >= MATCH_SIZE:
        players = matchmaking_queue[:MATCH_SIZE]
        del matchmaking_queue[:MATCH_SIZE]

        room_name = f"match_{players[0][:5]}"

        for player_sid in players:
            join_room(room_name, sid=player_sid)
            socketio.emit(
                "match_found",
                {"room": room_name},
                to=player_sid
            )
    

@socketio.on("disconnect")
def handle_disconnect():
    user_id = connected_users.get(request.sid)

    if request.sid in matchmaking_queue:
        matchmaking_queue.remove(request.sid)

    if user_id:
        print(f"User {user_id} disconnected")
        del connected_users[request.sid]
