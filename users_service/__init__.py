from flask import Flask
from config import UsersDevelopmentConfig
from app.extensions import db, migrate, cache, limiter
from users_service.routes import users_bp  # you'll define this
from flask_migrate import Migrate

migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(UsersDevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    limiter.init_app(app)

    from users_service import models

    app.register_blueprint(users_bp)

    return app