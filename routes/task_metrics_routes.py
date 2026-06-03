from fastapi import APIRouter
from services.task_metrics_service import TaskMetricsService
from schemas.task_metrics_schemas import TaskMetricsByStatusResponse
from schemas.task_priority_schemas import TaskMetricsByPriorityResponse
from schemas.task_average_time_schemas import TaskAverageTimeResponse, StandardAverageTimeResponse
from schemas.task_response_time_schemas import ResponseTimeMetrics, StandardResponseTimeResponse
from schemas.task_resolutions_time_schemas import ResolutionTimeMetrics, StandardResolutionTimeResponse
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


# Rota para obter métricas de tarefas por status
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

# Rota para obter métricas de tarefas por prioridade
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

# Rota para obter o tempo médio para conclusão das tarefas
@router.get("/task/metrics/average-time",
            response_model=StandardAverageTimeResponse,
            summary="Obter tempo médio para conclusão das tarefas",
            description="Retorna o tempo médio estimado para conclusão de uma tarefa com base nas tarefas já concluídas.")
async def get_average_time_to_complete_tasks(current_user_id: dict = Depends(verify_token_user)):
    data = await service.get_average_time_to_complete_tasks(

        # Logica autenticação
        user_id=current_user_id["user_id"], # Substitua pelo ID do usuário autenticado
        role=current_user_id["role"] # Substitua pela função do usuário autenticado
    )

    from schemas.task_average_time_schemas import TaskAverageTimeResponse

    return StandardAverageTimeResponse(
        success=True,
        data=TaskAverageTimeResponse(
            average_time_seconds=data['average_time_seconds'],
            average_time_hours=data['average_time_hours'],
            average_time_days=data['average_time_days']
        )
    )

# Rota para obter a taxa de conclusão de tarefas (throughput)
@router.get("/task/metrics/throughput",
            summary="Obter taxa de conclusão de tarefas",
            description="Retorna a quantidade de tarefas concluídas em um determinado período.")
async def get_tasks_throughput(current_user_id: dict = Depends(verify_token_user)):
    data = await service.get_tasks_throughput(
        user_id=current_user_id["user_id"],
        role=current_user_id["role"]
    )

    return {
        "success": True,
        "data": data
    }

# Rota para obter o backlog de tarefas (criadas vs finalizadas por dia)
@router.get("/task/metrics/backlog",
            summary="Obter backlog de tarefas",
            description="Retorna a diferença entre tarefas criadas e finalizadas por dia.")
async def get_tasks_backlog(current_user_id: dict = Depends(verify_token_user)):
    data = await service.get_tasks_backlog(
        user_id=current_user_id["user_id"],
        role=current_user_id["role"]
    )

    return {
        "success": True,
        "data": data
    }

# Rota para obter o tempo de resposta das tarefas (dentro ou fora do SLA)
@router.get("/task/metrics/response-time",
            response_model=StandardResponseTimeResponse,
            summary="Obter tempo de resposta das tarefas",
            description="Retorna o percentual de tarefas concluídas dentro do SLA (até 3 horas).")
async def get_tasks_response_time(current_user_id: dict = Depends(verify_token_user)):
    data = await service.get_tasks_response_time(
        user_id=current_user_id["user_id"],
        role=current_user_id["role"]
    )

    return {
        "success": True,
        "data": data
    }

# Rota para obter o percentual de tarefas resolvidas dentro do prazo (SLA de 90%)
@router.get("/task/metrics/resolution-time",
            summary="Obter percentual de tarefas resolvidas dentro do prazo",
            description="Retorna o percentual de tarefas concluídas dentro do prazo (dueDate) agrupadas por dia.")
async def get_tasks_resolution_time(current_user_id: dict = Depends(verify_token_user)):
    data = await service.get_tasks_resolution_time(
        user_id=current_user_id["user_id"],
        role=current_user_id["role"]
    )

    return {
        "success": True,
        "data": data
    }

# Rota para obter o percentual de tarefas resolvidas dentro do prazo (SLA de 90%)
@router.get("/task/metrics/resolution-time",
            response_model=StandardResolutionTimeResponse,
            summary="Obter percentual de tarefas resolvidas dentro do prazo",
            description="Retorna o percentual de tarefas resolvidas dentro do prazo (SLA de 90%).")
async def get_tasks_resolution_time(current_user_id: dict = Depends(verify_token_user)):
    data = await service.get_tasks_resolution_time(
        user_id=current_user_id["user_id"],
        role=current_user_id["role"]
    )

    return {
        "success": True,
        "data": data
    }   