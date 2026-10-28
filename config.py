import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY environment variable is required")
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60


class DevelopmentConfig(Config):
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
    DATABASE = os.path.join(basedir, "recipes.db")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "recipes.db")
    

class TestingConfig(Config):
    TESTING = os.getenv("FLASK_TESTING", "1") == "1"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_recipes.db"


class ProductionConfig(Config):
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
    SQLALCHEMY_DATABASE_URI = "sqlite:///recipes.db"