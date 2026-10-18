"""Recipe Box API — BE104 course skeleton.

A working Flask + SQLite CRUD API for recipes. It stores data perfectly —
and it trusts everyone. There is no authentication and no authorization yet.
That is the point: you will add both, lesson by lesson, in Units 2 and 3.
"""

import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, g, jsonify, request, current_app

import jwt

from datetime import datetime, timedelta, timezone

from werkzeug.security import check_password_hash
import os

from config import DevelopmentConfig, TestingConfig, ProductionConfig
from app.routes.recipes import recipes_bp
from app.helpers import require_auth, recipe_to_dict
from app.db import init_db
from app.routes.auth import auth_bp

DATABASE = "recipes.db"

def create_app(config_name):
    app = Flask(__name__)

    if config_name == "testing":
        app.config["DATABASE"] = "test_recipes.db"
    else:
        app.config["DATABASE"] = "recipes.db"
        
    init_db(app)

    if config_name == "development":

        app.config.from_object(DevelopmentConfig) 
    elif config_name == "testing":
        app.config.from_object(TestingConfig)
    elif config_name == "production":

        app.config.from_object(ProductionConfig)
    else:

        app.config.from_object(DevelopmentConfig)


    @app.teardown_appcontext
    def close_db(exception):
        db = getattr(g, "_database", None)
        if db is not None:
            db.close()

    @app.get("/")
    def hello():
        return jsonify({"message": "Recipe Box API", "recipes": "/recipes"})

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp, url_prefix="/recipes")


    return app




def current_user_id():
    token = request.headers.get("Authorization", "")
    if token.startswith("user-"):
        return int(token[len("user-"):])
    return None

if __name__ == "__main__":
    dev_app = create_app("development")
    print("DEV:", dev_app.config["ENV_NAME"])

    prod_app = create_app("production")
    print("PROD:", prod_app.config["ENV_NAME"])