from sqlalchemy.exc import IntegrityError
from app.models import User
from app.extensions import db
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

    password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        role="user",
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "username or email already in use"}, 409

    return {"message": f"registered {username}"}, 201


def login_user(data):
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"error": "username and password required"}, 400

    user = User.query.filter_by(username=username).first()

    def auth_failed():
        return {"error": "invalid username or password"}, 401

    if user is None:
        return auth_failed()

    if not check_password_hash(user.password_hash, password):
        return auth_failed()

    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )

    return {"token": token}, 200