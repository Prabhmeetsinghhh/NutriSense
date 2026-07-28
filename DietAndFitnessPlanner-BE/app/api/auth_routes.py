from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from app.db.mongo import get_database
from app.services.authService import authenticate_user, register_user

router = APIRouter()


@router.post("/auth/signup")
def signup(payload: Dict[str, Any]) -> Dict[str, Any]:
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))

    if not name or not email or not password:
        raise HTTPException(status_code=400, detail="Name, email and password are required")

    db = get_database()
    try:
        user = register_user(db, name, email, password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "status": "success",
        "message": "Account created successfully",
        "user": {"name": user["name"], "email": user["email"]},
    }


@router.post("/auth/login")
def login(payload: Dict[str, Any]) -> Dict[str, Any]:
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    db = get_database()
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    db.users.update_one(
        {"email": email},
        {"$set": {"last_login": datetime.now(timezone.utc)}}
    )

    return {
        "status": "success",
        "message": "Logged in successfully",
        "user": {"name": user["name"], "email": user["email"]},
    }
