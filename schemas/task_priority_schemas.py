from pydantic import BaseModel, Field

class PriorityItemMetrics(BaseModel):
    """Estrutura interna de métricas para cada prioridade individual."""
    count: int = Field(..., description="Quantidade total de tarefas nesta prioridade")
    percent: float = Field(..., description="Percentual que esta prioridade representa do total geral")

class TaskMetricsByPriorityResponse(BaseModel):
    """Contrato final que mapeia a distribuição de todas as prioridades."""
    total_tasks: int = Field(..., description="Total de tarefas considerado no cálculo dos percentuais")
    HIGH: PriorityItemMetrics
    MEDIUM: PriorityItemMetrics
    LOW: PriorityItemMetrics

class StandardPriorityResponse(BaseModel):
    success: bool
    data: TaskMetricsByPriorityResponse