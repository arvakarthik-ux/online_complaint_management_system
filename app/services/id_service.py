from datetime import datetime
from ..models import Complaint
from ..extensions import db

def generate_complaint_public_id() -> str:
    # Format: CMPYYYYNNNN where NNNN is zero-padded sequence for that year
    year = datetime.utcnow().year
    prefix = f"CMP{year}"
    # Count existing for that year
    like = f"{prefix}%"
    last = db.session.query(Complaint.public_id).filter(Complaint.public_id.like(like)).order_by(Complaint.public_id.desc()).first()
    if not last:
        seq = 1
    else:
        try:
            seq = int(last[0][-4:]) + 1
        except Exception:
            seq = 1
    return f"{prefix}{seq:04d}"
