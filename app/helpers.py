import sqlite3
from flask import g, jsonify, request, current_app
import jwt


def require_auth():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.lower().startswith("bearer "):
        return jsonify({"error": "Missing or invalid token"}), 401

    token = auth_header.split(" ", 1)[1]

    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=["HS256"],
        )
    except jwt.ExpiredSignatureError as e:
        print("JWT EXPIRED:", repr(e))
        return jsonify({"error": "Token has expired. Please log in again."}), 401
    except jwt.InvalidTokenError as e:
        print("JWT ERROR:", repr(e))
        return jsonify({"error": "Invalid token"}), 401

    user_id = payload.get("sub")
    username = payload.get("username")
    role = payload.get("role")
    print("AUTH USER:", user_id, username)

    return user_id, username, role





def recipe_to_dict(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "ingredients": row["ingredients"],
        "instructions": row["instructions"],
        "is_public": bool(row["is_public"]),
    }