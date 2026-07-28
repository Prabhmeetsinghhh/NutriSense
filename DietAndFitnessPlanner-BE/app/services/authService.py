import hashlib
import secrets
from datetime import datetime, timezone
from typing import Any, Dict


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(db: Any, name: str, email: str, password: str) -> Dict[str, Any]:
    normalized_email = (email or "").strip().lower()
    if not normalized_email or not name.strip() or not password:
        raise ValueError("Name, email and password are required")

    existing = db.users.find_one({"email": normalized_email})
    if existing:
        raise ValueError("User already exists")

    user_doc = {
        "name": name.strip(),
        "email": normalized_email,
        "password_hash": _hash_password(password),
        "created_at": datetime.now(timezone.utc),
    }
    db.users.insert_one(user_doc)
    return user_doc


def authenticate_user(db: Any, email: str, password: str) -> Dict[str, Any] | None:
    normalized_email = (email or "").strip().lower()
    if not normalized_email or not password:
        return None

    user_doc = db.users.find_one({"email": normalized_email})
    if not user_doc:
        return None

    if user_doc.get("password_hash") != _hash_password(password):
        return None

    return user_doc
