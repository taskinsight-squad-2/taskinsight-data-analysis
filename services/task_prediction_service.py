# services/task_prediction_service.py

from datetime import datetime
from datetime import timedelta
import copy

from bson import ObjectId

from ml.throughput_forecast import (
    ThroughputForecast
)

from pipelines.task_previsao_throughput_pipeline import (
    pipeline as throughput_prediction_pipeline
)

from repositories.task_metrics_repository import (
    TaskMetricsRepository
)


class PredictionService:

    def __init__(self):
        self.repository = TaskMetricsRepository()

    async def predict_throughput(
        self,
        user_id: str,
        role: str
    ):

        # Cria cópia do pipeline
        dynamic_pipeline = copy.deepcopy(
            throughput_prediction_pipeline
        )

        # Se for usuário comum,
        # filtra somente suas tarefas
        if role == "user":

            dynamic_pipeline[0]["$match"][
                "userId"
            ] = ObjectId(user_id)

        

        # Consulta MongoDB
        data = await self.repository.aggregate(
            dynamic_pipeline
        )

        

        # Necessário um histórico mínimo
        if not data or len(data) < 7:

            return {
                "forecast": [],
                "metadata": {
                    "average": 0,
                    "daysAnalysed": 0
                }
            }

        # Média histórica
        historical_average = round(
            sum(
                item["completed"]
                for item in data
            ) / len(data),
            2
        )

        # Executa previsão
        predictions = (
            ThroughputForecast
            .forecast(data)
        )

        # Última data do histórico
        last_date = datetime.strptime(
            data[-1]["_id"],
            "%Y-%m-%d"
        )

        forecast = []

        for i, prediction in enumerate(
            predictions
        ):

            # Garante que prediction seja tratado como float caso ainda venha em estrutura aninhada
            val = prediction[0] if isinstance(prediction, list) else prediction

            future_date = (
                last_date +
                timedelta(days=i + 1)
            )

            forecast.append({

                "day": future_date.strftime(
                    "%Y-%m-%d"
                ),

                "count": max(
                    0,
                    int(
                        round(val)
                    )
                )

            })

        return {

            "forecast": forecast,

            "metadata": {

                "average": historical_average,

                "daysAnalysed": len(data)

            }

        }