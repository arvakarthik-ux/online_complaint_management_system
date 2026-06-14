import secrets
import string

def random_filename(ext: str) -> str:
    token = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
    return f"{token}.{ext.lower()}"
