from core.database import Base, get_async_session
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    balance: Mapped[int] = mapped_column(Integer, default=100)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    predictions: Mapped[list["Prediction"]] = relationship(
        "Prediction", back_populates="user"
    )


class Prediction(Base):
    __tablename__ = "prediction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("model.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    input_filename: Mapped[str] = mapped_column(String(length=320), nullable=False)
    predictions: Mapped[str] = mapped_column(String(length=320), nullable=True)

    model: Mapped["Model"] = relationship("Model", back_populates="predictions")
    user: Mapped["User"] = relationship("User", back_populates="predictions")


class Model(Base):
    __tablename__ = "model"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    model_path: Mapped[str] = mapped_column(String(length=320), nullable=False)
    description: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    cost: Mapped[int] = mapped_column(Integer, default=100)

    predictions: Mapped[list["Prediction"]] = relationship(
        "Prediction", back_populates="model"
    )


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
