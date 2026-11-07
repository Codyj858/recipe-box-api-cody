from flask import Blueprint, jsonify, request, current_app
import jwt
from users_service.models import User, db
from datetime import datetime, timedelta

users_bp = Blueprint("users", __name__)

@users_bp.get("/health")
def health():
    return jsonify({"status": "users ok"})


@users_bp.post("/register")
def register():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "username, email, and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "username taken"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email taken"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "username": user.username}), 201


@users_bp.post("/login")
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "invalid credentials"}), 401

    payload = {
        "sub": user.id,
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    secret = current_app.config["JWT_SECRET_KEY"]
    token = jwt.encode(payload, secret, algorithm="HS256")

    return jsonify({"access_token": token}), 200