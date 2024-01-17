from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    balance: Optional[int]


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
