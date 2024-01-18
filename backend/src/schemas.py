from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    email: str
    balance: int


class ModelSchema(BaseModel):
    id: int
    name: str
    description: str
    cost: int


class PredictionSchema(BaseModel):
    id: int
    model_id: int
    filename: str
    predictions: str | None
