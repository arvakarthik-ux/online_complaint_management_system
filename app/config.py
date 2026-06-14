import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    # ==========================================
    # SECRET KEY
    # ==========================================
    SECRET_KEY = os.getenv("SECRET_KEY")


    # ==========================================
    # DATABASE
    # ==========================================
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # ==========================================
    # MAIL SETTINGS
    # ==========================================
    MAIL_SERVER = os.getenv("MAIL_SERVER")

    MAIL_PORT = int(
        os.getenv("MAIL_PORT", 587)
    )

    MAIL_USE_TLS = os.getenv(
        "MAIL_USE_TLS",
        "1"
    ) == "1"

    MAIL_USE_SSL = os.getenv(
        "MAIL_USE_SSL",
        "0"
    ) == "1"

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")

    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER"
    )


    # ==========================================
    # GOOGLE LOGIN
    # ==========================================
    GOOGLE_CLIENT_ID = os.getenv(
        "GOOGLE_CLIENT_ID"
    )

    GOOGLE_CLIENT_SECRET = os.getenv(
        "GOOGLE_CLIENT_SECRET"
    )


    # ==========================================
    # SESSION SETTINGS
    # ==========================================
    SESSION_COOKIE_SECURE = os.getenv(
        "SESSION_COOKIE_SECURE",
        "False"
    ) == "True"


    # ==========================================
    # FILE UPLOADS
    # ==========================================
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        "uploads"
    )

    MAX_CONTENT_LENGTH = int(
        os.getenv(
            "MAX_CONTENT_LENGTH",
            10485760
        )
    )

    ALLOWED_EXTENSIONS = set(
        os.getenv(
            "ALLOWED_EXTENSIONS",
            "png,jpg,jpeg,pdf,doc,docx"
        ).split(",")
    )