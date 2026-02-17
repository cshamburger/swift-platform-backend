from flask import Flask
from extensions import socketio
from routes.auth import auth_bp
from routes.users import users_bp
from routes.store import store_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(store_bp)

    @app.route("/")
    def home():
        return {"message": "SwiftID API is running"}

    socketio.init_app(app)
    return app

app = create_app()

# import AFTER socketio exists
import routes.lobby

if __name__ == "__main__":
    socketio.run(app, debug=True)
