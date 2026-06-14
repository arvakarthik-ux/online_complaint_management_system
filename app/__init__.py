
from flask import Flask

from .config import Config

from .extensions import (
    db,
    migrate,
    mail,
    login_manager,
    csrf,
    oauth
)

from .models import (
    user,
    admin,
    category,
    complaint,
    otp,
    complaint_update
)

from .routes.public import public_bp
from .routes.auth import auth_bp
from .routes.user import user_bp
from .routes.admin import admin_bp

from .utils.filters import register_template_filters


def create_app(config_class=Config):

    app = Flask(
        __name__,
        instance_relative_config=False
    )

    app.config.from_object(config_class)

    # ==========================================
    # INITIALIZE EXTENSIONS
    # ==========================================
    db.init_app(app)

    migrate.init_app(app, db)

    mail.init_app(app)

    login_manager.init_app(app)

    csrf.init_app(app)

    oauth.init_app(app)

    # ==========================================
    # GOOGLE OAUTH CONFIG
    # ==========================================
    oauth.register(

        name="google",

        client_id=app.config["GOOGLE_CLIENT_ID"],

        client_secret=app.config["GOOGLE_CLIENT_SECRET"],

        server_metadata_url=(
            "https://accounts.google.com/.well-known/openid-configuration"
        ),

        client_kwargs={
            "scope": "openid email profile"
        }
    )

    # ==========================================
    # LOGIN SETTINGS
    # ==========================================
    login_manager.login_view = "auth.login"

    login_manager.login_message_category = "warning"

    # ==========================================
    # REGISTER BLUEPRINTS
    # ==========================================
    app.register_blueprint(public_bp)

    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    app.register_blueprint(
        user_bp,
        url_prefix="/user"
    )

    app.register_blueprint(
        admin_bp,
        url_prefix="/admin"
    )

    # ==========================================
    # JINJA FILTERS
    # ==========================================
    register_template_filters(app)

    # ==========================================
    # CREATE UPLOAD FOLDER
    # ==========================================
    import os

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    return app
