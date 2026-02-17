from flask import Blueprint, request, jsonify
from models import get_db_connection
from routes.middleware import token_required

store_bp = Blueprint("store", __name__)

@store_bp.route("/store/products", methods=["POST"])
def create_product():
    data = request.get_json()

    name = data.get("name")
    description = data.get("description")
    price = data.get("price")

    if not name or price is None:
        return jsonify({"error": "Name and price required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO products (name, description, price)
        VALUES (%s, %s, %s)
        RETURNING id;
        """,
        (name, description, price)
    )

    product_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "message": "Product created",
        "product_id": product_id
    }), 201

@store_bp.route("/store/purchase", methods=["POST"])
@token_required
def purchase_product():
    user_id = request.user_id
    data = request.get_json()
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"error": "product_id required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # check product exists
    cur.execute("SELECT id FROM products WHERE id=%s;", (product_id,))
    product = cur.fetchone()

    if not product:
        return jsonify({"error": "Product not found"}), 404

    # add license
    try:
        cur.execute(
            """
            INSERT INTO user_licenses (user_id, product_id)
            VALUES (%s, %s);
            """,
            (user_id, product_id)
        )
        conn.commit()
    except:
        return jsonify({"error": "Already owned"}), 409

    cur.close()
    conn.close()

    return jsonify({"message": "Purchase successful"})

@store_bp.route("/store/library", methods=["GET"])
@token_required
def get_library():
    user_id = request.user_id

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT products.id, products.name, products.description, products.price
        FROM user_licenses
        JOIN products ON products.id = user_licenses.product_id
        WHERE user_licenses.user_id = %s;
        """,
        (user_id,)
    )

    items = cur.fetchall()

    cur.close()
    conn.close()

    library = []
    for item in items:
        library.append({
            "id": item[0],
            "name": item[1],
            "description": item[2],
            "price": float(item[3])
        })

    return jsonify(library)
