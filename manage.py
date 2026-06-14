from app import create_app
from app.extensions import db
from app.models import User, Admin, Category, Complaint, ComplaintUpdate, OTP

app = create_app()

@app.shell_context_processor
def make_context():
    return dict(app=app, db=db, User=User, Admin=Admin, Category=Category, Complaint=Complaint, ComplaintUpdate=ComplaintUpdate, OTP=OTP)

if __name__ == "__main__":
    app.run()
