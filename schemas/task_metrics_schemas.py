from pydantic import BaseModel, Field

class StatusItemMetrics(BaseModel):
    """Estrutura interna de métricas para cada status individual."""
    count: int = Field(..., description="Quantidade total de tarefas neste status")
    percent: float = Field(..., description="Percentual que este status representa do total geral")

class TaskMetricsByStatusResponse(BaseModel):
    """Contrato final que mapeia a distribuição de todos os status."""
    total_tasks: int = Field(..., description="Total de tarefas considerado no cálculo dos percentuais")
    PENDING: StatusItemMetrics
    IN_PROGRESS: StatusItemMetrics
    DONE: StatusItemMetrics
    CANCELLED: StatusItemMetrics

    class Config:
        # Permite ler dados mesmo que venham como dicionários puros do Python
        from_attributes = True
