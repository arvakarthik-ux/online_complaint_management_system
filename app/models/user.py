from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from ..extensions import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    complaints = db.relationship("Complaint", backref="user", lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        # Flask-Login uses this
        return f"user-{self.id}"

@login_manager.user_loader
def load_user(user_id):
    # Support both user and admin IDs with prefixes
    if not user_id:
        return None
    try:
        prefix, raw_id = user_id.split("-", 1)
    except ValueError:
        return None

    from .admin import Admin
    if prefix == "user":
        return User.query.get(int(raw_id))
    if prefix == "admin":
        return Admin.query.get(int(raw_id))
    return None
