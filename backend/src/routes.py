from io import StringIO

import pandas as pd
from auth.auth import auth_backend
from auth.user_manager import get_user_manager
from core.database import get_async_session
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi_users import FastAPIUsers
from joblib import load
from models import User
from redis import Redis
from rq import Queue
from schemas import ModelSchema, PredictionSchema, UserSchema
from services import ModelService, PredictionService, UserService
from sqlalchemy.ext.asyncio import AsyncSession
from worker.worker_task import predict_task

predictions_router = APIRouter(prefix="/predictions")
models_router = APIRouter(prefix="/models")
user_router = APIRouter(prefix="/user")

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


def get_current_user():
    return fastapi_users.current_user()


redis_conn = Redis(host="redis", port=6379)
queue = Queue(connection=redis_conn)


async def init_models(session):
    models = await ModelService.get_all_models(session)
    return {model.id: load(model.model_path) for model in models}


@predictions_router.get("/")
async def get_user_predictions(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
) -> list:
    predictions = await PredictionService.get_predictions_by_user_id(user.id, session)

    if predictions is None:
        return []

    return [
        PredictionSchema(
            id=prediction.id,
            model_id=prediction.model_id,
            filename=prediction.input_filename,
            predictions=prediction.predictions,
            created_at=str(prediction.created_at),
        )
        for prediction in predictions
    ]


@predictions_router.post("/create")
async def create_prediction(
    model_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user()),
    file: UploadFile = File(...),
) -> dict:
    model = await ModelService.get_model_by_id(model_id, session)
    if model is None:
        raise HTTPException(status_code=400, detail="No such model")

    if user.balance < model.cost:
        raise HTTPException(
            status_code=400, detail="Not enough money to make prediction"
        )

    models = await init_models(session)

    data_str = await file.read()
    filename = file.filename
    prediction_df = pd.read_csv(StringIO(data_str.decode("utf-8")), sep=";")
    prediction = await PredictionService.create_prediction(
        user.id, model.id, filename, session
    )
    print(prediction)

    job = queue.enqueue(
        predict_task, args=(prediction_df, models[model.id], prediction.id)
    )
    await UserService.reduce_balance(user.id, model.cost, session)

    return {"job_id": job.get_id()}


@models_router.get("/")
async def get_models(session: AsyncSession = Depends(get_async_session)) -> list:
    models = await ModelService.get_all_models(session)
    if models is None:
        return []
    return [
        ModelSchema(
            id=model.id,
            name=model.name,
            cost=model.cost,
            description=model.description,
        )
        for model in models
    ]


@user_router.get("/")
async def get_current_user_info(
    user: User = Depends(get_current_user()),
) -> UserSchema:
    return UserSchema(id=user.id, email=user.email, balance=user.balance)
