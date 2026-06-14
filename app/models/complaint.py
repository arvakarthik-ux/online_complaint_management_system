from datetime import datetime
from ..extensions import db

class Complaint(db.Model):
    __tablename__ = "complaints"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(20), unique=True, index=True, nullable=False)  # CMP20260001
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    incident_date = db.Column(db.Date, nullable=False)
    incident_location = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20), nullable=False)  # Low/Medium/High
    additional_notes = db.Column(db.Text)

    # Uploads: store server path or filename (relative) - multiple files supported in separate table or JSON
    attachments = db.Column(db.JSON, default=list)  # list of dicts: {filename, original_name, mimetype, size}

    status = db.Column(db.String(50), default="Submitted", nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    updates = db.relationship("ComplaintUpdate", backref="complaint", lazy=True, cascade="all, delete-orphan")
