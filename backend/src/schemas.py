from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_session


class UserScheme(BaseModel):
    id: int
    email: str
    balance: int


class ModelScheme(BaseModel):
    id: int
    name: str
    description: str
    cost: int


class ModelListScheme(BaseModel):
    models: list[ModelScheme]


Session = Annotated[AsyncSession, Depends(get_async_session)]
