from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def admin_required(fn=None, *, super_only=False):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.get_id().startswith("admin-"):
                flash("Admin access required.", "danger")
                return redirect(url_for("auth.admin_login"))
            if super_only and not getattr(current_user, "is_superadmin", False):
                flash("Superadmin access required.", "danger")
                return redirect(url_for("admin.dashboard"))
            return view(*args, **kwargs)
        return wrapped
    return decorator(fn) if fn else decorator
