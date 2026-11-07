from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False, server_default="user")
    bio = db.Column(db.String(160), nullable=True)

    def set_password(self, password):
        self.password_hash = password

    def check_password(self, password):
        return check_password_hash == password