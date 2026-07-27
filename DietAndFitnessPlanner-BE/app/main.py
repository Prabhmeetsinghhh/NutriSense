from fastapi import FastAPI
from app.api.apiRouter import router
from fastapi.middleware.cors import CORSMiddleware
from app.config import APP_ENV, get_allowed_origins
from app.db.mongo import close_mongo_connection, connect_to_mongo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    print(f"Starting NutriSense backend in {APP_ENV} mode")
    connect_to_mongo()


@app.on_event("shutdown")
def on_shutdown() -> None:
    close_mongo_connection()


app.include_router(router)
