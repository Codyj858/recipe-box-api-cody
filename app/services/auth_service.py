import sqlite3
from app.db import get_db
from app.data.auth_data import get_user_by_username, insert_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from flask import current_app
import jwt

def register_user(data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {"error": "username, email and password required"}, 400

    db = get_db()
    try:
        password_hash = generate_password_hash(password, method="pbkdf2:sha256")
        insert_user(db, username, email, password_hash)
    except sqlite3.IntegrityError:
        return {"error": "username or email already in use"}, 409

    return {"message": f"registered {username}"}, 201


def login_user(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "username and password required"}, 400

    db = get_db()
    user = get_user_by_username(db, username)
    print("LOGIN DEBUG user:", user)

    def auth_failed():
        return {"error": "invalid username or password"}, 401

    if user is None:
        return auth_failed()

    if not check_password_hash(user["password_hash"], password):
        return auth_failed()

    payload = {
        "sub": str(user["id"]),
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )

    return {"token": token}, 200