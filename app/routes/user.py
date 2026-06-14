from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app,
    send_from_directory
)

from flask_login import (
    login_required,
    current_user
)

from sqlalchemy import func

from ..extensions import db

from ..models import (
    Complaint,
    Category,
    ComplaintUpdate
)

from ..forms.complaint import ComplaintForm

from ..services.file_service import save_upload
from ..services.id_service import generate_complaint_public_id
from ..services.email_service import send_email


user_bp = Blueprint(
    "user",
    __name__,
    template_folder="../templates/user"
)


# ==========================================
# USER DASHBOARD
# ==========================================
@user_bp.route("/dashboard")
@login_required
def dashboard():

    # Only users allowed
    if not current_user.get_id().startswith("user-"):
        return redirect(url_for("admin.dashboard"))

    # Get categories
    categories = Category.query.order_by(
        Category.name.asc()
    ).all()

    # Total complaints
    total = Complaint.query.filter_by(
        user_id=current_user.id
    ).count()

    # Complaint status summary
    status_counts = dict(
        db.session.query(
            Complaint.status,
            func.count(Complaint.id)
        )
        .filter(
            Complaint.user_id == current_user.id
        )
        .group_by(
            Complaint.status
        )
        .all()
    )

    return render_template(
        "user/dashboard.html",
        categories=categories,
        total=total,
        status_counts=status_counts
    )


# ==========================================
# CREATE NEW COMPLAINT
# ==========================================
@user_bp.route("/complaint/new", methods=["GET", "POST"])
@login_required
def complaint_new():

    # Only users allowed
    if not current_user.get_id().startswith("user-"):
        return redirect(url_for("admin.dashboard"))

    form = ComplaintForm()

    # Load categories
    form.category.choices = [
        (c.id, c.name)
        for c in Category.query.order_by(Category.name.asc()).all()
    ]

    # Submit form
    if form.validate_on_submit():

        attachments = []

        # Save uploaded file
        if form.attachments.data:

            fileinfo = save_upload(
                form.attachments.data
            )

            if fileinfo:
                attachments.append(fileinfo)

        # Create complaint
        complaint = Complaint(

            public_id=generate_complaint_public_id(),

            user_id=current_user.id,

            category_id=form.category.data,

            title=form.title.data.strip(),

            description=form.description.data.strip(),

            incident_date=form.incident_date.data,

            incident_location=form.incident_location.data.strip(),

            priority=form.priority.data,

            additional_notes=(
                form.additional_notes.data.strip()
                if form.additional_notes.data
                else None
            ),

            attachments=attachments,

            status="Submitted"
        )

        db.session.add(complaint)
        db.session.commit()

        # Initial complaint update
        update = ComplaintUpdate(

            complaint_id=complaint.id,

            status="Submitted",

            remarks="Complaint submitted successfully."
        )

        db.session.add(update)
        db.session.commit()

        # ==========================================
        # TERMINAL MESSAGE
        # ==========================================
        print("\n" + "=" * 60)
        print("COMPLAINT SUBMITTED SUCCESSFULLY")
        print(f"Complaint ID: {complaint.public_id}")
        print("=" * 60 + "\n")

        # ==========================================
        # SEND EMAIL TO USER
        # ==========================================
        print("CURRENT USER EMAIL:", current_user.email)
        send_email(

            subject="Complaint Submitted Successfully",

            recipients=[current_user.email],

            body=f"""
Hello {current_user.full_name},

Your complaint has been submitted successfully.

Complaint ID: {complaint.public_id}

Complaint Title: {complaint.title}

Current Status: Submitted

We will notify you whenever your complaint status changes.

Thank you,
Complaint Management System
"""
        )

        flash(
            f"Complaint submitted successfully. Complaint ID: {complaint.public_id}",
            "success"
        )

        return redirect(
            url_for("user.my_complaints")
        )

    return render_template(
        "user/complaint_form.html",
        form=form
    )


# ==========================================
# VIEW USER COMPLAINTS
# ==========================================
@user_bp.route("/complaints")
@login_required
def my_complaints():

    if not current_user.get_id().startswith("user-"):
        return redirect(url_for("admin.dashboard"))

    page = request.args.get(
        "page",
        1,
        type=int
    )

    query = Complaint.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Complaint.submitted_at.desc()
    )

    pagination = query.paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    return render_template(
        "user/my_complaints.html",
        pagination=pagination,
        complaints=pagination.items
    )


# ==========================================
# COMPLAINT DETAIL
# ==========================================
@user_bp.route("/complaint/<public_id>")
@login_required
def complaint_detail(public_id):

    if not current_user.get_id().startswith("user-"):
        return redirect(url_for("admin.dashboard"))

    complaint = Complaint.query.filter_by(
        public_id=public_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "user/complaint_detail.html",
        complaint=complaint
    )


# ==========================================
# FILE DOWNLOAD / VIEW
# ==========================================
@user_bp.route("/uploads/<path:filename>")
@login_required
def uploaded_file(filename):

    import os

    upload_folder = os.path.join(
        current_app.root_path,
        "..",
        current_app.config["UPLOAD_FOLDER"]
    )

    upload_folder = os.path.abspath(upload_folder)

    return send_from_directory(
        upload_folder,
        filename
    )