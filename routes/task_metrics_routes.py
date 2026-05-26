from fastapi import APIRouter
from services.task_metrics_service import TaskMetricsService
from schemas.task_metrics_schemas import TaskMetricsByStatusResponse
from schemas.task_priority_schemas import TaskMetricsByPriorityResponse
from pydantic import BaseModel, Field
from middlewares.auth import verify_token_user
from fastapi import Depends


router = APIRouter()

service = TaskMetricsService()

class StandardStatusResponse(BaseModel):
    success: bool
    data: TaskMetricsByStatusResponse

class StandardPriorityResponse(BaseModel):
    success: bool
    data: TaskMetricsByPriorityResponse



@router.get("/task/metrics/by-status", 
            response_model=StandardStatusResponse,
            summary="Obter métricas de tarefas por status",
            description="Retorna a quantidade e percentual de tarefas agrupadas por status.")
async def get_tasks_by_status(current_user_id: dict = Depends(verify_token_user)):
    data = await service.get_tasks_by_status(
        # Logica autenticação
        user_id=current_user_id["user_id"], # Substitua pelo ID do usuário autenticado
        role=current_user_id["role"] # Substitua pela função do usuário autenticado
    )


    return StandardStatusResponse(
        success=True,
        data=TaskMetricsByStatusResponse(
            total_tasks=data['total_tasks'],
            **data['by_status']
        )
    )

@router.get("/task/metrics/by-priority",
            response_model=StandardPriorityResponse,
            summary="Obter métricas de tarefas por prioridade",
            description="Retorna a quantidade e percentual de tarefas agrupadas por prioridade.")
async def get_tasks_by_priority(current_user_id: dict = Depends(verify_token_user)):
    data = await service.get_tasks_by_priority(

        # Logica autenticação
        user_id=current_user_id["user_id"], # Substitua pelo ID do usuário autenticado
        role=current_user_id["role"] # Substitua pela função do usuário autenticado
    )


    return StandardPriorityResponse(
        success=True,
        data=TaskMetricsByPriorityResponse(
            total_tasks=data['total_tasks'],
            **data['by_priority']
        )
    )