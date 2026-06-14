from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Complaint
from ..extensions import db

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def home():
    return redirect(url_for("auth.login"))

@public_bp.route("/track", methods=["GET", "POST"])
def track():
    if request.method == "POST":
        cmp_id = request.form.get("complaint_id", "").strip()
        if not cmp_id:
            flash("Please enter a complaint ID.", "warning")
            return render_template("public/track.html")
        complaint = Complaint.query.filter_by(public_id=cmp_id).first()
        if not complaint:
            flash("Complaint not found. Please check the ID.", "danger")
            return render_template("public/track.html")
        return render_template("public/tracking_result.html", complaint=complaint)
    return render_template("public/track.html")
