from models.models import Model, Prediction, User
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ModelService:
    @staticmethod
    async def get_model_by_id(model_id: int, session: AsyncSession) -> Model | None:
        result = await session.get_one(Model, model_id)
        return result

    @staticmethod
    async def get_all_models(session: AsyncSession) -> list[Model] | None:
        result = await session.execute(select(Model))
        return result.scalars().all()


class UserService:
    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> None:
        result = await session.get_one(User, user_id)
        return result

    @staticmethod
    async def reduce_balance(user_id: int, amount: int, session: AsyncSession) -> None:
        await session.execute(
            update(User).where(User.id == user_id).values(balance=User.balance - amount)
        )
        await session.commit()

    @staticmethod
    async def get_all_predictions(session: AsyncSession) -> list[Model] | None:
        query = select(Model)
        result = (await session.scalars(query)).all()
        return result


class PredictionService:
    @staticmethod
    async def get_prediction_by_id(
        prediction_id: int, session: AsyncSession
    ) -> Prediction:
        result = await session.get_one(Prediction, prediction_id)
        return result

    @staticmethod
    async def get_predictions_by_user_id(
        user_id: int, session: AsyncSession
    ) -> list[Prediction] | None:
        result = await session.execute(
            select(Prediction).where(Prediction.user_id == user_id)
        )
        return result.scalars().all()

    @staticmethod
    async def create_prediction(
        user_id: int, model_id: int, input_filename: str, session: AsyncSession
    ) -> Prediction:
        prediction = Prediction(
            user_id=user_id, model_id=model_id, input_filename=input_filename
        )
        session.add(prediction)
        await session.commit()
        return prediction

    @staticmethod
    async def update_prediction(
        prediction_id: int, predictions: list[int], session: AsyncSession
    ) -> None:
        await session.execute(
            update(Prediction)
            .where(Prediction.id == prediction_id)
            .values(predictions=str(predictions))
        )
        await session.commit()
