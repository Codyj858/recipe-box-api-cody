import httpx
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, request, current_app
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from app.routes.recipes import recipes_bp
from app.helpers import require_auth, recipe_to_dict
from app.routes.auth import auth_bp
from app.extensions import db, migrate, cache, limiter
import asyncio


DATABASE = "recipes.db"

def create_app(config_name):
    app = Flask(__name__)

    if config_name == "development":
        app.config.from_object(DevelopmentConfig) 
    elif config_name == "testing":
        app.config.from_object(TestingConfig)
    elif config_name == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)



    @app.get("/")
    def hello():
        return jsonify({"message": "Recipe Box API", "recipes": "/recipes"})

    @app.get("/me")
    async def me():
        auth_header = request.headers.get("Authorization")
        async with httpx.AsyncClient() as client:
            users_call = client.get("http://localhost:5001/health", headers={"Authorization": auth_header} if auth_header else {}, timeout=0.5, )
            recipes_call = client.get("http://localhost:5002/recipes", timeout=0.5,)
            users_resp, recipes_resp = await asyncio.gather(users_call, recipes_call, return_exceptions=False)

            users_ok = users_resp.status_code == 200
            recipes_ok = recipes_resp.status_code == 200

            return jsonify({
                "completeness": {
                    "users": "ok" if users_ok else "missing",
                    "recipes": "ok" if recipes_ok else "missing",
                },
                    "users": users_resp.json() if users_ok else None,
                    "recipes": recipes_resp.json() if recipes_ok else None,
            }), 200


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
