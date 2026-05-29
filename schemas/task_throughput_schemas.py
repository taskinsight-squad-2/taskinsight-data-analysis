from pydantic import BaseModel, Field

class StatusItemMetrics(BaseModel):
    """Estrutura interna de métricas para cada status individual."""
    count: int = Field(..., description="Quantidade total de tarefas neste status")
    percent: float = Field(..., description="Percentual que este status representa do total geral")

    