import os
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_users import FastAPIUsers, fastapi_users
from pydantic import BaseModel, Field

from src.auth.auth import auth_backend
from src.auth.schemas import UserCreate, UserRead
from src.auth.user_manager import get_user_manager
from src.core.database import create_db_and_tables
from src.models.models import User
from src.repositories.model_repository import ModelRepository
from src.schemas import ModelScheme, Session

app = FastAPI(title="My App")
router_fastapi = APIRouter(prefix="/api")

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

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

current_user = fastapi_users.current_user()


@router_fastapi.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@router_fastapi.get("/unprotected-route")
def unprotected_route():
    return "Hello, anonym"


@router_fastapi.post("/models")
async def get_models(session: Session, user: User = Depends(current_user)) -> list:
    models = await ModelRepository.get_all_models(session)
    if models is None:
        return []
    return [
        ModelScheme(
            id=model.id,
            name=model.name,
            cost=model.cost,
            description=model.description,
        )
        for model in models
    ]


from io import StringIO

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from joblib import load

# Load pre-trained models
logreg_model = load(os.path.join("models", "lgbm.joblib"))
lgbm_model = load(os.path.join("models", "logreg.joblib"))

models = {"logreg": logreg_model, "lgbm": lgbm_model}


@router_fastapi.post("/predictions/create")
async def make_prediction(
    session: Session,
    model_name: str,
    user: User = Depends(current_user),
    file: UploadFile = File(...),
) -> dict:
    if model_name not in models:
        return {"error": "Model not found"}

    data_str = await file.read()
    data = StringIO(data_str.decode("utf-8"))
    df_test = pd.read_csv(data, sep=";")
    print(df_test.columns)

    model = models[model_name]
    predictions = model.predict(df_test)

    return {"predictions": predictions.tolist()}


app.include_router(router_fastapi)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
