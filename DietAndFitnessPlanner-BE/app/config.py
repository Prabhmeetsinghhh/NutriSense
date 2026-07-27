from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

APP_ENV = os.getenv("APP_ENV", "development").strip().lower() or "development"
IS_PRODUCTION = APP_ENV in {"production", "prod"}


def _as_bool(raw_value: str | None, default: bool = False) -> bool:
    if raw_value is None or str(raw_value).strip() == "":
        return default
    return str(raw_value).strip().lower() in {"1", "true", "yes", "on"}


def _as_csv_list(raw_value: str | None) -> list[str]:
    if not raw_value:
        return []
    return [item.strip() for item in raw_value.split(",") if item.strip()]


DEFAULT_DEV_CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017").strip()
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "diet_fitness_planner").strip()
MONGODB_USE_MOCK = _as_bool(os.getenv("MONGODB_USE_MOCK"), default=False)
MONGODB_ALLOW_MOCK_FALLBACK = _as_bool(
    os.getenv("MONGODB_ALLOW_MOCK_FALLBACK"),
    default=not IS_PRODUCTION,
)
ML_MODEL_DIR = os.getenv("ML_MODEL_DIR", str(PROJECT_ROOT / "models")).strip()

_raw_cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "").strip()
if _raw_cors_origins:
    CORS_ALLOWED_ORIGINS = tuple(_as_csv_list(_raw_cors_origins))
else:
    CORS_ALLOWED_ORIGINS = tuple(DEFAULT_DEV_CORS_ORIGINS if not IS_PRODUCTION else [])


def get_allowed_origins() -> list[str]:
    if CORS_ALLOWED_ORIGINS:
        return list(CORS_ALLOWED_ORIGINS)
    if IS_PRODUCTION:
        raise RuntimeError("CORS_ALLOWED_ORIGINS must be set when APP_ENV=production")
    return list(DEFAULT_DEV_CORS_ORIGINS)
