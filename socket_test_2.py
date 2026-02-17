import socketio

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3NzEzNzA0NjF9.zX48zNFv2J966noW-OlGuk24w7VCpDV4H0iGByXq3nE"

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
