from datetime import datetime, timedelta
from ..extensions import db
from flask import current_app

class OTP(db.Model):
    __tablename__ = "otps"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, nullable=False)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)

    @staticmethod
    def create(email: str, code: str):
        exp = datetime.utcnow() + timedelta(minutes=current_app.config.get("OTP_EXP_MINUTES", 5))
        return OTP(email=email, code=code, expires_at=exp)

    def is_valid(self):
        return (not self.used) and (datetime.utcnow() <= self.expires_at)
