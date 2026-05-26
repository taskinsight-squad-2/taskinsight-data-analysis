from fastapi import APIRouter
from services.task_metrics_service import TaskMetricsService
from schemas.task_metrics_schemas import TaskMetricsByStatusResponse
from pydantic import BaseModel, Field
router = APIRouter()

service = TaskMetricsService()

class StandardResponse(BaseModel):
    success: bool
    data: TaskMetricsByStatusResponse

@router.get("/task/metrics/by-status", 
            response_model=StandardResponse,
            summary="Obter métricas de tarefas por status",
            description="Retorna a quantidade e percentual de tarefas agrupadas por status.")
async def get_tasks_by_status():
    data = await service.get_tasks_by_status()

    return StandardResponse(
        success=True,
        data=TaskMetricsByStatusResponse(**data['by_status'])
    )