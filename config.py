import os

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY environment variable is required")


class DevelopmentConfig(Config):
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

class TestingConfig(Config):
    TESTING = os.getenv("FLASK_TESTING", "1") == "1"

class ProductionConfig(Config):
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"