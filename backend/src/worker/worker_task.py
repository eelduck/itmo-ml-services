import pandas as pd
from core.database import async_session_maker
from services import PredictionService


async def predict_task(data: pd.DataFrame, model, prediction_id: int) -> None:
    predictions = model.predict(data)
    print(predictions)

    async with async_session_maker() as session:
        await PredictionService.update_prediction(
            prediction_id, predictions.tolist(), session
        )
