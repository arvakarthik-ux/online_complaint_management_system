
import random
import random
from werkzeug.security import generate_password_hash

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session
)

from flask_login import (
    login_user,
    current_user,
    logout_user
)

from app.services.email_service import send_email

from ..extensions import db, oauth

from ..models import User, OTP, Admin

from ..forms.auth import (
    RegisterForm,
    VerifyOTPForm,
    LoginForm,
    AdminLoginForm
)

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="../templates/auth"
)


# ==========================================
# GENERATE OTP
# ==========================================
def _generate_otp():
    return f"{random.randint(0, 999999):06d}"


# ==========================================
# USER REGISTER
# ==========================================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated and current_user.get_id().startswith("user-"):
        return redirect(url_for("user.dashboard"))

    form = RegisterForm()

    if form.validate_on_submit():

        existing = User.query.filter_by(
            email=form.email.data.lower()
        ).first()

        if existing:

            flash(
                "Email already registered.",
                "danger"
            )

            return render_template(
                "auth/register.html",
                form=form
            )

        # Create user
        user = User(

            full_name=form.full_name.data.strip(),

            email=form.email.data.lower(),

            mobile=form.mobile.data.strip(),
        )

        user.set_password(form.password.data)

        db.session.add(user)

        db.session.commit()

        # Generate OTP
        code = _generate_otp()

        otp = OTP.create(
            email=user.email,
            code=code
        )

        db.session.add(otp)

        db.session.commit()

        # TEMPORARY TERMINAL OTP
        print("\n" + "=" * 60)
        print(f"OTP for {user.email}: {code}")
        print("=" * 60 + "\n")
        
        # SEND OTP EMAIL
        send_email(

    subject="Email Verification OTP",

    recipients=[user.email],

    body=f"""
Hello {user.full_name},

Your OTP for Complaint Management System verification is:

{code}

This OTP will expire in 5 minutes.

Do not share this OTP with anyone.

Thank you,
Complaint Management System
"""
)
        
        

        flash(
            "Account created successfully. Check terminal for OTP.",
            "success"
        )

        return redirect(
            url_for(
                "auth.verify_otp",
                email=user.email
            )
        )

    return render_template(
        "auth/register.html",
        form=form
    )


# ==========================================
# VERIFY OTP
# ==========================================
@auth_bp.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    email_param = request.args.get("email")

    form = VerifyOTPForm(email=email_param)

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data.lower()
        ).first()

        if not user:

            flash(
                "No user found for this email.",
                "danger"
            )

            return render_template(
                "auth/verify_otp.html",
                form=form
            )

        otp = OTP.query.filter_by(
            email=user.email,
            code=form.code.data
        ).order_by(
            OTP.created_at.desc()
        ).first()

        if not otp or not otp.is_valid():

            flash(
                "Invalid or expired OTP.",
                "danger"
            )

            return render_template(
                "auth/verify_otp.html",
                form=form
            )

        otp.used = True

        user.is_verified = True

        db.session.commit()

        flash(
            "Email verified successfully. You can login now.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/verify_otp.html",
        form=form
    )


# ==========================================
# USER LOGIN
# ==========================================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated and current_user.get_id().startswith("user-"):
        return redirect(url_for("user.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data.lower()
        ).first()

        if not user or not user.check_password(form.password.data):

            flash(
                "Invalid email or password.",
                "danger"
            )

            return render_template(
                "auth/login.html",
                form=form
            )

        if not user.is_verified:

            flash(
                "Please verify your email before login.",
                "warning"
            )

            return redirect(
                url_for(
                    "auth.verify_otp",
                    email=user.email
                )
            )

        login_user(
            user,
            remember=form.remember.data
        )

        flash(
            "Login successful.",
            "success"
        )

        return redirect(
            url_for("user.dashboard")
        )

    return render_template(
        "auth/login.html",
        form=form
    )


# ==========================================
# USER LOGOUT
# ==========================================
@auth_bp.route("/logout")
def logout():

    if current_user.is_authenticated:
        logout_user()

    flash(
        "Logged out successfully.",
        "info"
    )

    return redirect(
        url_for("auth.login")
    )


# ==========================================
# GOOGLE LOGIN
# ==========================================
@auth_bp.route("/google")
def google_login():

    redirect_uri = url_for(
        "auth.google_callback",
        _external=True
    )

    return oauth.google.authorize_redirect(
        redirect_uri
    )


# ==========================================
# GOOGLE CALLBACK
# ==========================================
@auth_bp.route("/google/callback")
def google_callback():

    token = oauth.google.authorize_access_token()

    user_info = token.get("userinfo")

    if user_info is None:
        user_info = oauth.google.parse_id_token(token)

    email = user_info["email"]

    full_name = user_info.get(
        "name",
        "Google User"
    )

    # Check existing user
    user = User.query.filter_by(
        email=email
    ).first()

    # Create new Google user
    if not user:

        user = User(

            full_name=full_name,

            email=email,

            mobile="Google Account",

            is_verified=True
        )

        db.session.add(user)

        db.session.commit()

        # Store session temporarily
        session["google_user_email"] = email

        return redirect(
            url_for("auth.set_google_password")
        )

    login_user(user)

    flash(
        "Logged in with Google successfully.",
        "success"
    )

    return redirect(
        url_for("user.dashboard")
    )


# ==========================================
# SET PASSWORD FOR GOOGLE USER
# ==========================================
@auth_bp.route("/set-google-password", methods=["GET", "POST"])
def set_google_password():

    email = session.get("google_user_email")

    if not email:

        flash(
            "Session expired. Please login again.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    user = User.query.filter_by(
        email=email
    ).first()

    if request.method == "POST":

        password = request.form.get("password")

        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return render_template(
                "auth/set_google_password.html"
            )

        user.set_password(password)

        db.session.commit()

        session.pop(
            "google_user_email",
            None
        )

        login_user(user)

        flash(
            "Password created successfully.",
            "success"
        )

        return redirect(
            url_for("user.dashboard")
        )

    return render_template(
        "auth/set_google_password.html"
    )


# ==========================================
# ADMIN LOGIN
# ==========================================
@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if current_user.is_authenticated and current_user.get_id().startswith("admin-"):
        return redirect(url_for("admin.dashboard"))

    form = AdminLoginForm()

    if form.validate_on_submit():

        admin = Admin.query.filter_by(
            email=form.email.data.lower()
        ).first()

        if not admin or not admin.check_password(form.password.data):

            flash(
                "Invalid admin credentials.",
                "danger"
            )

            return render_template(
                "admin/login.html",
                form=form
            )

        login_user(
            admin,
            remember=form.remember.data
        )

        flash(
            "Admin login successful.",
            "success"
        )

        return redirect(
            url_for("admin.dashboard")
        )

    return render_template(
        "admin/login.html",
        form=form
    )
    
    

# ==========================================
# FORGOT PASSWORD
# ==========================================
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    from ..models.user import User
    from ..services.email_service import send_email

    if request.method == "POST":

        email = request.form.get("email").strip().lower()

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found.", "danger")
            return redirect(url_for("auth.forgot_password"))

        otp = str(random.randint(100000, 999999))

        session["reset_otp"] = otp
        session["reset_email"] = email

        print("\nRESET OTP:", otp)

        send_email(

            subject="Password Reset OTP",

            recipients=[email],

            body=f"""
Hello {user.full_name},

Your password reset OTP is:

{otp}

This OTP will expire soon.
"""
        )

        flash("OTP sent to your email.", "success")

        return redirect(url_for("auth.verify_reset_otp"))

    return render_template("auth/forgot_password.html")


# ==========================================
# VERIFY RESET OTP
# ==========================================
@auth_bp.route("/verify-reset-otp", methods=["GET", "POST"])
def verify_reset_otp():

    if request.method == "POST":

        entered_otp = request.form.get("otp").strip()

        if entered_otp == session.get("reset_otp"):

            flash("OTP verified successfully.", "success")

            return redirect(url_for("auth.reset_password"))

        else:
            flash("Invalid OTP.", "danger")

    return render_template("auth/verify_reset_otp.html")


# ==========================================
# RESET PASSWORD
# ==========================================
@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    from ..models.user import User

    if request.method == "POST":

        new_password = request.form.get("password")

        email = session.get("reset_email")

        user = User.query.filter_by(email=email).first()

        if user:

            user.set_password(new_password)
            user.is_verified = True  # Ensure the user is marked as verified after password reset

            db.session.commit()

            session.pop("reset_otp", None)
            session.pop("reset_email", None)

            flash("Password reset successful.", "success")

            return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html")
