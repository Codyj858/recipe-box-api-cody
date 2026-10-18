from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import sqlite3
from app.db import get_db
from app.services.auth_service import register_user, login_user
from app.helpers import require_auth

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
        data = request.get_json(silent=True) or {}
        body, status = register_user(data)
        return jsonify(body), status

@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    body, status = login_user(data)
    return jsonify(body), status