import socketio

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3NzEzNjk0MDN9.h9OVlXuf2zdfmVUJTiMZLUcKmddjwIy7N78aM8sQHMI"

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")
    sio.emit("authenticate", {"token": TOKEN})

@sio.on("auth_success")
def auth_success(data):
    print("Authenticated:", data)
    sio.emit("find_match")

@sio.on("system_message")
def system_message(data):
    print("Server:", data)

@sio.on("match_found")
def match_found(data):
    print("MATCH FOUND! Room:", data["room"])

@sio.event
def disconnect():
    print("Disconnected")

sio.connect("http://127.0.0.1:5000")
sio.wait()
