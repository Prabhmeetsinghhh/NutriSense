from fastapi import APIRouter

from app.api.exercise_routes import router as exercise_router
from app.api.ml_routes import router as ml_router
from app.api.notification_routes import router as notification_router
from app.api.plan_routes import router as plan_router

router = APIRouter()
router.include_router(plan_router)
router.include_router(exercise_router)
router.include_router(ml_router)
router.include_router(notification_router)
