from sqlalchemy.exc import IntegrityError
from app.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from flask import current_app

def register_user(data):
    return {"error": "register_user now lives in users service"}, 500

def login_user(data):
    return {"error": "login_user now lives in users service"}, 500