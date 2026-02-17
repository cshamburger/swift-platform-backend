from flask import Blueprint, request, jsonify
from models import get_db_connection
from routes.middleware import token_required
import bcrypt

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Basic validation
    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    # Hash password
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # check existing email
        cur.execute("SELECT id FROM users WHERE email=%s;", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            return jsonify({"error": "Email already registered"}), 409

        # insert user
        cur.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (username, email, hashed_pw.decode("utf-8"))
        )

        user_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

import jwt
import datetime
from config import Config


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, password_hash FROM users WHERE email=%s;",
            (email,)
        )

        user = cur.fetchone()

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        user_id, stored_hash = user
        # set user online
        cur.execute(
        "UPDATE users SET status='online', last_seen=NOW() WHERE id=%s;",
        (user_id,)
)
        conn.commit()


        # compare password
        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return jsonify({"error": "Invalid credentials"}), 401

        # create JWT token
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }

        token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

        return jsonify({
            "message": "Login successful",
            "token": token
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/auth/logout", methods=["POST"])
@token_required
def logout():
    user_id = request.user_id

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE users SET status='offline', last_seen=NOW() WHERE id=%s;",
            (user_id,)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Logged out successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


