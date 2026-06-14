from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    current_app
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
    Admin,
    User,
    ComplaintUpdate
)

from ..forms.admin import AdminCreateForm

from ..utils.decorators import admin_required

from ..services.email_service import send_email
from ..services.stats_service import complaint_stats


admin_bp = Blueprint(
    "admin",
    __name__,
    template_folder="../templates/admin"
)


# ==========================================
# ENSURE ADMIN ACCESS
# ==========================================
@admin_bp.before_request
def _ensure_admin():

    if not current_user.is_authenticated:
        return

    if (
        current_user.get_id().startswith("user-")
        and request.endpoint
        and request.endpoint.startswith("admin.")
    ):

        return redirect(
            url_for("user.dashboard")
        )


# ==========================================
# ADMIN DASHBOARD
# ==========================================
@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():

    base_q = Complaint.query

    if (
        not current_user.is_superadmin
        and current_user.category_id
    ):

        base_q = base_q.filter(
            Complaint.category_id == current_user.category_id
        )

    total = base_q.count()

    resolved = base_q.filter_by(
        status="Resolved"
    ).count()

    pending = base_q.filter(
        Complaint.status != "Resolved"
    ).count()

    recent = base_q.order_by(
        Complaint.submitted_at.desc()
    ).limit(10).all()

    charts = complaint_stats(base_q)

    return render_template(
        "admin/dashboard.html",
        total=total,
        pending=pending,
        resolved=resolved,
        recent=recent,
        charts=charts
    )


# ==========================================
# VIEW COMPLAINTS
# ==========================================
@admin_bp.route("/complaints")
@login_required
@admin_required
def complaints():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    status = request.args.get("status")

    qtext = request.args.get("q")

    category_id = request.args.get(
        "category_id",
        type=int
    )

    base_q = Complaint.query

    if (
        not current_user.is_superadmin
        and current_user.category_id
    ):

        base_q = base_q.filter(
            Complaint.category_id == current_user.category_id
        )

    if status:

        base_q = base_q.filter(
            Complaint.status == status
        )

    if qtext:

        like = f"%{qtext.strip()}%"

        base_q = base_q.filter(
            (
                Complaint.public_id.ilike(like)
            )
            |
            (
                Complaint.title.ilike(like)
            )
        )

    if category_id:

        base_q = base_q.filter(
            Complaint.category_id == category_id
        )

    base_q = base_q.order_by(
        Complaint.submitted_at.desc()
    )

    pagination = base_q.paginate(
        page=page,
        per_page=15,
        error_out=False
    )

    categories = Category.query.order_by(
        Category.name.asc()
    ).all()

    return render_template(
        "admin/complaints.html",
        pagination=pagination,
        complaints=pagination.items,
        categories=categories
    )


# ==========================================
# COMPLAINT DETAIL + UPDATE
# ==========================================
@admin_bp.route("/complaint/<public_id>", methods=["GET", "POST"])
@login_required
@admin_required
def complaint_detail(public_id):

    complaint = Complaint.query.filter_by(
        public_id=public_id
    ).first_or_404()

    if (
        not current_user.is_superadmin
        and current_user.category_id != complaint.category_id
    ):

        flash(
            "Not authorized for this complaint.",
            "danger"
        )

        return redirect(
            url_for("admin.complaints")
        )

    if request.method == "POST":

        new_status = request.form.get("status")

        remarks = request.form.get(
            "remarks",
            ""
        )

        if new_status and new_status != complaint.status:

            complaint.status = new_status

        update = ComplaintUpdate(

            complaint_id=complaint.id,

            status=complaint.status,

            remarks=remarks
        )

        db.session.add(update)

        db.session.commit()

        # ==========================================
        # SEND EMAIL TO USER
        # ==========================================
        send_email(

    subject=f"Complaint {complaint.public_id} Status Updated",

    recipients=[complaint.user.email],

    body=f"""
Hello {complaint.user.full_name},

Your complaint status has been updated.

Complaint ID: {complaint.public_id}

Complaint Title: {complaint.title}

New Status: {complaint.status}

Remarks:
{remarks if remarks else "No remarks"}

Please login to the portal for more details.

Thank you,
Online Complaint Management System
"""
)

        flash(
            "Complaint updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "admin.complaint_detail",
                public_id=public_id
            )
        )

    statuses = [
        "Submitted",
        "Under Review",
        "Investigation Started",
        "Pending Documents",
        "Resolved",
        "Rejected"
    ]

    return render_template(
        "admin/complaint_detail.html",
        complaint=complaint,
        statuses=statuses
    )


# ==========================================
# DELETE COMPLAINT
# ==========================================
@admin_bp.route("/complaint/<public_id>/delete", methods=["POST"])
@login_required
@admin_required
def complaint_delete(public_id):

    complaint = Complaint.query.filter_by(
        public_id=public_id
    ).first_or_404()

    if complaint.status != "Resolved":

        flash(
            "Only resolved complaints can be deleted.",
            "warning"
        )

        return redirect(
            url_for(
                "admin.complaint_detail",
                public_id=public_id
            )
        )

    if (
        not current_user.is_superadmin
        and current_user.category_id != complaint.category_id
    ):

        flash(
            "Not authorized for this complaint.",
            "danger"
        )

        return redirect(
            url_for("admin.complaints")
        )

    db.session.delete(complaint)

    db.session.commit()

    flash(
        "Complaint deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.complaints")
    )


# ==========================================
# MANAGE ADMINS
# ==========================================
@admin_bp.route("/admins", methods=["GET", "POST"])
@login_required
@admin_required(super_only=True)
def admins():

    form = AdminCreateForm()

    categories = Category.query.order_by(
        Category.name.asc()
    ).all()

    form.category_id.choices = [

        (0, "— None (Superadmin or All) —")

    ] + [

        (c.id, c.name)

        for c in categories
    ]

    if form.validate_on_submit():

        existing = Admin.query.filter_by(
            email=form.email.data.lower()
        ).first()

        if existing:

            flash(
                "Admin email already exists.",
                "danger"
            )

        else:

            admin = Admin(

                full_name=form.full_name.data.strip(),

                email=form.email.data.lower(),

                role=form.role.data,

                category_id=(
                    form.category_id.data
                    if form.category_id.data != 0
                    else None
                )
            )

            admin.set_password(
                request.form.get("password")
            )

            db.session.add(admin)

            db.session.commit()

            flash(
                "Admin created successfully.",
                "success"
            )

            return redirect(
                url_for("admin.admins")
            )

    admins = Admin.query.order_by(
        Admin.created_at.desc()
    ).all()

    return render_template(
        "admin/admins.html",
        form=form,
        admins=admins,
        categories=categories
    )


# ==========================================
# USERS LIST
# ==========================================
@admin_bp.route("/users")
@login_required
@admin_required
def users():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    qtext = request.args.get("q")

    q = User.query

    if qtext:

        like = f"%{qtext.strip()}%"

        q = q.filter(
            (
                User.email.ilike(like)
            )
            |
            (
                User.full_name.ilike(like)
            )
        )

    q = q.order_by(
        User.created_at.desc()
    )

    pagination = q.paginate(
        page=page,
        per_page=20,
        error_out=False
    )

    return render_template(
        "admin/users.html",
        pagination=pagination,
        users=pagination.items
    )


# ==========================================
# MANAGE CATEGORIES
# ==========================================
@admin_bp.route("/categories", methods=["GET", "POST"])
@login_required
@admin_required(super_only=True)
def categories():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        if not name:

            flash(
                "Category name required.",
                "warning"
            )

        elif Category.query.filter(
            func.lower(Category.name) == name.lower()
        ).first():

            flash(
                "Category already exists.",
                "danger"
            )

        else:

            db.session.add(
                Category(name=name)
            )

            db.session.commit()

            flash(
                "Category added successfully.",
                "success"
            )

        return redirect(
            url_for("admin.categories")
        )

    cats = Category.query.order_by(
        Category.name.asc()
    ).all()

    return render_template(
        "admin/categories.html",
        categories=cats
    )