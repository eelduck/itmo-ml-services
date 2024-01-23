from auth.auth import auth_backend
from auth.schemas import UserCreate, UserRead
from core.database import create_db_and_tables
from fastapi import FastAPI
from fastapi_users import fastapi_users
from routes import (fastapi_users, models_router, predictions_router,
                    user_router)

app = FastAPI(title="My App")

app.include_router(predictions_router)
app.include_router(models_router)
app.include_router(user_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
