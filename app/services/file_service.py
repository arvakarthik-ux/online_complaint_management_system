import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename


# ==========================================
# CHECK ALLOWED FILES
# ==========================================
def allowed_file(filename):

    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1].lower()

    return ext in current_app.config["ALLOWED_EXTENSIONS"]


# ==========================================
# SAVE FILE
# ==========================================
def save_upload(storage):

    if not storage:
        return None

    if storage.filename == "":
        return None

    if not allowed_file(storage.filename):
        return None

    # Original filename
    original_name = storage.filename

    # Extension
    ext = original_name.rsplit(".", 1)[1].lower()

    # Generate unique filename
    filename = f"{uuid.uuid4().hex}.{ext}"

    filename = secure_filename(filename)

    # Upload folder
    upload_folder = current_app.config["UPLOAD_FOLDER"]

    os.makedirs(upload_folder, exist_ok=True)

    # Full path
    filepath = os.path.join(upload_folder, filename)

    # Save file
    storage.save(filepath)

    # Return complete file info
    return {
        "filename": filename,
        "original_name": original_name,
        "filepath": filepath
    }