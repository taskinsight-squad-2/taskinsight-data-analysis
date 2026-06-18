from fastapi import APIRouter, Depends

from services.task_prediction_service import (
    PredictionService
)

from schemas.task_prediction_thoughput_schemas import (
    StandardThroughputResponse
)

from middlewares.auth import (
    verify_token_user
)

router = APIRouter(
    prefix="/task/predictions",
    tags=["task_predictions"]
)

service = PredictionService()


@router.get(
    "/throughput",
    response_model=StandardThroughputResponse,
    summary="Previsão de Throughput",
    description="Prevê quantidade de tarefas concluídas nos próximos 7 dias."
)
async def get_throughput_prediction(
    current_user=Depends(
        verify_token_user
    )
):

    result = await (
        service.predict_throughput(
            user_id=current_user["user_id"],
            role=current_user["role"]
        )
    )

    return StandardThroughputResponse(
        success=True,
        data=result
    )