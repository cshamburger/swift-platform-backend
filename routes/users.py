from flask import Blueprint, jsonify, request
from models import get_db_connection
from routes.middleware import token_required

users_bp = Blueprint("users", __name__)


@users_bp.route("/users/me", methods=["GET"])
@token_required
def get_current_user():
    user_id = request.user_id

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, email, created_at FROM users WHERE id=%s;",
        (user_id,)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "created_at": user[3]
    })

@users_bp.route("/users/online", methods=["GET"])
def get_online_users():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, last_seen FROM users WHERE status='online';"
    )

    users = cur.fetchall()

    cur.close()
    conn.close()

    online_list = []
    for user in users:
        online_list.append({
            "id": user[0],
            "username": user[1],
            "last_seen": user[2]
        })

    return jsonify(online_list)
