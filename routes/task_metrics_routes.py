from fastapi import APIRouter
from services.task_metrics_service import TaskMetricsService

router = APIRouter()

service = TaskMetricsService()

@router.get("/task/metrics/by-status")
async def get_tasks_by_status():
    data = await service.get_tasks_by_status()

    return {
        'success': True,
        'data': data
    }