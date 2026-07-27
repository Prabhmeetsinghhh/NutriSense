import os
from typing import Optional

import certifi
from dotenv import load_dotenv
from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.database import Database

from app.config import (
    APP_ENV,
    IS_PRODUCTION,
    MONGODB_ALLOW_MOCK_FALLBACK,
    MONGODB_DB_NAME,
    MONGODB_URI,
    MONGODB_USE_MOCK,
)

load_dotenv()

# Allow using an in-memory mongomock instance for demos when
# environment variable `MONGODB_USE_MOCK` is set to '1' or 'true'.
_USE_MOCK = MONGODB_USE_MOCK

_mongo_client: Optional[MongoClient] = None
_database: Optional[Database] = None
_database_mode: str = "none"


def _create_mock_database(db_name: str) -> Database:
    global _mongo_client, _database, _database_mode

    try:
        import mongomock

        _mongo_client = mongomock.MongoClient()
        _database = _mongo_client[db_name]
        _database_mode = "mock"
        return _database
    except Exception as exc:
        raise RuntimeError("mongomock is required for in-memory MongoDB but is not installed") from exc


def _ensure_indexes(database: Database) -> None:
    # Ensure core indexes exist for user lookup and plan history retrieval.
    database["users"].create_index("email", unique=True)
    database["plan_history"].create_index([("email", ASCENDING), ("created_at", DESCENDING)])
    database["plan_feedback"].create_index([("email", ASCENDING), ("created_at", DESCENDING)])
    database["plan_feedback"].create_index("plan_id")
    database["user_notifications"].create_index([("email", ASCENDING), ("read", ASCENDING), ("created_at", DESCENDING)])
    database["user_notifications"].create_index([("email", ASCENDING), ("created_at", DESCENDING)])
    database["coach_messages"].create_index([("email", ASCENDING), ("created_at", DESCENDING)])


def connect_to_mongo() -> Database:
    """Create MongoDB connection and verify it with a ping."""
    global _mongo_client, _database, _database_mode

    if _database is not None:
        return _database

    db_name = MONGODB_DB_NAME

    if _USE_MOCK:
        if IS_PRODUCTION:
            raise RuntimeError("MONGODB_USE_MOCK cannot be enabled when APP_ENV=production")
        _database = _create_mock_database(db_name)
    else:
        try:
            _mongo_client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                tlsCAFile=certifi.where(),
            )
            _mongo_client.admin.command("ping")
            _database = _mongo_client[db_name]
            _database_mode = "mongodb"
        except Exception as exc:
            if not IS_PRODUCTION and MONGODB_ALLOW_MOCK_FALLBACK:
                print(f"Warning: MongoDB connection failed ({exc}); falling back to in-memory mock database.")
                _mongo_client = None
                _database = _create_mock_database(db_name)
            else:
                raise RuntimeError(
                    f"MongoDB connection failed: {exc}. "
                    "Set MONGODB_URI to a reachable server and disable mock fallback for production."
                ) from exc

    _ensure_indexes(_database)
    return _database


def close_mongo_connection() -> None:
    """Close MongoDB connection if it is active."""
    global _mongo_client, _database

    if _mongo_client is not None:
        _mongo_client.close()

    _mongo_client = None
    _database = None


def get_database() -> Database:
    """Return active database connection."""
    if _database is None:
        raise RuntimeError("MongoDB is not connected. Call connect_to_mongo first.")
    return _database


def get_database_mode() -> str:
    """Return the active database mode."""
    return _database_mode
