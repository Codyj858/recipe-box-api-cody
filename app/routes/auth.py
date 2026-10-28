from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app.services.auth_service import register_user, login_user
from app.helpers import require_auth
from app.extensions import limiter

auth_bp = Blueprint("auth", __name__)

@limiter.limit("1 per 10 seconds")
@auth_bp.post("/register")
def register():
        data = request.get_json(silent=True) or {}
        body, status = register_user(data)
        return jsonify(body), status

@limiter.limit("1 per 10 seconds")
@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    body, status = login_user(data)
    return jsonify(body), status