from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException

from app.db.mongo import get_database

router = APIRouter()


def _normalize_email(email: str) -> str:
    return str(email or "").strip().lower()


def _notifications_collection():
    return get_database()["user_notifications"]


def _serialize_notification(document: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(document.get("_id")),
        "email": document.get("email"),
        "title": document.get("title"),
        "message": document.get("message"),
        "type": document.get("type", "info"),
        "priority": document.get("priority", "normal"),
        "source": document.get("source", "system"),
        "action_label": document.get("action_label"),
        "action_path": document.get("action_path"),
        "read": bool(document.get("read", False)),
        "created_at": document.get("created_at"),
        "read_at": document.get("read_at"),
    }


def create_user_notification(
    email: str,
    title: str,
    message: str,
    notification_type: str = "info",
    action_label: Optional[str] = None,
    action_path: Optional[str] = None,
    source: str = "system",
    priority: str = "normal",
) -> Optional[str]:
    normalized_email = _normalize_email(email)
    if not normalized_email:
        return None

    document = {
        "email": normalized_email,
        "title": title,
        "message": message,
        "type": notification_type,
        "priority": priority,
        "source": source,
        "action_label": action_label,
        "action_path": action_path,
        "read": False,
        "created_at": datetime.now(timezone.utc),
        "read_at": None,
    }

    inserted = _notifications_collection().insert_one(document)
    return str(inserted.inserted_id)


@router.get("/notifications/{email}")
def get_notifications(email: str, limit: int = 12) -> Dict[str, Any]:
    normalized_email = _normalize_email(email)
    bounded_limit = max(1, min(limit, 50))

    cursor = (
        _notifications_collection()
        .find({"email": normalized_email})
        .sort("created_at", -1)
        .limit(bounded_limit)
    )

    notifications = [_serialize_notification(item) for item in cursor]
    unread_count = _notifications_collection().count_documents({"email": normalized_email, "read": False})

    return {
        "status": "success",
        "email": normalized_email,
        "count": len(notifications),
        "unread_count": unread_count,
        "notifications": notifications,
    }


@router.get("/notifications/{email}/unread-count")
def get_unread_notification_count(email: str) -> Dict[str, Any]:
    normalized_email = _normalize_email(email)
    unread_count = _notifications_collection().count_documents({"email": normalized_email, "read": False})
    return {"status": "success", "email": normalized_email, "unread_count": unread_count}


@router.post("/notifications/{email}/{notification_id}/read")
def mark_notification_read(email: str, notification_id: str) -> Dict[str, Any]:
    from bson import ObjectId

    normalized_email = _normalize_email(email)
    notifications = _notifications_collection()

    try:
        object_id = ObjectId(notification_id)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid notification_id") from exc

    result = notifications.update_one(
        {"_id": object_id, "email": normalized_email},
        {"$set": {"read": True, "read_at": datetime.now(timezone.utc)}},
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")

    return {"status": "success", "message": "Notification marked as read"}


@router.post("/notifications/{email}/read-all")
def mark_all_notifications_read(email: str) -> Dict[str, Any]:
    normalized_email = _normalize_email(email)
    notifications = _notifications_collection()
    result = notifications.update_many(
        {"email": normalized_email, "read": False},
        {"$set": {"read": True, "read_at": datetime.now(timezone.utc)}},
    )

    return {
        "status": "success",
        "message": "All notifications marked as read",
        "updated_count": result.modified_count,
    }